#A script that takes command and parameter as an argument
import re
import argparse
import json 
import sqlite3
from datetime import datetime, date


def init_argparser():
  """Fetch arguments from command line"""

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help='sub-command help', dest='operation')
  # create the parser for the init command
  parser_init = subparsers.add_parser('init', help='init command')
  # add parameter
  parser_init.add_argument('--file', help='Path to the initial file')
  # create the parser for the percentage command
  parser_percentage = subparsers.add_parser('percentage', help='percent of female or male')
  # add parameter
  parser_percentage.add_argument('--gender', help='Enter female or male')
  args = parser.parse_args()
  return args


def find_records(people_json):
  record_names_phone = []
  record_names_with_dob =[] 
  dict_json_to_list = people_json['results']
  for dict_single_record in dict_json_to_list:
    if 'phone' and 'cell' in dict_single_record:
      record_names_phone.append(dict_single_record)
    if 'dob' in dict_single_record:
      record_names_with_dob.append(dict_single_record)
  return (record_names_phone, record_names_with_dob)


def is_leap_year(year):
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def create_new_record_with_dob_in_json(dob_records):
  for record in dob_records:
    born = record['dob']['date']
    full_date_of_birth = datetime.strptime(born, '%Y-%m-%dT%H:%M:%S.%fZ')
    date_of_birth = full_date_of_birth.date()
    today = date.today()
    is_leap_year_birthday = False
    if date_of_birth.month == 2 and date_of_birth.day == 29 and is_leap_year(today.year) == False:
      is_leap_year_birthday = True
      date_of_birth = date_of_birth.replace(day=28)
    date_of_the_nearest_birthday = date_of_birth.replace(year=today.year)
    if date_of_the_nearest_birthday < today:
      if date_of_birth.month == 2 and date_of_birth.day == 29 and is_leap_year(today.year + 1) == False:
        date_of_birth = date_of_birth.replace(day=28)
      date_of_the_nearest_birthday = date_of_birth.replace(year=today.year +1)
      if is_leap_year_birthday:
        date_of_the_nearest_birthday = date_of_the_nearest_birthday.replace(day=29)      
    days_left = abs(date_of_the_nearest_birthday - today).days    
    dob_new_record_time_until_birthday = {"time_until_birthday": days_left}
    record["dob"].update(dob_new_record_time_until_birthday)
  

def removes_special_characters_from_phone_and_cell_numbers(phone_records):
  for record in phone_records:
    phone = record['phone']       
    clear_phone = re.sub(r'\(|\)|\-|\+|\s', '', phone)
    record['phone'] = clear_phone

    cell = record['cell'] 
    clear_cell = re.sub(r'\(|\)|\-|\+|\s', '', cell)
    record['cell'] = clear_cell


def remove_record_with_picture_from_json(people_json):
  dict_json_to_list = people_json['results']
  for dict_single_record in dict_json_to_list:
    if 'picture' in dict_single_record:
      del dict_single_record['picture']


def create_connection(db_file):
  conn = None
  try:
    conn = sqlite3.connect(db_file)
  except sqlite3.Error as e:
    print(e)
  
  return conn


def create_users_table(conn):
  sql_create_users_table = ''' CREATE TABLE IF NOT EXISTS users (
    gender text,
    name_title text,
    name_first text,
    name_last text,
    location_street_number integer,
    location_street_name text,
    location_city text,
    location_state text,
    location_country text,
    location_postcode integer,
    location_coordinates_latitude numeric,
    location_coordinates_longitude numeric,
    location_timezone_offset numeric,
    location_timezone_description text,
    email text,
    login_uuid text,
    login_username text,
    login_password text,
    login_salt text,
    login_md5 text,
    login_sha1 text,
    login_sha256 text,
    dob_date text,
    dob_age text,
    dob_time_until_birthday integer,
    registered_date text,
    registered_age text,
    phone text,
    cell text,
    id_name text,
    id_value text,
    nat
  ); '''  

  try:
    cursor = conn.cursor()
    cursor.execute(sql_create_users_table)
  except sqlite3.Error as e:
    print(e)  


def insert_users_to_table(conn, users):
  sql = '''INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

  cur = conn.cursor()
  for columns in users:
    cur.execute(sql, columns)  
  conn.commit()


def init_db(conn):  
  '''Initializing the database'''    

  # create table
  if conn is not None:
    create_users_table(conn)  
  
  people_json =  json.load(open("init\persons.json", encoding='utf-8'))
  (phone_records, dob_records) = find_records(people_json)
  create_new_record_with_dob_in_json(dob_records)
  removes_special_characters_from_phone_and_cell_numbers(phone_records)
  remove_record_with_picture_from_json(people_json)
  import_users_to_db(conn, people_json)
  

def import_users_to_db(conn, people_json):
  people = []

  list_of_people = people_json['results']
  for dict_of_person in list_of_people:   
    gender = dict_of_person['gender']
    name_title = dict_of_person['name']['title']
    name_first = dict_of_person['name']['first']
    name_last = dict_of_person['name']['last']
    location_street_number = dict_of_person['location']['street']['number']
    location_street_name = dict_of_person['location']['street']['name']
    location_city = dict_of_person['location']['city']
    location_state = dict_of_person['location']['state']
    location_country = dict_of_person['location']['country']
    location_postcode = dict_of_person['location']['postcode']
    location_coordinates_latitude = dict_of_person['location']['coordinates']['latitude']
    location_coordinates_longitude = dict_of_person['location']['coordinates']['longitude']
    location_timezone_offset = dict_of_person['location']['timezone']['offset']
    location_timezone_description = dict_of_person['location']['timezone']['description']
    email = dict_of_person['email']
    login_uuid = dict_of_person['login']['uuid']
    login_username = dict_of_person['login']['username']
    login_password = dict_of_person['login']['password']
    login_salt = dict_of_person['login']['salt']
    login_md5 = dict_of_person['login']['md5']
    login_sha1 = dict_of_person['login']['sha1']
    login_sha256 = dict_of_person['login']['sha256']
    dob_date = dict_of_person['dob']['date']
    dob_age = dict_of_person['dob']['age']
    dob_time_until_birthday = dict_of_person['dob']['time_until_birthday']
    registered_date = dict_of_person['registered']['date']
    registered_age = dict_of_person['registered']['age']
    phone = dict_of_person['phone']
    cell = dict_of_person['cell']
    id_name = dict_of_person['id']['name']
    id_value = dict_of_person['id']['value']
    nat = dict_of_person['nat']
    columns = [
      gender,
      name_title,
      name_first,
      name_last,
      location_street_number,
      location_street_name,
      location_city,
      location_state,
      location_country,
      location_postcode,
      location_coordinates_latitude,
      location_coordinates_longitude,
      location_timezone_offset,
      location_timezone_description,
      email,
      login_uuid,
      login_username,
      login_password,
      login_salt,
      login_md5,
      login_sha1,
      login_sha256,
      dob_date,
      dob_age,
      dob_time_until_birthday,
      registered_date,
      registered_age,
      phone,
      cell,
      id_name,
      id_value,
      nat
    ]

    people.append(columns)      
    
  insert_users_to_table(conn, people)


def percentage():
  print('A function summarizing the percentage of women / men in the database')


def main():
  results = []  
  conn = create_connection('db/pythonsqliteusers.db')
  args = init_argparser()    
  if args.operation == 'init':  
    init_db(conn)
  elif args.operation == 'percentage':
    results = percentage()

  # for r in results:
  #   print(r)  

main()
