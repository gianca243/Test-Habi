"""
Python Lambda Function
"""
from cerberus import Validator
from datetime import timezone
import json
import datetime
import requests 
from src.utils.db_connection import db_connection
from src.utils.dicts_formation import dicts_formation
from src.schema.get_properties_with_filter_schema import body_schema
def get_properties_with_filter(event, *_context):
    """
    Returns (dict) with info about properties according given parameters

    Args:
      event (dict): Brings everything involve in the request
      context (dict): They are the user info

    Returns:
      statusCode (int): http code
      body (dict): response content
    """
    try:
      assert event.get('body'), (400, 'There is no body')

      body = json.loads(event.get('body')) if isinstance(event.get('body'), str) else event.get('body')
      schema = Validator(body_schema)
      if not schema.validate(body):
        raise Exception((400, schema.errors))      

      mydb = db_connection()
      my_cursor = mydb.cursor()

      query_string = ''
      query_string = query_filter(body.get('status'),body.get('city'),body.get('year'))      
      my_cursor.execute(query_string)
      myresult = my_cursor.fetchall()

      keys = ['status', 'address', 'city', 'price', 'description']
      myresult = dicts_formation(myresult,keys)
      
      return {
        'statusCode': 200,
        'body': json.dumps({
            'success': True,
            'message': 'Document found successfully',
            'propertys': myresult,
            'timestamp': str(datetime.datetime.now(timezone.utc))
        })
      }
    except Exception as error:
      print('errorOMG',error)
      error = error.args[0]
      return {
          'statusCode': error[0] if isinstance(error, tuple) else 500,
          'body': json.dumps({
              'success': False,
              'message': 'Properties not found',
              'details': error[1] if isinstance(error, tuple) else error,
              'timestamp': str(datetime.datetime.now(timezone.utc))
          })
      }

def query_filter(status,city,year):
  """
    Returns (string) with a query with filters according with given parameters

    Args:
      status (string): Is the status of a property
      city (string): Is the city where the property is
      year (number):Is the year when the building was made

    Returns:
      query_string (string): is the complete query
    """
  query_string ="""
    SELECT st.name, po.address, po.city, po.price, po.description
    FROM status_history t1
    INNER JOIN
    (
        SELECT `property_id`, MAX(update_date) AS upt
        FROM status_history
        GROUP BY `property_id`
    ) t2
        ON t1.`property_id` = t2.`property_id` AND t1.update_date = t2.upt
    JOIN status st ON st.id = t1.status_id
    JOIN property po ON po.id = t1.property_id 
    WHERE 1=1
  """
  if city != None and city != '':
    query_string += f" AND city = '{city}'"

  if year != None and year != '':
    query_string += f" AND year = '{year}'"
  
  if status != None and status != '':
    query_string += f" AND name = '{status}'"
  else:
    query_string +=" AND (name = 'en_venta' OR name = 'pre_venta' OR name = 'vendido')"
  # (name = "en_venta" OR name = "pre_venta" OR name = "vendido")
  # query_string += f" AND city = '{city}'"
  return query_string

