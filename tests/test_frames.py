import unittest
import tkinter as tk

from invoice_gui.data_model import CostModel
from invoice_gui.frames import FeeFrame


class MyTestCase(unittest.TestCase):

    def test_debtor_frame(self):

        root = tk.Tk()

        fees_model = CostModel()

        fee_frame = FeeFrame(master=root, fees_model=fees_model)




        print("Hello")


if __name__ == '__main__':
    unittest.main()
