import gettext
import os
from threading import Thread

import tkinter as tk
from tkinter import messagebox
import datetime
from pathlib import Path

import yaml
from importlib_resources import files

from qr_payment_slip import QRPaymentSlip, Address as QRAddress, SVGPrinter
from invoice import InvoiceGenerator, Address, Fee, Expense
from qr_payment_slip.printer import PDFPrinter

from invoice_gui.data_model import CostModel, PaymentInformationModel, ExtendedAddressModel, AccountModel
from invoice_gui.errors import ValidationException
from invoice_gui.frames import AddressFrame, FeeFrame, ExpensesFrame, StorageFrame, PaymentInformationFrame
from invoice_gui import config


class InvoiceFrame(tk.Frame):
    """Frame which collects all information need to create the invoice and the payment slip"""

    def __init__(self, master, debtor_address_model, storage_model):
        """

        :param master:
        :param debtor_address_model:
        :param storage_model:
        """
        super(InvoiceFrame, self).__init__(master=master)

        self.debtor_address_model = debtor_address_model
        self.storage_model = storage_model

        self.account = AccountModel()
        self.creditor = ExtendedAddressModel()

        self.fees_model = CostModel()
        self.expenses_model = CostModel()
        self.payment_info_model = PaymentInformationModel()

        self._load_creditor_config()

        self.init_ui()

        # Load the creditor and its account from environment variables
        # self.creditor, self.creditor_account = self._load_env_creditor()

    def init_ui(self):
        debtor_gui = AddressFrame(self, padx=5, pady=3, address_model=self.debtor_address_model)
        debtor_gui.pack(fill="x", padx=15, pady=5)

        fee_frame = FeeFrame(self, padx=5, pady=3, fees_model=self.fees_model)
        fee_frame.pack(padx=15, pady=5, fill="x")

        expenses_frame = ExpensesFrame(self, expenses_model=self.expenses_model, padx=5, pady=3)
        expenses_frame.pack(padx=15, pady=5, fill="x")

        payment_slip_frame = PaymentInformationFrame(self, payment_info_model=self.payment_info_model, padx=5, pady=3)
        payment_slip_frame.pack(padx=10, pady=5, fill="x")

        storage_frame = StorageFrame(self, padx=5, pady=3, storage_model=self.storage_model)
        storage_frame.pack(padx=15, pady=5, fill="x")

        btn_invoice = tk.Button(self, text="Create",  command=self.create_invoice)
        btn_invoice.pack(padx=20, pady=20, side=tk.RIGHT)

    def _load_creditor_config(self, path=files(config).joinpath("config.yaml")):
        with open(path, "r", encoding="utf8") as file:
            config_data = yaml.safe_load(file)

            creditor_config = config_data["creditor"]
            storage_config = config_data["storage"]

            self.account.account.set(creditor_config["account"])
            self.creditor.is_male.set("Male" if creditor_config["is_male"] else "Female")
            self.creditor.firstname.set(creditor_config["firstname"])
            self.creditor.lastname.set(creditor_config["lastname"])
            self.creditor.address_line_1.set(creditor_config["address_line_1"])
            self.creditor.address_line_2.set(creditor_config["address_line_2"])
            self.creditor.phone.set(creditor_config["phone"])
            self.creditor.pcode.set(creditor_config["pcode"])
            self.creditor.town.set(creditor_config["town"])

            self.storage_model.storage.set(storage_config["path"])

    # def _load_env_creditor(self):
    #     """Load creditor and its account from environmental variable"""

    # env_vars = {
    #     "account": "creditor_account",
    #     "is_male": "creditor_is_male",
    #     "firstname": "creditor_firstname",
    #     "lastname": "creditor_lastname",
    #     "address_line_1": "creditor_address_line_1",
    #     "address_line_2": "creditor_address_line_2",
    #     "phone": "creditor_phone",
    #     "pcode": "creditor_pcode",
    #     "town": "creditor_town"
    # }

    # account = AccountModel()
    # creditor = ExtendedAddressModel()

    # for name, env_var in env_vars.items():

    # val = os.environ[env_var]

    # if name in ["account"]:
    #     account.__getattribute__(name).set(val)
    # else:
    #     creditor.__getattribute__(name).set(val)

    # return creditor, account

    def create_invoice(self, *args):

        try:
            self.debtor_address_model.validate()
            self.creditor.validate()
            for fee in self.fees_model.costs:
                fee.validate()
        except ValidationException as e:
            messagebox.showwarning(title="Validation Exception", message=str(e))
            return False

        # Information to generate the invoice
        inv_debtor = Address(**self.debtor_address_model.as_invoice_format())
        inv_creditor = Address(**self.creditor.as_invoice_format())

        # Information to generate the QR payment slip
        qps_debtor = QRAddress(**self.debtor_address_model.as_payment_slip_format())
        qps_creditor = QRAddress(**self.creditor.as_payment_slip_format())
        qr_info = ""

        fees = [Fee(**fee.as_dict()) for fee in self.fees_model.costs if self.fees_model.costs]
        expenses = [Expense(**expense.as_dict()) for expense in self.expenses_model.costs if self.expenses_model.costs]

        # Information to store the documents
        destination_dir = self.storage_model.storage.get().replace(" ", r"\ ")

        timestamp = datetime.datetime.now().strftime("%y%m%d")
        output_name = f"{timestamp}_{inv_debtor.lastname.replace(' ', '_')}_{inv_debtor.firstname.replace(' ', '_')}"

        # Generate output directory if it does not exist
        output_dir = Path(destination_dir, output_name)
        output_dir.mkdir(parents=True, exist_ok=True)

        total_costs = sum([fee.total_costs for fee in fees]) + sum([expense.total_costs for expense in expenses])

        # Create QR payment slip
        payment_slip = QRPaymentSlip(
            account=self.account.account.get(),
            creditor=qps_creditor,
            debtor=qps_debtor,
            unstructured_message=self.payment_info_model.unstructured_message.get(),
            amount=total_costs,
            printer=PDFPrinter()
        )

        qps_output_file = Path(output_dir, output_name + "_qr_slip.pdf")  # TODO: Change to pdf
        qps_thread = CustomThread(payment_slip.save_as, file_name=qps_output_file)

        # Create the invoice
        def create_invoice():

            invoice = InvoiceGenerator()
            invoice_tex = invoice.fill_template(biller=inv_creditor, receiver=inv_debtor, fees=fees, expenses=expenses)

            inv_output_tex_file = Path(output_dir, output_name + ".tex")

            with open(inv_output_tex_file, "w+b") as file:
                file.write(invoice_tex.encode("utf-8"))

            os.system(f"pdflatex -output-directory={output_dir} -jobname={output_name} {inv_output_tex_file}")

        inv_thread = CustomThread(create_invoice)

        # Start both threads
        qps_thread.start()
        inv_thread.start()


class CustomThread(Thread):

    def __init__(self, fun, *args, **kwargs):
        super(CustomThread, self).__init__()

        self.fun = fun
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.fun(*self.args, **self.kwargs)
