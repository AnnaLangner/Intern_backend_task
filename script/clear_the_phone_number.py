import json
import re


JSON_FILE = 'init/persons.json'
persons = json.load(open(JSON_FILE, encoding='utf-8'))


def clear_the_phone():
  persons_list = persons['results']
  for persons_dict in persons_list:
    phone = persons_dict['phone']       
    clear_phone = re.findall(r'[0-9]', phone)
    clear_phone = ''.join(clear_phone)
    persons_dict['phone'] = clear_phone

    cell = persons_dict['cell'] 
    clear_cell = re.findall(r'[0-9]', cell)
    clear_cell = ''.join(clear_cell)
    persons_dict['cell'] = clear_cell

  new_file = open(JSON_FILE, 'a')
  new_file.close()


clear_the_phone()
print(persons)