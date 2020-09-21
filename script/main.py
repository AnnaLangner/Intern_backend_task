#A script that takes command and parameter as an argument
import argparse
import json 
import sqlite3


JSON_FILE = "init\persons.json"
unflat_people =  json.load(open(JSON_FILE, encoding='utf-8'))


people = []

list_of_people = unflat_people['results']
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
  registered_date = dict_of_person['registered']['date']
  registered_age = dict_of_person['registered']['age']
  phone = dict_of_person['phone']
  cell = dict_of_person['cell']
  id_name = dict_of_person['id']['name']
  id_value = dict_of_person['id']['value']
  picture_large = dict_of_person['picture']['large']
  picture_medium = dict_of_person['picture']['medium']
  picture_thumbnail = dict_of_person['picture']['thumbnail']
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
    registered_date,
    registered_age,
    phone,
    cell,
    id_name,
    id_value,
    picture_large,
    picture_medium,
    picture_thumbnail,
    nat
  ]

  people.append(columns)



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


def create_connection(db_file):
  conn = None
  try:
    conn = sqlite3.connect(db_file)
  except sqlite3.Error as e:
    print(e)
  
  return conn


def create_table(conn, create_table_sql):
  try:
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
  except sqlite3.Error as e:
    print(e)  


def delete_all_users(conn):
    sql = 'DELETE FROM users'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def delete_table(conn):
    sql = 'DROP TABLE users'
    cur = conn.cursor()
    cur.execute(sql)
    print("Table dropped... ")
    conn.commit()


def create_user(conn, users):
  sql = '''INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
  cur = conn.cursor()
  for columns in people:
    cur.execute(sql, columns)  
  conn.commit()


def init_db():  
  '''Initializing the database'''  

  database = "db/pythonsqliteusers.db"
  
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
    registered_date text,
    registered_age text,
    phone text,
    cell text,
    id_name text,
    id_value text,
    picture_large text,
    picture_medium text,
    picture_thumbnail text,
    nat
  ); '''

  conn = create_connection(database)  

  # create table
  if conn is not None:
    create_table(conn, sql_create_users_table)
  else:
    print("Error! cannot create the database connection.")
  
  with conn:     
    person = (
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
      registered_date,
      registered_age,
      phone,
      cell,
      id_name,
      id_value,
      picture_large,
      picture_medium,
      picture_thumbnail,
      nat
    )
    user_id = create_user(conn, person)
    # delete_table(conn)
    # delete_all_users(conn)

def percentage():
  print('A function summarizing the percentage of women / men in the database')


def main():
  results = []
  args = init_argparser()
  if args.operation == 'init':
    results = init_db()
  elif args.operation == 'percentage':
    results = percentage()

  # for r in results:
  #   print(r)  
  print(args.operation)
  print(len(people))

main()
