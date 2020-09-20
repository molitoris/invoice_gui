import tkinter as tk
import tkinter.font as tk_font
from tkinter import filedialog

from invoice_gui.data_model import FeeModel, ExpenseModel
from invoice_gui.utils import PlaceholderEntry


class AddressFrame(tk.Frame):

    def __init__(self, master, address_model, *args, title="Debtor", lbl_padx=10, lbl_pady=3, ent_padx=5, ent_pady=7,
                 **kwargs):
        """

        :param master:
        :param address_model:
        :param args:
        :param title:
        :param lbl_padx:
        :param lbl_pady:
        :param ent_padx:
        :param ent_pady:
        :param kwargs:
        """
        super(AddressFrame, self).__init__(master=master, *args, **kwargs)

        self.title = title

        self.lbl_padx = lbl_padx
        self.lbl_pady = lbl_pady
        self.ent_padx = ent_padx
        self.ent_pady = ent_pady

        self.address_model = address_model

        self.init_ui()

    def get_data(self, *args, **kwargs):
        pass

    def init_ui(self):
        title_font = tk_font.Font(family="Helvetica", size=12)

        tk.Label(self, text=self.title, font=title_font).grid(sticky=tk.W, pady=10)

        tk.Label(self, text="Gender").grid(column=0, sticky=tk.E, pady=self.lbl_pady, padx=self.lbl_padx)

        tk.OptionMenu(self, self.address_model.is_male, *self.address_model.is_male.get_keys())\
            .grid(row=1, column=1, sticky="ew")

        # Name
        tk.Label(self, text="Name").grid(column=0, sticky=tk.E, padx=self.lbl_padx, pady=self.lbl_pady)

        PlaceholderEntry(self, placeholder="First name", textvariable=self.address_model.firstname, width=30)\
            .grid(row=2, column=1, sticky=tk.W, padx=self.ent_padx, pady=self.ent_pady)

        PlaceholderEntry(self, placeholder="Last name", textvariable=self.address_model.lastname, width=30)\
            .grid(row=2, column=2, sticky=tk.W, padx=self.ent_padx, pady=self.ent_pady)

        # Address
        tk.Label(self, text="Address").grid(row=3, sticky=tk.E, padx=self.lbl_padx, pady=self.lbl_pady)

        PlaceholderEntry(self, placeholder="Street", textvariable=self.address_model.address_line_1, widt=30)\
            .grid(row=3, column=1, padx=self.ent_padx, pady=self.ent_pady)

        PlaceholderEntry(self, placeholder="No.", textvariable=self.address_model.address_line_2, width=7)\
            .grid(row=3, column=2, sticky=tk.W, padx=self.ent_padx, pady=self.ent_pady)

        PlaceholderEntry(self, placeholder="Postcode", textvariable=self.address_model.pcode, width=30)\
            .grid(row=4, column=1, sticky=tk.W, padx=self.ent_padx, pady=self.ent_pady)

        PlaceholderEntry(self, placeholder="Town", textvariable=self.address_model.town, width=30)\
            .grid(row=4, column=2, padx=self.ent_padx, pady=self.ent_pady)

        tk.OptionMenu(self, self.address_model.country, *self.address_model.country.get_keys())\
            .grid(row=5, column=2, sticky="ew")


class FeeFrame(tk.Frame):

    def __init__(self, master, fees_model, *args, lbl_padx=10, ent_padx=5, ent_pady=7, **kwargs):
        super(FeeFrame, self).__init__(master=master, *args, **kwargs)

        self.fees_model = fees_model

        self.lbl_padx = lbl_padx
        self.ent_padx = ent_padx
        self.ent_pady = ent_pady

        self.fee_widgets = []

        self.init_ui()

    def init_ui(self):

        title_font = tk_font.Font(family="Helvetica", size=12)

        tk.Label(self, text="Fees", font=title_font).grid(sticky=tk.W, pady=10)

        tk.Label(self, text="Activity", anchor=tk.W).grid(row=1, column=0, sticky="w", padx=10)

        tk.Label(self, text="Unit", anchor=tk.W).grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(self, text="Price/Unit", anchor=tk.W).grid(row=1, column=2, padx=10, sticky=tk.W)

        tk.Button(self, text="+", padx=8, command=self.add_fee).grid(row=1, column=3, sticky="ew")

        self.add_fee()

    def add_fee(self, *args):
        """Add a new row in the grid"""

        _, row = self.grid_size()
        fee_model = FeeModel()

        ent_description = PlaceholderEntry(self, placeholder="Description", textvariable=fee_model.description)
        ent_description.grid(row=row, column=0, sticky="ew", padx=10, pady=self.ent_pady)
        ent_description.grid_columnconfigure(index=0, weight=2)

        ent_unit = PlaceholderEntry(self, placeholder=1, textvariable=fee_model.unit)
        ent_unit.grid(row=row, column=1, padx=10, pady=self.ent_pady, sticky="ew")

        ent_price = PlaceholderEntry(self, placeholder=100.0, textvariable=fee_model.price)
        ent_price.grid(row=row, column=2, padx=10, pady=self.ent_pady, sticky="ew")

        btn_remove = tk.Button(self, text="-", padx=8,
                               command=lambda eff, index=row-2: self.remove_fee(eff, index=index))
        btn_remove.grid(row=row, column=3, sticky="ew")

        self.fee_widgets.append((ent_description, ent_unit, ent_price, btn_remove))
        self.fees_model.costs.append(fee_model)

    def remove_fee(self, *args, index):
        """Remove a row in the grid and update binding of all buttons which were above the removed row"""

        fee_row = self.fee_widgets.pop(index)
        self.fees_model.costs.pop(index)

        for item in fee_row:
            item.destroy()

        for i, fee in enumerate(self.fee_widgets):
            if i >= index:
                fee[3].bind("<Button-1>", lambda eff, index=i: self.remove_fee(eff, index=index))


