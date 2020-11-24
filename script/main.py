#A script that takes command and parameter as an argument
import re
import argparse
import json 
import sqlite3
from datetime import datetime, date


def fetch_arguments():
  """Fetch arguments from command line"""

  parser = argparse.ArgumentParser()
  parser.add_argument('command', help='list of command: init, percentage,average-age, most-popular-cities, most-common-passwords, users-born, most-secure-password')
  # parameter
  parser.add_argument('--file', help='Path to the initial file')
  parser.add_argument('--gender', help='Enter female or male')
  parser.add_argument('--number', type=int, help='Enter the number of cities to display')
  parser.add_argument('--start-date', type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
  parser.add_argument('--end-date', type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
  args = parser.parse_args()
  return (args.command, args.file, args.gender, args.number, args.start_date, args.end_date)


def convert_dict_to_list_extract_dob_and_phone_numbers(people):
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
  

def clear_phone_number(phone):
  clear_phone = re.sub(r'\(|\)|\-|\+|\s', '', phone)
  return clear_phone


def remove_special_characters_from_phone_numbers(phone_fields):
  for field in phone_fields:     
    field['phone'] = clear_phone_number(field['phone'])
    
    field['cell'] = clear_phone_number(field['cell'])

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


def init_db(conn, file):  
  people =  json.load(open(file , encoding='utf-8'))
  (phone_fields, dob_fields) = convert_dict_to_list_extract_dob_and_phone_numbers(people)
  add_field_time_until_birthday(dob_fields)
  remove_special_characters_from_phone_numbers(phone_fields)

  # create table
  if conn is not None:
    create_users_table(conn)    
  
  insert_users_to_db(conn, people)


def select_all_gender_and_dob_date(conn):
  cur = conn.cursor()
  cur.execute("SELECT gender, dob_date FROM users")
  gender_rows = cur.fetchall() 
  return gender_rows


def percentage(conn, gender):
  gender_rows = select_all_gender_and_dob_date(conn) 
  gender_list = [i[0] for i in gender_rows]  
  male = 0
  female = 0
  for item in gender_list:
    if item == 'male':
      male = male + 1
    else:
      female = female + 1
  percentage_of_women = ((female * 100)/(female + male))
  percentage_of_men = ((male * 100)/(female + male))
  if gender == 'male':
    print('Percentage of men: ' , percentage_of_men, '%')
  elif gender == 'female':
    print('Percentage of women: ' , percentage_of_women, '%')
  else:
    print('You are entering the wrong gender')


def average_age(conn, gender):
  gender_rows = select_all_gender_and_dob_date(conn)    
  male = 0
  female = 0
  sum_of_age_male = 0
  sum_of_age_female = 0
  today = date.today().year

  for item in gender_rows:
    full_date_of_birth = datetime.strptime(item[1], '%Y-%m-%dT%H:%M:%S.%fZ')
    yaer_of_birth = full_date_of_birth.date().year  
    age = today - yaer_of_birth
    if item[0] == 'male':
      male = male + 1
      sum_of_age_male = sum_of_age_male + age
    else:
      female = female + 1
      sum_of_age_female = sum_of_age_female + age

  average_age_of_men = float(sum_of_age_male/male)
  average_age_of_women = float(sum_of_age_female/female)
  average_age_overall = float((sum_of_age_male + sum_of_age_female)/(male + female))

  if gender == 'male':
    print('Average age of men: {value:.2f} years'.format(value = average_age_of_men))
  elif gender == 'female':
    print('Average age of women: {value:.2f} years'.format(value = average_age_of_women))
  else:
    print('Overall average age: {value:.2f} years'.format(value = average_age_overall))


def most_popular_cities(conn, number):
  cur = conn.cursor()
  command = "SELECT location_city, count(location_city) FROM users GROUP BY location_city ORDER BY count(location_city) DESC LIMIT ?"
  cur.execute(command, (number,))
  cities = cur.fetchall()  
  cities_list = []
  for city in cities:
      city_name = city[0]
      city_occurrences = city[1] 
      cities_list.append((city_name, city_occurrences))
  return cities_list
  

def most_common_passwords(conn, number):
  cur = conn.cursor()
  command = "SELECT login_password, COUNT(login_password) FROM users GROUP BY login_password ORDER BY COUNT(login_password) DESC limit ?"
  cur.execute(command, (number,))
  passwords = cur.fetchall()
  passwords_list = []
  for password in passwords:
    password_value = password[0]
    password_occurrences = password[1]
    passwords_list.append((password_value, password_occurrences))
  return passwords_list  


def users_born(conn, start_date, end_date):
  cur = conn.cursor()
  command = "SELECT name_first, name_last, dob_date FROM users WHERE dob_date BETWEEN ? and ? ORDER BY dob_date ASC"
  cur.execute(command, (start_date, end_date))
  users_data = cur.fetchall() 
  user_data_list = []
  for user_data in users_data:
    user_name = user_data[0]
    user_last_name = user_data[1]
    user_date_birth = user_data[2]
    full_date_of_birth = datetime.strptime(user_date_birth, '%Y-%m-%dT%H:%M:%S.%fZ')
    date_of_birth = full_date_of_birth.date()
    user_data_list.append((user_name, user_last_name, date_of_birth))
  return user_data_list


def most_secure_passwords(conn):
  cur = conn.cursor()
  command = 'SELECT login_password FROM users'
  cur.execute(command)
  passwords_tuple = cur.fetchall()
  passwords_list = []
  for item in passwords_tuple:
    passwords_list.append(item[0])

  password_and_score_tuple_list = []
  for password in passwords_list:
    total = 0
    if len(password) >= 8:
      total += 5      
    if any(letter.isupper() for letter in password):
      total += 2
    if any(letter.islower() for letter in password):
      total += 1
    if any(letter.isdigit() for letter in password):
      total += 1
    if any(not letter.isalnum() for letter in password):
      total += 3
    if total >= 7:
      password_and_score_tuple_list.append((password, total))
    
  return password_and_score_tuple_list  


def main():
  conn = create_connection('db/pythonsqliteusers.db')
  (command, file, gender, number, start_date, end_date) = fetch_arguments()    
  if command == 'init':  
    init_db(conn, file)
  elif command == 'percentage':
    percentage(conn, gender)
  elif command == 'average-age':
    average_age(conn, gender)
  elif command == 'most-popular-cities':
    cities_list = most_popular_cities(conn, number)
    for result in cities_list:
      print(f'City {result[0]} occurr {result[1]} times.')
  elif command == 'most-common-passwords':
    passwords_list = most_common_passwords(conn, number)
    for result in passwords_list:
      print(f'Password {result[0]} occurr {result[1]} times.')
  elif command == 'users-born':
    users_data = users_born(conn, start_date, end_date)
    for user_data in users_data:
      print(f'User {user_data[0]} {user_data[1]} was born in {user_data[2]}')
  elif command == 'most-secure-password':
    password_and_score_tuple_list = most_secure_passwords(conn)
    for result in password_and_score_tuple_list:
      print(f'This password: {result[0]} it is secure, get {result[1]} points')


if __name__ == "__main__":
  main()
