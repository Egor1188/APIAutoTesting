import json

json_as_string = '{"answer":"Hello, User"}'
obj = json.loads(json_as_string)
print(obj)