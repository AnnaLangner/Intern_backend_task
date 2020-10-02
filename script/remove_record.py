import json


JSON_FILE = 'init/persons-test.json'
persons = json.load(open(JSON_FILE, encoding='utf-8'))


def find_record_with_picture():
  record_names = []
  dict_json_to_list = persons['results']
  for dict_single_record in dict_json_to_list:
    if 'picture' in dict_single_record:
      record_names.append(dict_single_record)
  return record_names


def remove_record_from_json(records):
  for record in records:
    del record['picture']
  


def main():
  records = find_record_with_picture()
  remove_record_from_json(records)


main()
print(persons)