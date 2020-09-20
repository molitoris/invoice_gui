import unittest
import tkinter as tk

from invoice_gui.data_model import FeeModel


class FeeModelTestCase(unittest.TestCase):

    def setUp(self) -> None:
        root = tk.Tk()

    def test_fees(self):
        fee = FeeModel()

        fee.description.set("Simple setup")
        fee.price.set(100)
        fee.unit.set(1)

        self.assertEqual(fee.total_cost, 100*1)
        self.assertDictEqual(fee.as_dict(), {"description": "Simple setup", "price": 100, "unit": 1})


if __name__ == '__main__':
    unittest.main()
