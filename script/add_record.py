import json
from datetime import datetime

JSON_FILE = 'init/persons-test.json'
persons = json.load(open(JSON_FILE, encoding='utf-8'))


def add_record_to_json():
  dict_json_to_list = persons['results']
  for dict_single_record in dict_json_to_list:
    if 'dob' in dict_single_record:
      born = dict_single_record['dob']['date']
      date_born = born[0:10]
      date_born_dt = datetime.strptime(date_born, '%Y-%m-%d')
      today = datetime.now()
      time_until_birth = today - date_born_dt
      dob_new_record = {"time_until_birth": str(time_until_birth)}
      dict_single_record["dob"].update(dob_new_record)

  new_file = open(JSON_FILE, 'a')
  new_file.close()


add_record_to_json()
print(persons)