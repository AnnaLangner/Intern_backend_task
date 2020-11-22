import unittest
import main


class TestRemovesSpecialCharacters(unittest.TestCase):

  def test_remove_special_characters(self):

    self.assertEqual(main.clear_phone_numbers("04-56-18-88-34"),"0456188834")
    self.assertEqual(main.clear_phone_numbers("06-74-93-14-75"),"0674931475") 

    self.assertEqual(main.clear_phone_numbers("075 831 68 55"),"0758316855")
    self.assertEqual(main.clear_phone_numbers("075 292 22 27"),"0752922227")

    self.assertEqual(main.clear_phone_numbers("(394)-381-6746"),"3943816746")
    self.assertEqual(main.clear_phone_numbers("(361)-356-8993"),"3613568993")

    self.assertEqual(main.clear_phone_numbers("(00) 1170-0136"),"0011700136")
    self.assertEqual(main.clear_phone_numbers("(32) 7367-6536"),"3273676536")


  def test_are_no_special_characters(self):

    self.assertEqual(main.clear_phone_numbers("0456188834"),"0456188834")
    self.assertEqual(main.clear_phone_numbers("0674931475"),"0674931475") 


class TestIsLeapYear(unittest.TestCase):

  def test_is_leap_year(self):
    self.assertTrue(main.is_leap_year(400), True)
    self.assertTrue(main.is_leap_year(1960), True)
    self.assertTrue(main.is_leap_year(2000), True)
    self.assertTrue(main.is_leap_year(2020), True)
    self.assertTrue(main.is_leap_year(2024), True)

  def test_is_not_leap_year(self):
    self.assertFalse(main.is_leap_year(100), True)

if __name__ == '__main__':
    unittest.main()