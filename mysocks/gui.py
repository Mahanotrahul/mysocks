from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
import re
from mysocks import chat
import threading    # threading library is used to create separate threads for every clients connected
import sys
import ctypes

class launch():
    """This class is a parent class for all tkinter gui related tasks
        Call this class to start a tkinter gui.
        Filemenu options can be used to start a chatroom server or a client

    :param kwargs **kwargs: `**kwargs`.
    :attr type launch_gui: Function module to start gui

    """


    def __init__(self, **kwargs):

        print('hello')
        # self.launch_gui(**kwargs)

    def hit_return(self, event):
        print("You hit return.")

    def onclick(self, event=None):
        print("You clicked the button")

    def help_win(self):
         win = tk.Toplevel()
         win.title("About")
         about = '''mysocks package - version 1.0.3
         Author: Rahul Mahanot
         Email: thecodeboxed@gmail.com'''
         about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
         t=CustomText(win, wrap="word", width=100, height=10, borderwidth=0)
         t.tag_configure("blue", foreground="blue")
         t.pack(sid="top",fill="both",expand=True)
         t.insert("1.0", about)
         t.HighlightPattern("^.*? - ", "blue")
         tk.Button(win, text='OK', command=win.destroy).pack()

    def launch_gui(self, **kwargs):


        self.master_window = Tk()
        self.title_master_window = kwargs.get('title', 'mysocks Chatroom')
        self.master_window.title(self.title_master_window)

        self.menu = Menu(self.master_window)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label = 'New')
        self.filemenu.add_command(label = 'Start Chatroom', command = self.start_server)
        self.filemenu.add_command(label = 'Connect Chatroom', command = self.start_client)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = 'Exit', command = self.exit_gui)

        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label = 'Help', menu=self.helpmenu)
        self.helpmenu.add_command(label = 'About', command = self.help_win)

        # scrollbar = Scrollbar(group2)
        # scrollbar.pack(side = RIGHT, fill = Y )

        # Group1 Frame ----------------------------------------------------
        self.group1 = LabelFrame(self.master_window, text="Type your message here", padx=5, pady=5)
        self.group1.grid(row=0, column=0, columnspan=3, padx=10, sticky=E+W+N+S)

        self.message_box = Text(self.group1, height = 2)
        # message_box.pack(side = LEFT, fill = BOTH)
        self.message_box.grid(row = 0, column = 0, columnspan = 2, pady=10, sticky = E+W+N+S)


        self.btn_File = Button(self.group1, text='Send', command=self.onclick)
        self.btn_File.grid(row=0, column=2, padx=(10), pady=10, sticky=E+W+N+S)

        self.message_box.bind('<Return>', self.hit_return)

        # Group2 Frame ----------------------------------------------------
        self.group2 = LabelFrame(self.master_window, text="Chat Room", padx=5, pady=5)
        self.group2.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=E+W+N+S)

        self.master_window.columnconfigure(0, weight=1)
        self.master_window.rowconfigure(1, weight=1)

        self.group1.rowconfigure(0, weight=1)
        self.group1.columnconfigure(0, weight=1)

        self.group2.rowconfigure(0, weight=1)
        self.group2.columnconfigure(0, weight=1)
        # Create the textbox
        self.txtbox = scrolledtext.ScrolledText(self.group2, width=40, height=10)
        self.txtbox.grid(row=0, column=0,   sticky=E+W+N+S)

        self.master_window.config(menu=self.menu)
        self.master_window.after(1000, self.Text_insert)
        self.master_window.mainloop()

    def Text_insert(self):
        try:
            while not self._chat.message_queue.empty():
                self.txtbox.insert(END, self._chat.message_queue.get() + '\n')
                self.txtbox.see("end")
            self.master_window.after(1000, self.Text_insert)
        except:
            self.master_window.after(1000, self.Text_insert)

    def start_server(self):
        self._chat = chat.server()
        self.chat_thread = threading.Thread(target = self._chat.start_server, args = ('127.0.0.1', 5660, 5))
        self.chat_thread.daemon = True
        self.chat_thread.start()
        print(self._chat.Id_start)

    def start_client(self):
        self.chat_thread = threading.Thread(target = chat.client)
        self.chat_thread.daemon = True
        self.chat_thread.start()

    def exit_gui(self):
        self.raise_exception()
        # self.chat_thread.join()
        self.master_window.destroy()
        sys.exit()

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self.chat_thread, '_thread_id'):
            return self.chat_thread._thread_id
        for id, thread in threading._active.items():
            if thread is self.chat_thread:
                return id
    def raise_exception(self):
        try:
            thread_id = self.get_id()
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                  ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Exception raise failure')
        except:
            pass

class CustomText(tk.Text):
    '''A text widget with a new method, HighlightPattern

    example:

    text = CustomText()
    text.tag_configure("red",foreground="#ff0000")
    text.HighlightPattern("this should be red", "red")

    The HighlightPattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def HighlightPattern(self, pattern, tag, start="1.0", end="end", regexp=True):
        '''Apply the given tag to all text that matches the given pattern'''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",end)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",count=count, regexp=regexp)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index,count.get()))
            self.tag_add(tag, "matchStart","matchEnd")
