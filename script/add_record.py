import json
from datetime import datetime


persons = json.load(open('init/persons-test.json', encoding='utf-8'))

def find_record_with_dob():
  record_names = []
  dict_json_to_list = persons['results']
  for dict_single_record in dict_json_to_list:
    if 'dob' in dict_single_record:
      record_names.append(dict_single_record)
  return record_names


def create_new_record_in_dob(records):
  for record in records:
    days_left = 0
    born = record['dob']['date']
    date_born_dt = datetime.strptime(born, '%Y-%m-%dT%H:%M:%S.%fZ')
    today = datetime.now().timetuple().tm_yday
    birthday_day = date_born_dt.timetuple().tm_yday
    if today > birthday_day:
      days_left = (365-today)+birthday_day
    else:
      days_left = birthday_day - today    
    dob_new_record = {"time_until_birthday": str(days_left)}
    record["dob"].update(dob_new_record)
 

def main():
  records = find_record_with_dob()
  create_new_record_in_dob(records)  


main()
