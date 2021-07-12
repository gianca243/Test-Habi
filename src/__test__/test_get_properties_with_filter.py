'''
Unit tests
'''
from src.functions.get_properties_with_filter import get_properties_with_filter
from unittest import mock
import json

class TestClass:
  '''Unit tests for get_properties_with_filter function
  '''
  event = {}

  @mock.patch('src.functions.get_properties_with_filter.db_connection')
  def setup_method(self, *_module):
    self.event = {
        'body': {
          "year": 2000,
          "city": "bogota",
          "status": "pre_venta" 
        }
    }
  @mock.patch('src.functions.get_properties_with_filter.db_connection')
  def test_200_successfull_request(self, mock_function):
    db_SQL = SQL_connection()
    mock_function.return_value = db_SQL
    response = get_properties_with_filter(self.event, {})
    response_body = json.loads(response['body'])
    status_code = response['statusCode']
    message = response_body['message']
    expected_message = 'Document found successfully'
    assert status_code == 200, f'statusCode must be 200, got {status_code}'
    assert message == expected_message, f'message must be "{expected_message}", got "{message}"'

  def test_400_no_body_request(self):
    self.event.pop('body')    
    response = get_properties_with_filter(self.event, {})
    response_body = json.loads(response['body'])
    status_code = response['statusCode']
    message = response_body['message']
    expected_message = 'Properties not found'
    assert status_code == 400, f'statusCode must be 200, got {status_code}'
    assert message == expected_message, f'message must be "{expected_message}", got "{message}"'

  @mock.patch('src.functions.get_properties_with_filter.db_connection')
  def test_500_successfull_request(self, mock_function):
    class SQL_connection_failed(SQL_connection):
      def execute(self, *_body):
        raise Exception('error')
    db_SQL = SQL_connection_failed()
    mock_function.return_value = db_SQL
    response = get_properties_with_filter(self.event, {})
    print(response)
    response_body = json.loads(response['body'])
    status_code = response['statusCode']
    message = response_body['message']
    expected_message = 'Properties not found'
    assert status_code == 500, f'statusCode must be 500, got {status_code}'
    assert message == expected_message, f'message must be "{expected_message}", got "{message}"'

class SQL_connection:
  """
  Utility class for unit tests
  Mocks SQL Collection class
  """
  def cursor(self, *_body):
    return self

  def execute(self, *_query):
    return self

  def fetchall(self):
    return [('pre_venta','calle 23 #45-67',None,120000000,'Hermoso apartamento en el centro de la ciudad')]