class ExpensesFrame(tk.Frame):

    def __init__(self, master, expenses_model, *args, lbl_padx=10, ent_padx=5, ent_pady=7, **kwargs):
        super(ExpensesFrame, self).__init__(master=master, *args, **kwargs)

        self.expenses_model = expenses_model

        self.lbl_padx = lbl_padx
        self.ent_padx = ent_padx
        self.ent_pady = ent_pady

        self.expenses = []

        self.nrow = 1  # add next fee in this row

        self.init_ui()

    def init_ui(self, *args):
        self.grid_columnconfigure(0, weight=1)  # as did this

        title_font = tk_font.Font(family="Helvetica", size=12)

        tk.Label(self, text="Expenses", font=title_font).grid(sticky=tk.W, pady=10)

        tk.Label(self, text="Activity", anchor=tk.W).grid(row=1, column=0, sticky="w", padx=10)

        tk.Label(self, text="Price", anchor=tk.W).grid(row=1, column=1, padx=10, sticky=tk.W)

        tk.Button(self, text="+", padx=8, command=self.add_expenses).grid(row=1, column=2, sticky="ew")

    def add_expenses(self, *args):
        """Add a new row in the grid"""

        _, row = self.grid_size()
        expense_model = ExpenseModel()

        ent_description = PlaceholderEntry(self, placeholder="Description", textvariable=expense_model.description)
        ent_description.grid(row=row, column=0, sticky="ew", padx=10, pady=self.ent_pady)

        ent_price = PlaceholderEntry(self, placeholder=100.0, textvariable=expense_model.price)
        ent_price.grid(row=row, column=1, padx=10, pady=self.ent_pady, sticky="ew")

        btn_remove = tk.Button(self, text="-", padx=8,
                               command=lambda eff, index=row - 2: self.remove_expenses(eff, index=index))
        btn_remove.grid(row=row, column=2, sticky="ew")

        self.expenses.append((ent_description, ent_price, btn_remove))
        self.expenses_model.costs.append(expense_model)

    def remove_expenses(self, *args, index):
        """Remove a row in the grid and update binding of all buttons which were above the removed row"""
        expense_row = self.expenses.pop(index)
        self.expenses_model.costs.pop(index)

        for item in expense_row:
            item.destroy()

        for i, fee in enumerate(self.expenses):
            if i >= index:
                fee[2].bind("<Button-1>", lambda eff, index=i: self.remove_expenses(eff, index=index))


class PaymentInformationFrame(tk.Frame):

    def __init__(self, master, payment_info_model, *args, lbl_padx=10, lbl_pady=3, ent_padx=5, ent_pady=7, **kwargs):
        super(PaymentInformationFrame, self).__init__(master=master, *args, **kwargs)

        self.model = payment_info_model

        self.lbl_padx = lbl_padx
        self.lbl_pady = lbl_pady
        self.ent_padx = ent_padx
        self.ent_pady = ent_pady

        self.init_ui()

    def init_ui(self):
        title_font = tk_font.Font(family="Helvetica", size=12)

        tk.Label(self, text="Payment Slip Information", font=title_font).grid(sticky=tk.W, pady=10)

        tk.Label(self, text="Ref No.").grid(column=0, sticky=tk.E, pady=self.lbl_pady)

        PlaceholderEntry(self, placeholder="Ref No.", width=30, textvariable=self.model.reference_no)\
            .grid(row=1, column=1, sticky=tk.W, padx=self.ent_padx, pady=self.ent_pady)

        tk.Label(self, text="Unstructured Message").grid(row=2, column=0, sticky=tk.E, pady=self.lbl_pady)

        PlaceholderEntry(self, placeholder="Unstructured Message", width=30,
                         textvariable=self.model.unstructured_message)\
            .grid(row=2, column=1, sticky=tk.W, padx=self.ent_padx, pady=self.ent_pady)

        tk.Label(self, text="Billing Information").grid(row=3, column=0, sticky=tk.E, pady=self.lbl_pady)

        PlaceholderEntry(self, placeholder="Billing information", width=30,
                         textvariable=self.model.billing_information)\
            .grid(row=3, column=1, sticky=tk.W, padx=self.ent_padx, pady=self.ent_pady)


class StorageFrame(tk.Frame):

    def __init__(self, master, storage_model, *args, **kwargs):
        super(StorageFrame, self).__init__(master=master, *args, **kwargs)

        self.storage_model = storage_model

        self.init_ui()

    def init_ui(self, *args):

        self.grid_rowconfigure(0, weight=1)  # this needed to be added
        self.grid_columnconfigure(0, weight=1)  # as did this

        title_font = tk_font.Font(family="Helvetica", size=12)

        tk.Label(self, text="Storage", font=title_font).grid(sticky=tk.W, pady=10)

        tk.Entry(self, textvariable=self.storage_model.storage, width=50).grid(row=1, column=0, sticky="ew", padx=10)

        tk.Button(self, text="Browse...", padx=8, command=self.select_dir).grid(row=1, column=1, sticky="ew")

    def select_dir(self, *args):

        if self.storage_model.storage.get() != "":
            directory = filedialog.askdirectory(master=self, initialdir=self.storage_model.storage.get())
        else:
            directory = filedialog.askdirectory(master=self)

        if directory != "":
            self.storage_model.storage.set(directory)
