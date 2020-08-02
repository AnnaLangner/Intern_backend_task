#A script that takes command and parameter as an argument
import argparse
import requests
import re


def fetch_arguments():
  """Fetch arguments from command line"""

  parser = argparse.ArgumentParser()
  parser.add_argument('--command', help='entry command')
  parser.add_argument('--parameter', help='entry parameter: female, male, number or date')
  args = parser.parse_args()  
  return (args.command, args.parameter)

def init_db():
  '''Initializing the database'''
  
  print('Nothing is implemented')


def main():
  fetch_arguments()
  init_db()


main()
