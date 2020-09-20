import tkinter as tk
from tkinter import ttk

from invoice_gui.data_model import StorageModel
from invoice_gui.data_model import AddressModel
from invoice_gui.frame_invoice import InvoiceFrame


class TopLevelMenu(tk.Menu):

    def __init__(self, master):
        super(TopLevelMenu, self).__init__(master=master)
        self.init_ui()

    def init_ui(self):

        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Settings")

        self.add_cascade(label="File", menu=file_menu)



if __name__ == '__main__':

    root = tk.Tk()
    root.title("Invoice Generator")

    debtor_address_model = AddressModel()
    creditor_address_model = AddressModel()

    storage_model = StorageModel()

    tab_controller = ttk.Notebook(root)

    invoice_tab = InvoiceFrame(tab_controller, debtor_address_model, storage_model=storage_model)
    tab_controller.add(invoice_tab, text="Invoice")

    menubar = TopLevelMenu(root)
    root.config(menu=menubar)

    tab_controller.pack(expand=1, fill="both")

    root.mainloop()