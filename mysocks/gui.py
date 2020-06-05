from tkinter import *
import tkinter as tk
import re
import mysocks.chat as chat


class launch():


    def __init__(self):

        print('hello')
        self.launch_gui()

    def func(self, event):
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

    def launch_gui(self):
        from tkinter import scrolledtext

        master_window = Tk()
        master_window.title('mysocks Chatroom')

        menu = Menu(master_window)
        filemenu = Menu(menu)
        menu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label = 'New')
        filemenu.add_command(label = 'Open')
        filemenu.add_separator()
        filemenu.add_command(label = 'Exit', command = master_window.destroy)

        helpmenu = Menu(menu)
        menu.add_cascade(label = 'Help', menu=helpmenu)
        helpmenu.add_command(label = 'About', command = self.help_win)

        # scrollbar = Scrollbar(group2)
        # scrollbar.pack(side = RIGHT, fill = Y )

        # Group1 Frame ----------------------------------------------------
        group1 = LabelFrame(master_window, text="Type your message here", padx=5, pady=5)
        group1.grid(row=0, column=0, columnspan=3, padx=10, sticky=E+W+N+S)

        message_box = Text(group1, height = 2)
        # message_box.pack(side = LEFT, fill = BOTH)
        message_box.grid(row = 0, column = 0, columnspan = 2, pady=10, sticky = E+W+N+S)


        btn_File = Button(group1, text='Send', command=self.onclick)
        btn_File.grid(row=0, column=2, padx=(10), pady=10, sticky=E+W+N+S)

        message_box.bind('<Return>', self.func)

        # Group2 Frame ----------------------------------------------------
        group2 = LabelFrame(master_window, text="Chat Room", padx=5, pady=5)
        group2.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=E+W+N+S)

        master_window.columnconfigure(0, weight=1)
        master_window.rowconfigure(1, weight=1)

        group1.rowconfigure(0, weight=1)
        group1.columnconfigure(0, weight=1)

        group2.rowconfigure(0, weight=1)
        group2.columnconfigure(0, weight=1)
        # Create the textbox
        txtbox = scrolledtext.ScrolledText(group2, width=40, height=10)
        txtbox.grid(row=0, column=0,   sticky=E+W+N+S)

        master_window.config(menu=menu)
        mainloop()

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
