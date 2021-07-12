"""
Schema valitation for get_properties_with_filter function
"""
body_schema = {
  'year':{
    'type':'number',
    'required': False
  },
  'city':{
    'type':'string',
    'required': False
  },
  'status':{
    'type':'string',
    'required': False,
    'allowed': ['pre_venta', 'en_venta', 'vendido', '']
  }
}