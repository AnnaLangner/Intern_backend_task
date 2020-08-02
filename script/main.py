#A script that takes command and parameter as an argument
import argparse


def init_argparser():
  """Fetch arguments from command line"""

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')
  # create the parser for the init command
  parser_init = subparsers.add_parser('init', help='init command')
  # add parameter
  parser_init.add_argument('--file', help='Path to the initial file')
  # create the parser for the percentage command
  parser_percentage = subparsers.add_parser('percentage', help='Enter command')
  # add parameter
  parser_percentage.add_argument('--female', help='Enter gender')
  parser_percentage.add_argument('--male', help='Enter gender')
  args = parser.parse_args()
  return args


def init_db():  
  '''Initializing the database'''

  print('Nothing is implemented')


def main():
  init_argparser()
  init_db()


main()
