#A script that takes command and parameter as an argument
import argparse
import json 
import sqlite3


JSON_FILE = "init\person-test.json"
unflat_persons =  json.load(open(JSON_FILE, encoding='utf-8'))


def flatten_persons(data):
  out = {}

  def flatten(item, name = ''):
    if type(item) is dict:
      for x in item:
        flatten(item[x], name + x + '_')
    elif type(item) is list:
      i = 0
      for x in item:
        flatten(x, name + str(i) + '_')
    else:
      out[name[:-1]] = item

  flatten(data)
  return out


persons = flatten_persons(unflat_persons)


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


def delete_table(conn):
    sql = 'DROP TABLE users'
    cur = conn.cursor()
    cur.execute(sql)
    print("Table dropped... ")
    conn.commit()


def create_user(conn, users):
  sql = '''INSERT INTO users (
    GENDER,
    NAME_TITLE,
    NAME_FIRST,
    NAME_LAST,
    LOCATION_STREET_NUMBER,
    LOCATION_STREET_NAME,
    LOCATION_CITY,
    LOCATION_STATE,
    LOCATION_COUNTRY,
    LOCATION_POSTCODE,
    LOCATION_COORDINATES_LATITUDE,
    LOCATION_COORDINATES_LONGITUDE,
    LOCATION_TIMEZONE_OFFSET,
    LOCATION_TIMEZONE_DESCRIPTION,
    EMAIL,
    LOGIN_UUID,
    LOGIN_USERNAME,
    LOGIN_PASSWORD,
    LOGIN_SALT,
    LOGIN_MD5,
    LOGIN_SHA1,
    LOGIN_SHA256,
    DOB_DATE,
    DOB_AGE,
    REGISTERED_DATE,
    REGISTERED_AGE,
    PHONE,
    CELL,
    ID_NAME,
    ID_VALUE,
    PICTURE_LARGE,
    PICTURE_MEDIUM,
    PICTURE_THUMBNAIL,
    NAT
  ) 
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
 
  cur = conn.cursor()
  cur.execute(sql, users)
  conn.commit()


def init_db():  
  '''Initializing the database'''  

  database = "db/pythonsqliteusers.db"
  
  sql_create_users_table = ''' CREATE TABLE IF NOT EXISTS users (
    GENDER text,
    NAME_TITLE text,
    NAME_FIRST text NOT NULL,
    NAME_LAST text,
    LOCATION_STREET_NUMBER integer,
    LOCATION_STREET_NAME text,
    LOCATION_CITY text,
    LOCATION_STATE text,
    LOCATION_COUNTRY text,
    LOCATION_POSTCODE integer,
    LOCATION_COORDINATES_LATITUDE numeric,
    LOCATION_COORDINATES_LONGITUDE numeric,
    LOCATION_TIMEZONE_OFFSET numeric,
    LOCATION_TIMEZONE_DESCRIPTION text,
    EMAIL text,
    LOGIN_UUID text,
    LOGIN_USERNAME text,
    LOGIN_PASSWORD text,
    LOGIN_SALT text,
    LOGIN_MD5 text,
    LOGIN_SHA1 text,
    LOGIN_SHA256 text,
    DOB_DATE text,
    DOB_AGE text,
    REGISTERED_DATE text,
    REGISTERED_AGE text,
    PHONE text,
    CELL text,
    ID_NAME text,
    ID_VALUE text,
    PICTURE_LARGE text,
    PICTURE_MEDIUM text,
    PICTURE_THUMBNAIL text,
    NAT text
  ); '''

  conn = create_connection(database)  

  # create table
  if conn is not None:
    create_table(conn, sql_create_users_table)
  else:
    print("Error! cannot create the database connection.")
  
  with conn:
    user = (persons);
    user_id = create_user(conn, user)
    # delete_table(conn)

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


main()
