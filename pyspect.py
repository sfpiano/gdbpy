import gdb, threading, Queue, gtk, glib, os, pynotify
import gui

(read_pipe, write_pipe) = os.pipe()

event_queue = Queue.Queue()
main_window = None

def send_to_gtk(func):
    event_queue.put(func)
    os.write(write_pipe, 'x')

def on_stop_event(event):
    global main_window

    #global event_queue
    #global write_pipe
    #event_queue.put((gdb.execute, 'help'))
    #os.write(write_pipe, 'h')

    for bp in event.breakpoints:
        main_window.handle_event(bp.location)
    n = pynotify.Notification('Your program stopped in gdb')
    n.show()

class GtkThread(threading.Thread):
    def handle_queue(self, source, condition):
        global event_queue
        os.read(source, 1)
        items = event_queue.get()
        func = items[0]
        args = items[1:]
        func(*args)

    def run(self):
        global read_pipe
        global main_window
        glib.io_add_watch(read_pipe, glib.IO_IN, self.handle_queue)

        main_window = gui.MyWindow()
        main_window.init(gdb)
        main_window.connect("delete-event", gtk.main_quit)
        main_window.show_all()

        gtk.main()

gdb.events.stop.connect(on_stop_event)

gtk.gdk.threads_init()

pynotify.init('gdb')

t = GtkThread()
t.setDaemon(True)
t.start()
