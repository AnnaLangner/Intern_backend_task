#A script that takes command and parameter as an argument
import argparse
import requests
import re


def init_argparser():
  """Fetch arguments from command line"""

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help='sub-command help')
  # create the parser for the first command
  parser_command = subparsers.add_parser('command', help='entry command')
  # add parameter
  parser_command.add_argument('--parameter', help='Entry parameter')
  args = parser.parse_args()
  return args


def init_db():
  init_argparser()
  '''Initializing the database'''
  
  print('Nothing is implemented')


def main():
  init_db()


main()
