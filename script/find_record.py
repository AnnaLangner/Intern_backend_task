import json 


JSON_FILE = "init\persons.json"
unflat_persons = json.load(open(JSON_FILE, encoding='utf-8'))
 

def print_user_name(first_name, last_name):
  list_of_persons = unflat_persons['results']
  for dict_of_person in list_of_persons:   
    gender = dict_of_person['gender']
    title = dict_of_person['name']['title']
    first_name = dict_of_person['name']['first']
    last_name = dict_of_person['name']['last']
    print('first_name:' + first_name + '\n')
    print('last_name: ' + last_name+ '\n')

print_user_name('first', 'last')
