import gdb
import gdb.printing
import printers
import utils

import pyspect

# Try to use the new-style pretty-printing if available.
_use_gdb_pp = True
try:
    import gdb.printing
except ImportError:
    _use_gdb_pp = False

obj = gdb.current_objfile()

if _use_gdb_pp:
    gdb.printing.register_pretty_printer(obj, printers.BuildPrinter())
else:
    if obj is None:
        obj = gdb
    obj.pretty_printers.append(printers.BuildPrinter())
