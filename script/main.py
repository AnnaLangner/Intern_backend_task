#A script that takes command and parameter as an argument
import argparse
import json 
import sqlite3


JSON_FILE = "init\persons.json"
persons =  json.load(open(JSON_FILE, encoding='utf-8'))


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


def create_user(conn, users):
  sql = ''' INSERT INTO users(
    NAME_FIRST
  ) 
    VALUES(?) '''
  cur = conn.cursor()
  cur.execute(sql, (users,))
  conn.commit()
  return cur.lastrowid


def init_db():  
  '''Initializing the database'''  

  database = "db/pythonsqliteusers.db"
  
  sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
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
  ); """

  conn = create_connection(database)

  #create table
  if conn is not None:
    create_table(conn, sql_create_users_table)
  else:
    print("Error! cannot create the database connection.")
  
  #create users
  with conn:
    user = ('Anna');
    user_id = create_user(conn, user)


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
