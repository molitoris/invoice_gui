import tkinter as tk

from invoice_gui.errors import ValidationException
from invoice_gui.utils import VariableCls, ProxyVar


class BaseModel:

    def validate(self):
        for name, obj in self.__dict__.items():
            if not obj.validate():
                raise ValidationException(f"Variable {name} is required")


class AddressModel(BaseModel):

    def __init__(self):

        self.is_male = VariableCls(ProxyVar, proxy={"Female": False, "Male": True})
        self.firstname = VariableCls(tk.StringVar)
        self.lastname = VariableCls(tk.StringVar)
        self.address_line_1 = VariableCls(tk.StringVar)
        self.address_line_2 = VariableCls(tk.StringVar)
        self.pcode = VariableCls(tk.StringVar)
        self.town = VariableCls(tk.StringVar)
        self.country = VariableCls(ProxyVar, proxy={"Switzerland": "CH"})

    @property
    def name(self):
        return f"{self.firstname.get()} {self.lastname.get()}"

    def as_invoice_format(self):
        return {
            "is_male": self.is_male.get_value(),
            "firstname": self.firstname.get(),
            "lastname": self.lastname.get(),
            "address_line_1": self.address_line_1.get(),
            "address_line_2": self.address_line_2.get(),
            "pcode": self.pcode.get(),
            "town": self.town.get(),
            "country": self.country.get_value()
        }

    def as_payment_slip_format(self):
        output = self.as_invoice_format()
        output.pop("is_male")
        output.pop("firstname")
        output.pop("lastname")
        output["name"] = f"{self.firstname.get()} {self.lastname.get()}"

        return output


class ExtendedAddressModel(AddressModel):

    def __init__(self):
        super(ExtendedAddressModel, self).__init__()

        self.phone = VariableCls(tk.StringVar)

    def as_invoice_format(self):
        output = super(ExtendedAddressModel, self).as_invoice_format()
        output["phone"] = self.phone.get()
        return output

    def as_payment_slip_format(self):
        output = self.as_invoice_format()
        output.pop("is_male")
        output.pop("firstname")
        output.pop("lastname")
        output.pop("phone")
        output["name"] = f"{self.firstname.get()} {self.lastname.get()}"

        return output


class CostModel:

    def __init__(self):

        self.costs = []

    @property
    def total_cost(self):
        return sum(entry.total_costs() for entry in self.costs)

    def validate(self):
        for cost in self.costs:
            cost.validate()


class ExpenseModel(BaseModel):

    def __init__(self):
        self.description = VariableCls(tk.StringVar)
        self.price = VariableCls(tk.DoubleVar)

    @property
    def total_cost(self):
        return self.price.get()

    def as_dict(self):
        return {
            "description": self.description.get(),
            "price": self.price.get()
        }


class FeeModel(ExpenseModel):

    def __init__(self):
        super(FeeModel, self).__init__()
        self.unit = VariableCls(tk.DoubleVar)

    @property
    def total_cost(self):
        return self.unit.get() * self.price.get()

    def as_dict(self):
        return dict(super(FeeModel, self).as_dict(), **{"unit": self.unit.get()})


class StorageModel(BaseModel):

    def __init__(self):
        self.storage = VariableCls(tk.StringVar)


class PaymentInformationModel(BaseModel):

    def __init__(self):
        self.reference_no = VariableCls(tk.StringVar, mandatory=False)
        self.unstructured_message = VariableCls(tk.StringVar, mandatory=False)
        self.billing_information = VariableCls(tk.StringVar, mandatory=False)


class AccountModel:

    def __init__(self):
        self.account = VariableCls(tk.StringVar)
