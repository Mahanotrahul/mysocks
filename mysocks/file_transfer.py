import socket
import inspect
import os
import ntpath
import errno
from tqdm import tqdm
from sockets.utilities import mapcount
import time

from . import Model

class file_transfer(Model):
    """
    This class is parent class to file transfer module.
    """
    def __init__(self, host = '127.0.0.1', port = 5560, n_listen = 1):
        """
        Constructor to start the file transfer process
        """

        super(Model, self).__init__()
        self.s = super().create_socket(host, port, n_listen)

    def accept_connections(self):
        conn, addr = self.s.accept()
        print('Client connected' + str(addr[0]) + ' ' + str(addr[1]))
        return conn, addr



class send_file(Model):
    """
    This class is a parent class for all file sending methods.
    Call this class to send file_send
    """

    def __init__(self, filename, host = '127.0.0.1', port = 5560, n_listen = 1):
        """
        Constructor to start the file transfer process
        """
        if filename == None:
            print('Filename cannot be none')
        elif not os.path.exists(filename):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
        # super(Model, self).__init__()

        self.s = super().create_server_socket(host, port, n_listen)

        self.send_file(filename)

    def accept_connections(self):
        print("Waiting for client to connect")
        conn, addr = self.s.accept()
        print('Client connected at ' + str(addr[0]) + ':' + str(addr[1]))
        return conn, addr

    def lineno():
        """Returns the current line number in our program."""
        return inspect.currentframe().f_back.f_lineno

    def send_file(self, filename):

        # try:
            if 'conn' not in locals():
                conn, addr = self.accept_connections()
            print("Waiting for the client to give confirmation to receive data")
            confirm_time = time.time()
            if time.time() - confirm_time < 10:
                confirm = conn.recv(1024)   ## Receive confirmation from the client. Expected value - '1'
                if confirm.decode('utf-8') == '1':
                    print("Confirmation received.")
                    print("Sending File : " + ntpath.basename(filename))
                    conn.send(str.encode(ntpath.basename(filename)))
                    time.sleep(0.05)
                    file_size = os.path.getsize(filename)

                    conn.send(str.encode(str(file_size)))       ## sends file size as Metadata
                    # conn.send(str.encode('---- File starts ----\n'))
                    f =  open(filename, 'rb')
                    l = f.read(1024)
                    pbar = tqdm(total = int(file_size)//1024)
                    while(l):
                        conn.send(l)
                        l = f.read(1024)
                        pbar.update(1)
                    pbar.close()
                    f.close()
                    print('Done sending')
                    conn.send(str.encode(''))
                    print("Closing Connection")
                    conn.close()
                    self.s.close()
                else:
                    print('Confirmation Not received')
            else:
                print('Wait Timeout')
        # except Exception as e:
        #     print("Error : " + str(e))
        #     print(self.lineno)

class receive_file(Model):
    """
    This class is a parent class for all the procedures related to
    receiving a file.
    """
    def __init__(self, save_path: str = '', host = '127.0.0.1', port = 5560):
        """
        Constructor method for receive_file
        """

        self.s = super().create_client_socket(host, port)
        self.save_path = save_path
        self.receive_file()

    def receive_file(self):
        """
        Method to receive files from the socket server
        """
        self.s.send(str.encode('1'))
        file_name = self.s.recv(1024).decode('utf-8')
        print(file_name)
        file_ext = file_name.split('.')[-1]
        file_size = self.s.recv(1024).decode('utf-8')

        with open(os.path.join(self.save_path, str(file_name)), 'wb') as f:
            print('Receiving File')
            print(int(file_size))
            pbar = tqdm(total = int(file_size)//1024)
            while True:
                data = self.s.recv(1024)
                pbar.update(1)
                if not data:
                    break;
                f.write(data)
            pbar.close()
            f.close()
        print('Successfully received file.')
        self.s.close()
        print('connection closed')
