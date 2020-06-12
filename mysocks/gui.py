from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
import re
import time
from mysocks import __version__, __author__, __email__
from mysocks import chat
import threading    # threading library is used to create separate threads for every clients connected
import sys
import ctypes

class launch():
    """This class is a parent class for all tkinter gui related tasks
        Call this class to get an object of launch class to start a tkinter gui.
        Filemenu options can be used to start a chatroom server or a client

    :param kwargs **kwargs: `**kwargs`.
    :attr type launch_gui: Function module to start gui

    """


    def __init__(self, **kwargs):
        """Constructor for class launch

        :param kwargs **kwargs: `**kwargs`.
        :return: launch class object
        :rtype: launch class object

        """

        print('hello')
        # Parameters
        self._about_win_state = False   # True: About window is active. # False: about windows not active
        self._server_state = False  # True: server created. False: server closed or not created yet
        self._connected_as_client = False  # True: connected as client. False: not connected to any server

        self.isCalledFromServer = kwargs.get('isCalledFromServer', False)
        if self.isCalledFromServer == False:
            self.launch_gui(**kwargs)


    def submit(self, event=None):
        if self.u_name_state == False:
            self.u_name = self.message_box.get("1.0", 'end-1c')
            self.message_box.delete(1.0, END)
            print('Username is set as ' + str(self.u_name))
            self.u_name_state = True
            self._client_chat.set_username(username = self.u_name)
            self.group1.configure(text = 'Type your message here?')
            self.master_window.title('Connected to server as ' + str(self.u_name))
        
        else:
            message = self.message_box.get("1.0", 'end-1c')
            time.sleep(0.1)
            self.message_box.delete(1.0, END)
            print(message)
            self._client_chat.send_data(message = message)
            print('test')
        return 'break'




    def _about_win(self):
        if self._about_win_state == False:
             win = tk.Toplevel()
             self._about_win = win
             self._about_win_state = True
             win.title("About")
             about = '''mysocks package - version ''' + __version__ + '''\nAuthor: ''' + __author__ + '''\nEmail: ''' + __email__
             about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
             t=CustomText(win, wrap="word", width=100, height=10, borderwidth=0)
             t.tag_configure("blue", foreground="blue")
             t.pack(sid="top",fill="both",expand=True)
             t.insert("1.0", about)
             t.HighlightPattern("^.*? - ", "blue")
             ok_btn = tk.Button(win, text='OK', command = self._close_about_win)
             ok_btn.pack()
             t.config(state = DISABLED)
             win.protocol('WM_DELETE_WINDOW', self._close_about_win)
        self._about_win.lift()

    def _close_about_win(self):
        self._about_win_state = False
        self._about_win.destroy()

    def launch_gui(self, **kwargs):


        self.master_window = Tk()
        self.title_master_window = kwargs.get('title', 'mysocks Chatroom')  # title to master window
        self.master_window.title(self.title_master_window)

        self.menu = Menu(self.master_window)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label = 'New')
        self.filemenu.add_command(label = 'Start Chatroom', command = self.start_server)
        self.filemenu.add_command(label = 'Connect to Chatroom', command = self.start_client)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = 'Exit', command = self._exit_gui)


        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label = 'Help', menu=self.helpmenu)
        self.helpmenu.add_command(label = 'About', command = self._about_win)

        # scrollbar = Scrollbar(group2)
        # scrollbar.pack(side = RIGHT, fill = Y )

        # Group1 Frame ----------------------------------------------------
        self.group1 = LabelFrame(self.master_window, text = 'Type your message here', padx=5, pady=5)
        self.group1.grid(row=0, column=0, columnspan=3, padx=10, sticky=E+W+N+S)

        self.message_box = Text(self.group1, height = 2)
        # message_box.pack(side = LEFT, fill = BOTH)
        self.message_box.grid(row = 0, column = 0, columnspan = 2, pady=10, sticky = E+W+N+S)


        self.btn_File = Button(self.group1, text='Send', command=self.submit)
        self.btn_File.grid(row=0, column=2, padx=(10), pady=10, sticky=E+W+N+S)

        self.message_box.bind('<Return>', self.submit)

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
        self.master_window.protocol('WM_DELETE_WINDOW', self._exit_gui)
        self.master_window.mainloop()

    def Text_insert(self):
        if self._server_state == True:
            try:
                while not self._server_chat.message_queue.empty():
                    self.txtbox.insert(END, self._server_chat.message_queue.get() + '\n')
                    self.txtbox.see("end")
            except:
                pass
        elif self._connected_as_client == True:
            try:
                while not self._client_chat.message_queue.empty():
                    self.txtbox.insert(END, self._client_chat.message_queue.get() + '\n')
                    self.txtbox.see("end")
            except:
                pass
        self.master_window.after(1000, self.Text_insert)

    def start_server(self):
        try:
            if self._server_state == False:
                self._server_state = True
                self._server_chat = chat.server(isCalledFromGUI = True)
                self.server_chat_thread = threading.Thread(target = self._server_chat.start_server, args = ('127.0.0.1', 5660, 5))
                self.server_chat_thread.daemon = True
                self.server_chat_thread.start()
                time.sleep(0.5)
                if self._server_chat._server_running == True:   # true : In case a server is running
                    self._server_state = True                 # server is running at the same specified IP and port
                else:
                    self._server_state = False                # In case a server is running but was not started from this gui
            else:
                print('Server already running')
        except Exception as e:
            print(e)
            print('Unable to start a new server.')

    def start_client(self):
        try:
            if self._server_state == False:             # If server is running then chat is not allowed to start
                if self._connected_as_client == False:
                    self._client_chat = chat.client(isCalledFromGUI = True)
                    self.client_chat_thread = threading.Thread(target = self._client_chat.start_client, args = ('127.0.0.1', 5660))
                    self.client_chat_thread.daemon = True
                    self.client_chat_thread.start()
                    time.sleep(3)
                    print(self._client_chat._connected_as_client)
                    if self._client_chat._connected_as_client == True:
                        self._connected_as_client = True
                        self.group1.configure(text = 'Your Username?')
                        self.u_name_state = False            # True: Username of a client is set. False: username is yet to be set
                    else:
                        print('Client could not be connected')
                else:
                    print('Client already connected')
            else:
                print('Server is running in the same window. Client cannot be connected.\nPlease start a new GUI window')
        except Exception as e:
            print(e)
            print('Unable to connect to server')

    def _exit_gui(self):
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
