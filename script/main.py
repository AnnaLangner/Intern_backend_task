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
