"""
Formatter for tuples to dicts
"""

def dicts_formation(tuples, keys):
  final_result = []
  result = {}
  for element in tuples:
    for index in range(len(element)):
      if element[index] == None:
        result[keys[index]]=''
      else:
        result[keys[index]]=element[index]
    final_result.append(result.copy())
  return final_result
  
