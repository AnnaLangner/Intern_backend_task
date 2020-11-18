import unittest
import main


structure_to_test =[{"phone":"04-56-18-88-34","cell":"06-74-93-14-75"},{"phone":"17533450","cell":"67583818"},{"phone":"075 831 68 55","cell":"075 292 22 27"},{"phone":"(394)-381-6746","cell":"(361)-356-8993"},{"phone":"(00) 1170-0136","cell":"(32) 7367-6536"}]


class TestRemovesSpecialCharacters(unittest.TestCase):

  def test_remove_special_characters(self):
    dict1 = {
      "phone":"04-56-18-88-34",
      "cell":"06-74-93-14-75"
    }
    dict2 = {
      "phone":"075 831 68 55",
      "cell":"075 292 22 27"
    }
    dict3 = {
      "phone":"(394)-381-6746",
      "cell":"(361)-356-8993"
    }
    dict4 = {
      "phone":"(00) 1170-0136",
      "cell":"(32) 7367-6536"
    }
    list_dict = [dict1, dict2, dict3, dict4]

    self.assertEqual("04-56-18-88-34", list_dict[0]["phone"])
    self.assertEqual("06-74-93-14-75", list_dict[0]["cell"])

    self.assertEqual("075 831 68 55", list_dict[1]["phone"])
    self.assertEqual("075 292 22 27", list_dict[1]["cell"])

    self.assertEqual("(394)-381-6746", list_dict[2]["phone"])
    self.assertEqual("(361)-356-8993", list_dict[2]["cell"])

    self.assertEqual("(00) 1170-0136", list_dict[3]["phone"])
    self.assertEqual("(32) 7367-6536", list_dict[3]["cell"])

    main.remove_special_characters_from_phone_numbers(list_dict)

    self.assertEqual("0456188834", list_dict[0]["phone"])
    self.assertEqual("0674931475", list_dict[0]["cell"]) 

    self.assertEqual("0758316855", list_dict[1]["phone"])
    self.assertEqual("0752922227", list_dict[1]["cell"])

    self.assertEqual("3943816746", list_dict[2]["phone"])
    self.assertEqual("3613568993", list_dict[2]["cell"])

    self.assertEqual("0011700136", list_dict[3]["phone"])
    self.assertEqual("3273676536", list_dict[3]["cell"])


class TestDigitAddition(unittest.TestCase):
  def test_addition(self):
    number1 = 2
    number2 = 4
    sum_numbers = number1 + number2
    self.assertTrue(6, sum_numbers)


if __name__ == '__main__':
    unittest.main()