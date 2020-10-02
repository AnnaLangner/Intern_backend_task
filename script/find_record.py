import json 
from sys import argv


script, JSON_FILE, user_name  = argv


#JSON_FILE = "init\persons.json"
unflat_persons = json.load(open(JSON_FILE, encoding='utf-8'))
 

def find_user_name(first_name):
  list_of_persons = unflat_persons['results']
  record_found = False
  user_list = []
  for dict_of_person in list_of_persons:   
    gender = dict_of_person['gender']
    title = dict_of_person['name']['title']
    first_name = dict_of_person['name']['first']
    last_name = dict_of_person['name']['last']
    if first_name == user_name:
      record_found = True
      user_list.append((gender, title, first_name, last_name))
  if record_found == False:
    print('A user with this name does not exist')
  return(user_list)


def print_user_name(first_name):
  print_user = find_user_name(user_name)
  print(print_user)


print_user_name(user_name)
