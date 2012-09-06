#!/usr/bin/env python

import gtk

OK_CODE = 1
CANCEL_CODE = 2

class MyWindow(gtk.Window):

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

    def on_button_clicked(self, widget):
        self.textbuffer.set_text("asdf")
        print "Hello World"

    def handle_menu_file_open(self, widget, string):
        response = self.open_source_dialog.run()

        if response == OK_CODE:
            self.open_source_dialog.hide()
            self.textbuffer = textview.get_buffer()
        elif response == CANCEL_CODE:
            self.open_source_dialog.hide()
        else:
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
            buttons=('OK', 1, 'Cancel', 2))

        entry = gtk.Entry()
        completion = gtk.EntryCompletion()
        self.liststore = gtk.ListStore(str)
        for s in ['apple']:
            self.liststore.append([s])
        completion.set_model(self.liststore)
        entry.set_completion(completion)
        completion.set_text_column(0)
        entry.show()

        self.open_source_dialog.vbox.pack_start(entry, True, True, 0)

win = MyWindow()
win.connect("delete-event", gtk.main_quit)
win.show_all()
gtk.main()
