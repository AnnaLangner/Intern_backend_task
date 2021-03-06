import unittest
import main
import sqlite3


def create_connection(db_file):
  conn = None
  try:
    conn = sqlite3.connect(db_file)
  except sqlite3.Error as e:
    print(e)
  
  return conn


class TestFunctionsRetrievingDataFromTheDatabase(unittest.TestCase):

  def setUp(self):
    self.connection = create_connection("../db/pythonsqliteusers.db")

  def test_most_popular_cities(self):
    self.assertEqual(len(main.most_popular_cities(self.connection, 5)), 5)
    self.assertEqual(len(main.most_popular_cities(self.connection, 3)), 3)
    self.assertEqual(len(main.most_popular_cities(self.connection, 10)), 10)

  def test_most_common_passwords(self):
    self.assertEqual(len(main.most_common_passwords(self.connection, 5)), 5)
    self.assertEqual(len(main.most_common_passwords(self.connection, 3)), 3)
    self.assertEqual(len(main.most_common_passwords(self.connection, 10)), 10)

  def test_users_born(self):
    self.assertEqual(len(main.users_born(self.connection, '1944-01-01', '1999-01-01')), 1000)
    self.assertEqual(len(main.users_born(self.connection, '1960-01-01', '1965-01-01')), 92)
    self.assertEqual(len(main.users_born(self.connection, '1990-05-11', '1991-06-10')), 21)

  def test_most_secure_passwords(self):
    self.assertEqual(len(main.most_secure_passwords(self.connection)), 29)

  def tearDown(self):
    self.connection.close()


class TestRemovesSpecialCharacters(unittest.TestCase):

  def test_remove_special_characters(self):

    self.assertEqual(main.clear_phone_number("04-56-18-88-34"),"0456188834")
    self.assertEqual(main.clear_phone_number("06-74-93-14-75"),"0674931475") 

    self.assertEqual(main.clear_phone_number("075 831 68 55"),"0758316855")
    self.assertEqual(main.clear_phone_number("075 292 22 27"),"0752922227")

    self.assertEqual(main.clear_phone_number("(394)-381-6746"),"3943816746")
    self.assertEqual(main.clear_phone_number("(361)-356-8993"),"3613568993")

    self.assertEqual(main.clear_phone_number("(00) 1170-0136"),"0011700136")
    self.assertEqual(main.clear_phone_number("(32) 7367-6536"),"3273676536")


  def test_are_no_special_characters(self):

    self.assertEqual(main.clear_phone_number("0456188834"),"0456188834")
    self.assertEqual(main.clear_phone_number("0674931475"),"0674931475") 


class TestIsLeapYear(unittest.TestCase):

  def test_is_leap_year(self):
    self.assertTrue(main.is_leap_year(400), True)
    self.assertTrue(main.is_leap_year(1960), True)
    self.assertTrue(main.is_leap_year(2000), True)
    self.assertTrue(main.is_leap_year(2020), True)
    self.assertTrue(main.is_leap_year(2024), True)

  def test_is_not_leap_year(self):
    self.assertFalse(main.is_leap_year(100), True)
    self.assertFalse(main.is_leap_year(2007), True)


if __name__ == '__main__':
    unittest.main()
