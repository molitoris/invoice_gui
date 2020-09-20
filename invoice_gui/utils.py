import tkinter as tk

from invoice_gui.errors import SpecialVarException


class PlaceholderEntry(tk.Entry):
    """ The class is a special Entry which allows to set a placeholder.

    The placeholder is removed, when the user sets the focus on the entry. When the entry looses focus and does not
    has content, the placeholder is set again.
    """

    def __init__(self, master, placeholder, textvariable, color="grey", *args, **kwargs):
        super(PlaceholderEntry, self).__init__(master=master, *args, textvariable=textvariable, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.textvariable = textvariable

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        """ Insert placeholder into variable

        :return:
        """
        self.textvariable.set(self.placeholder)
        self.textvariable.is_placeholder = True  # has to be after set function
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self.textvariable.is_placeholder:
            self.textvariable.set("")
            self['fg'] = self.default_fg_color
            self.textvariable.is_placeholder = False

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def VariableCls(base_cls, *args, **kwargs):
    """ Return instance of SpecialVar which inherits from base_cls, initialized with given parameters"""

    class SpecialVar(base_cls):

        def __init__(self, mandatory=True, *args, **kwargs):
            super(SpecialVar, self).__init__(*args, **kwargs)

            self.is_placeholder = False
            self.is_mandatory = mandatory

        def get(self):
            if self.is_placeholder:
                return None

            return super(SpecialVar, self).get()

        def set(self, value):
            self.is_placeholder = False
            super(SpecialVar, self).set(value)

        def validate(self):
            return not (self.is_mandatory and self.is_placeholder)

    return SpecialVar(*args, **kwargs)


class ProxyVar(tk.StringVar):
    """Special variable class for Option Menu with name/value pairs"""

    def __init__(self, proxy, *args, **kwargs):
        super(ProxyVar, self).__init__(*args, **kwargs)

        self.proxy = proxy

        self.set(next(iter(self.proxy.keys())))

    def get(self):
        return super(ProxyVar, self).get()

    def set(self, value):
        if value not in self.proxy.keys():
            raise ValueError(f"{value} is not in list of proxy ({self.proxy})")

        super(ProxyVar, self).set(value)

    def get_keys(self):
        return list(self.proxy.keys())

    def get_value(self):
        return self.proxy[super(ProxyVar, self).get()]

    def set_value(self, proxy):
        super(ProxyVar, self).set(proxy)
