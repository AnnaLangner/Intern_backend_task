import json
import re


persons = json.load(open('init/persons.json', encoding='utf-8'))


def find_record_with_picture():
  record_names = []
  dict_json_to_list = persons['results']
  for dict_single_record in dict_json_to_list:
    if 'phone' and 'cell' in dict_single_record:
      record_names.append(dict_single_record)
  return record_names


def clear_the_phone(records):
  for record in records:
    phone = record['phone']       
    clear_phone = re.findall(r'[0-9]', phone)
    clear_phone = ''.join(clear_phone)
    record['phone'] = clear_phone

    cell = record['cell'] 
    clear_cell = re.findall(r'[0-9]', cell)
    clear_cell = ''.join(clear_cell)
    record['cell'] = clear_cell


def main():
  records = find_record_with_picture()
  clear_the_phone(records)
  

main()