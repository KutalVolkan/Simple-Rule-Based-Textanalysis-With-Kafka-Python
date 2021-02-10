import unittest
import regex_strategies

class TestRegex(unittest.TestCase):

    def test_regexGender(self):
    	res_0 = regex_strategies.regex_gender("Volkan is a man of heigth 182cm.")
    	res_1 = regex_strategies.regex_gender("Johanna is a female of heigth 175 cm.")
    	res_2 = regex_strategies.regex_gender("Johanna is a woman of heigth 175 cm and Volkan a man of height 182cm.")
    	self.assertEqual(res_0[0][2], "man")
    	self.assertEqual(res_1[0][2], "female")
    	self.assertEqual(res_2[0][2], "woman")
    	self.assertEqual(res_2[1][2], "man")

    def test_regexAge(self):
    	res_0 = regex_strategies.regex_age("Volkan is 29-year-old.")
    	self.assertEqual(res_0[0][2],"29-year-old")

    def test_regexWeight(self):
        res_0 = regex_strategies.regex_weight("Victoria is 173cm and weight 155 pounds.")
        res_1 = regex_strategies.regex_weight("Vitaly is 183cm and weight 100 kg.")
        res_2 = regex_strategies.regex_weight("Ali is 183cm and weight: 150 lbs.")
        res_3 = regex_strategies.regex_weight("The Baby is 35-weeks-old and weighs 9 pounds 10 ounces.")
        self.assertEqual(res_0[0], "weight 155 pounds")
        self.assertEqual(res_1[0], "weight 100 kg")
        self.assertEqual(res_2[0], "weight: 150 lbs")
        self.assertEqual(res_3[0], "weighs 9 pounds 10 ounces")
        
        # contextException
        res_4 = regex_strategies.regex_weight("The man lost 20 lbs in one year. ")
        res_5 = regex_strategies.regex_weight("Vitaly height 183 cm.")
        res_6 = regex_strategies.regex_weight("Volkan is 183 cm and lost 10 kg in the last couple months.")
        res_7 = regex_strategies.regex_weight("Weigth 19 gain.")
        self.assertEqual(res_4, "Unknown")
        self.assertEqual(res_5, "Unknown")
        self.assertEqual(res_6, "Unknown")
        self.assertEqual(res_7, "Unknown")



if __name__ == '__main__':
    unittest.main()