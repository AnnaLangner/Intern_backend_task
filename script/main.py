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


def init_db():  
  '''Initializing the database'''  
    
  conn = None
  try:
    conn = sqlite3.connect("db/db_file.db")
  except sqlite3.Error as e:
    print(e)

  cursor = conn.cursor()
  cursor.execute('DROP TABLE IF EXISTS USERS')
  sql_users_table = """ CREATE TABLE USERS (
    GENDER,
    NAME_TITLE,
    NAME_FIRST CHAR(20) NOT NULL,
    NAME_LAST CHAR(20),
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
    PICTURE_MEDIUM
    PICTURE_THUMBNAIL,
    NAT
  ); """

  cursor.execute(sql_users_table)
  conn.commit()
  conn.close()


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
