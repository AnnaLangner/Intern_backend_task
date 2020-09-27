import json


JSON_FILE = 'init/persons-test.json'
persons = json.load(open(JSON_FILE, encoding='utf-8'))


def remove_record_from_json():
  dict_json_to_list = persons['results']
  for dict_single_record in dict_json_to_list:
    if 'picture' in dict_single_record:
      del dict_single_record['picture']

  new_file = open(JSON_FILE, 'a')
  new_file.close()


remove_record_from_json()
print(persons)