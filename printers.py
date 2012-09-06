import gdb
import re

class BoostSharedPtrPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        val = self.val['px']
        try:
            result = str(val.dereference())
        except RuntimeError:
            result = "Cannot access memory at address " + str(val.address)
        return '%s' % result

def BuildPrinter():
    printer = gdb.printing.RegexpCollectionPrettyPrinter("custom")
    printer.add_printer('boost:shared_ptr', '^boost::shared_ptr<.*>$', BoostSharedPtrPrinter)
    return printer
