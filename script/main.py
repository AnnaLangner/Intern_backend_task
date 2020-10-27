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


def convert_dict_to_list_access_phone_cell_dob_field(people):
  field_names_phone = []
  field_names_with_dob =[] 
  dict_json_to_list = people['results']
  for dict_single_field in dict_json_to_list:
    if 'phone' and 'cell' in dict_single_field:
      field_names_phone.append(dict_single_field)
    if 'dob' in dict_single_field:
      field_names_with_dob.append(dict_single_field)
  return (field_names_phone, field_names_with_dob)


def is_leap_year(year):
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def add_field_time_until_birthday(dob_fields):
  for field in dob_fields:
    born = field['dob']['date']
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
    dob_new_field_time_until_birthday = {"time_until_birthday": days_left}
    field["dob"].update(dob_new_field_time_until_birthday)
  

def remove_special_characters_from_phone_numbers(phone_fields):
  for field in phone_fields:
    phone = field['phone']       
    clear_phone = re.sub(r'\(|\)|\-|\+|\s', '', phone)
    field['phone'] = clear_phone

    cell = field['cell'] 
    clear_cell = re.sub(r'\(|\)|\-|\+|\s', '', cell)
    field['cell'] = clear_cell


def remove_field_with_picture_from_records(people):
  dict_json_to_list = people['results']
  for dict_single_field in dict_json_to_list:
    if 'picture' in dict_single_field:
      del dict_single_field['picture']


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


def insert_users_to_db(conn, people):
  users = []

  peoples = people['results']
  for dict_of_person in peoples:      
    fields = [
      dict_of_person['gender'],
      dict_of_person['name']['title'],
      dict_of_person['name']['first'],
      dict_of_person['name']['last'],
      dict_of_person['location']['street']['number'],
      dict_of_person['location']['street']['name'],
      dict_of_person['location']['city'],
      dict_of_person['location']['state'],
      dict_of_person['location']['country'],
      dict_of_person['location']['postcode'],
      dict_of_person['location']['coordinates']['latitude'],
      dict_of_person['location']['coordinates']['longitude'],
      dict_of_person['location']['timezone']['offset'],
      dict_of_person['location']['timezone']['description'],
      dict_of_person['email'],
      dict_of_person['login']['uuid'],
      dict_of_person['login']['username'],
      dict_of_person['login']['password'],
      dict_of_person['login']['salt'],
      dict_of_person['login']['md5'],
      dict_of_person['login']['sha1'],
      dict_of_person['login']['sha256'],
      dict_of_person['dob']['date'],
      dict_of_person['dob']['age'],
      dict_of_person['dob']['time_until_birthday'],
      dict_of_person['registered']['date'],
      dict_of_person['registered']['age'],
      dict_of_person['phone'],
      dict_of_person['cell'],
      dict_of_person['id']['name'],
      dict_of_person['id']['value'],
      dict_of_person['nat'],
    ]

    users.append(fields)      
    
  insert_users_to_table(conn, users)


def init_db(conn):  
  people =  json.load(open("init\persons.json", encoding='utf-8'))
  (phone_fields, dob_fields) = convert_dict_to_list_access_phone_cell_dob_field(people)
  add_field_time_until_birthday(dob_fields)
  remove_special_characters_from_phone_numbers(phone_fields)
  remove_field_with_picture_from_records(people)   

  # create table
  if conn is not None:
    create_users_table(conn)    
  
  insert_users_to_db(conn, people)
  

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
