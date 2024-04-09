import unittest

import customer_frontend

class TestCustomerFrontend(unittest.TestCase):
    def setUp(self) -> None:
        meal_price_index_1 = {
            "" : 5,
            "" : 3,
            "" : 100
        }
        meal_price_index_2 = {
            "" : 0
        }
        meal_price_index_3 = {
            "" : 0,
            "" : 90,
            "ogkjiugyfcxdcghugf" : 12387659801,
            "a" : 0xDEADBEEF,
            "-!" : 11111
        }
        
        self.menu_1 = customer_frontend.GuiApp(meal_price_index_1)
        self.menu_2 = customer_frontend.GuiApp(meal_price_index_2)
        self.menu_3 = customer_frontend.GuiApp(meal_price_index_3)
        return super().setUp()
    
    def test_calculate_total(self):
        self.assertEqual(self.menu_1.calculate_total(), 108)
        self.assertEqual(self.menu_2.calculate_total(), 0)
        self.assertEqual(self.menu_3.calculate_total(), 16123599561)
    
    def test_getters(self):
        self.assertEqual(self.menu_1.get_entry("afsdsaafds"), None)
        self.assertEqual(self.menu_2.get_textbox("jhghfhj"), None)
        self.assertEqual(self.menu_3.get_button("bb_tt"), None)
    
    def test_is_proper_name(self):
        self.assertTrue(self.menu_1.is_proper_name("John Doe"))
        self.assertFalse(self.menu_2.is_proper_name("john doe"))
        self.assertFalse(self.menu_2.is_proper_name("hgxffdghjkl"))

if __name__ == "__main__":
    unittest.main()