import gdb

class CallerIs (gdb.Function):
    """Return True if the calling function's name is equal to a string.
This function takes one or two arguments.
The first argument is the name of a function; if the calling function's
name is equal to this argument, this function returns True.
The optional second argument tells this function how many stack frames
to traverse to find the calling function.  The default is 1.
Usage: break *FunctionName* if $caller_is("main")"""

    def __init__ (self):
        super (CallerIs, self).__init__ ("caller_is")

    def invoke (self, name, nframes = 1):
        frame = gdb.get_current_frame ()
        while nframes > 0:
            frame = frame.get_prev ()
            nframes = nframes - 1
        return frame.get_name () == name.string ()

class _LPrintfBreakpoint(gdb.Breakpoint):
    def __init__(self, spec, command):
        super(_LPrintfBreakpoint, self).__init__(spec, gdb.BP_BREAKPOINT,
                                                 internal = False)
        self.command = command

    def stop(self):
        gdb.execute(self.command)
        return False

class _LPrintfCommand(gdb.Command):
    """Log some expressions at a location, using 'printf'.
    Usage: lprintf test.cc:6, "%s", "Hit\n"
    Insert a breakpoint at the location given by LINESPEC.
    When the breakpoint is hit, do not stop, but instead pass
    the remaining arguments to 'printf' and continue.
    This can be used to easily add dynamic logging to a program
    without interfering with normal debugger operation."""

    def __init__(self):
        super(_LPrintfCommand, self).__init__('lprintf',
                                              gdb.COMMAND_DATA,
                                              # Not really the correct
                                              # completer, but ok-ish.
                                              gdb.COMPLETE_SYMBOL)

    def invoke(self, arg, from_tty):
        (remaining, locations) = gdb.decode_line(arg)
        if remaining is None:
            raise gdb.GdbError('printf format missing')
        remaining = remaining.strip(',')
        if locations is None:
            raise gdb.GdbError('no matching locations found')

        spec = arg[0:- len(remaining)]
        _LPrintfBreakpoint(spec, 'printf ' + remaining)

_LPrintfCommand()
CallerIs()

