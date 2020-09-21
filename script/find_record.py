import json 


JSON_FILE = "init\person-test.json"
unflat_persons =  json.load(open(JSON_FILE, encoding='utf-8'))


list_of_persons = unflat_persons['results']
for dict_of_person in list_of_persons:   
  gender = dict_of_person['gender']
  title = dict_of_person['name']['title']
  first_name = dict_of_person['name']['first']
  last_name = dict_of_person['name']['last']
  print(gender)
  print(title)
  print(first_name)
  print(last_name)
