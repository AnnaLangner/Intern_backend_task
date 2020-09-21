#A script that takes command and parameter as an argument
import argparse


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

  print('Nothing is implemented')


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
import json 


JSON_FILE = "init\person-test.json"
unflat_persons =  json.load(open(JSON_FILE, encoding='utf-8'))
 

def print_user_name(first_name, last_name):
  list_of_persons = unflat_persons['results']
  for dict_of_person in list_of_persons:   
    gender = dict_of_person['gender']
    title = dict_of_person['name']['title']
    first_name = dict_of_person['name']['first']
    last_name = dict_of_person['name']['last']
    print('first_name:' + first_name + '\n')
    print('last_name: ' + last_name+ '\n')

print_user_name('first', 'last')