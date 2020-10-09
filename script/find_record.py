import json 
from sys import argv


script, JSON_FILE, user_name  = argv


unflat_persons = json.load(open(JSON_FILE, encoding='utf-8'))
 

def find_users_by_name(first_name):
  list_of_persons = unflat_persons['results']
  user_list = []
  for dict_of_person in list_of_persons:   
    gender = dict_of_person['gender']
    title = dict_of_person['name']['title']
    first_name = dict_of_person['name']['first']
    last_name = dict_of_person['name']['last']
    if first_name == user_name:
      user_list.append((gender, title, first_name, last_name))
  return user_list


def print_users(users):  
  if users == []:
     print('A user with this name does not exist')
  else:
    record_num = 0
    print(' # | gender     | title      | first_name | last_name  |')
    print('----------------------------------------------------------')
    for item in users:   
      record_num += 1  
      print(f' {record_num} | {item[0]:10} | {item[1]:10} | {item[2]:10} | {item[3]:10} |')
      print('----------------------------------------------------------')
    

def main():
  users = find_users_by_name(user_name)
  print_users(users)


main()
