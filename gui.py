import gtk
import gdb
import os

OK_CODE = 1
CANCEL_CODE = 2

def end_match(completion, entrystr, iter, data):
    modelstr = completion.get_model()[iter][0]
    return entrystr in modelstr

class MyWindow(gtk.Window):
    def init(self, g):
      self.g = g

    def on_button_clicked(self, widget):
        print "Hello World"

    def __init__(self):
        gtk.Window.__init__(self)

        self.menu_bar = gtk.MenuBar()
        self.build_menu()
        self.build_dialogs()

        table = gtk.Table(4, 2, True)
        table.attach(self.menu_bar, 0, 2, 0, 1)
        scrolled_window = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)

        textview = gtk.TextView(buffer=None)
        textview.set_editable(False)

        self.textbuffer = textview.get_buffer()

        scrolled_window.add_with_viewport(textview)
        # Left-attach, right, top, bottom
        table.attach(scrolled_window, 0, 2, 1, 2)

        self.button = gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        table.attach(self.button, 0, 1, 2, 3)

        self.label = gtk.Label()
        self.label.set_text("This is a left-justified label.\nWith multiple lines.")
        table.attach(self.label, 0, 2, 3, 4)

        self.add(table)

    def match_cb(self, completion, model, iter):
        print model[iter][0], 'was selected'

    def handle_menu_file_open(self, widget, string):
        mydata = self.g.execute("info sources", False, True)

        self.liststore.clear()
        for l in mydata.split('\n'):
          if len(l) == 0 or l[-1] == ':':
            continue
          for sl in l.split(','):
            self.liststore.append([sl.strip()])

        self.completion.set_model(self.liststore)

        response = self.open_source_dialog.run()

        if response == OK_CODE:
            filename = self.entry.get_text()
            with open(filename) as f:
                self.textbuffer.set_text(f.read())

        self.open_source_dialog.hide()

    def build_menu(self):
        menu = gtk.Menu()

        sub_item = gtk.MenuItem("Open")
        sub_item.connect("activate", self.handle_menu_file_open, "Open")
        menu.append(sub_item)

        root_menu = gtk.MenuItem("File")
        root_menu.set_submenu(menu)

        root_menu.show()

        self.menu_bar.append(root_menu)

    def build_dialogs(self):
        self.open_source_dialog = gtk.Dialog(
            title='Open Source',
            parent=None,
            flags=0,
            buttons=('OK', OK_CODE, 'Cancel', CANCEL_CODE))

        self.entry = gtk.Entry()
        self.completion = gtk.EntryCompletion()
        self.liststore = gtk.ListStore(str)
        for s in ['apple']:
            self.liststore.append([s])
        self.completion.set_model(self.liststore)
        self.entry.set_completion(self.completion)
        self.completion.set_text_column(0)
        self.completion.set_minimum_key_length(3)
        self.completion.set_match_func(end_match, None)
        self.entry.show()

        self.open_source_dialog.vbox.pack_start(self.entry, True, True, 0)
