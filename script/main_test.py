import unittest
import main


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

    self.assertEqual(main.clear_phone_numbers("04-56-18-88-34"),"0456188834")
    self.assertEqual(main.clear_phone_numbers("06-74-93-14-75"),"0674931475") 

    self.assertEqual(main.clear_phone_numbers("075 831 68 55"),"0758316855")
    self.assertEqual(main.clear_phone_numbers("075 292 22 27"),"0752922227")

    self.assertEqual(main.clear_phone_numbers("(394)-381-6746"),"3943816746")
    self.assertEqual(main.clear_phone_numbers("(361)-356-8993"),"3613568993")

    self.assertEqual(main.clear_phone_numbers("(00) 1170-0136"),"0011700136")
    self.assertEqual(main.clear_phone_numbers("(32) 7367-6536"),"3273676536")


  def test_are_no_special_characters(self):
    dict1 = {
      "phone":"0456188834",
      "cell":"0674931475"
    }
    dict2 = {
      "phone":"0758316855",
      "cell":"0752922227"
    }
    dict3 = {
      "phone":"3943816746",
      "cell":"3613568993"
    }
    dict4 = {
      "phone":"0011700136",
      "cell":"3273676536"
    }
    list_dict = [dict1, dict2, dict3, dict4]

    main.remove_special_characters_from_phone_numbers(list_dict)

    self.assertEqual(main.clear_phone_numbers("0456188834"),"0456188834")
    self.assertEqual(main.clear_phone_numbers("0674931475"),"0674931475") 

    self.assertEqual(main.clear_phone_numbers("0758316855"),"0758316855")
    self.assertEqual(main.clear_phone_numbers("0752922227"),"0752922227")

    self.assertEqual(main.clear_phone_numbers("3943816746"),"3943816746")
    self.assertEqual(main.clear_phone_numbers("3613568993"),"3613568993")

    self.assertEqual(main.clear_phone_numbers("0011700136"),"0011700136")
    self.assertEqual(main.clear_phone_numbers("3273676536"),"3273676536")


if __name__ == '__main__':
    unittest.main()