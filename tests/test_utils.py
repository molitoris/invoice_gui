import unittest
import tkinter as tk

from invoice_gui.utils import ProxyVar, VariableCls


class ProxyVarTestCase(unittest.TestCase):

    def setUp(self) -> None:
        tk.Tk()

    def test_proxy_var(self):

        content = {"Apple": "apple", "Cherry": "cherry"}

        my_var = ProxyVar(proxy=content)

        self.assertEqual(my_var.get(), "Apple")
        self.assertEqual(my_var.get_value(), "apple")

        my_var.set("Cherry")

        self.assertEqual(my_var.get(), "Cherry")
        self.assertEqual(my_var.get_value(), "cherry")

        with self.assertRaises(ValueError):
            my_var.set("Banana")


class SpecialVarClassTestCase(unittest.TestCase):

    def setUp(self) -> None:
        tk.Tk()

    def test_string_var(self):

        string_var = VariableCls(tk.StringVar)

        self.assertFalse(string_var.is_placeholder)
        self.assertTrue(string_var.is_mandatory)

        string_var.set("name")

        self.assertFalse(string_var.is_placeholder)
        self.assertEqual(string_var.get(), "name")

        self.assertTrue(string_var.validate())

    def test_string_var_placeholder(self):

        string_var = VariableCls(tk.StringVar)

        string_var.is_placeholder = True
        self.assertTrue(string_var.is_placeholder)

        self.assertFalse(string_var.validate())

    def test_string_var_optional(self):
        string_var = VariableCls(tk.StringVar, mandatory=False)

        self.assertFalse(string_var.is_placeholder)
        self.assertFalse(string_var.is_mandatory)

        self.assertTrue(string_var.validate())










if __name__ == '__main__':
    unittest.main()
