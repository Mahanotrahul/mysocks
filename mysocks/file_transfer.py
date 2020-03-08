import socket
import inspect
import os
import ntpath
import errno
from tqdm import tqdm
from mysocks.utilities import mapcount
import time
from math import floor, ceil

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

    def __init__(self, filenames, host = '127.0.0.1', port = 5560, n_listen = 1):
        """
        Constructor to start the file transfer process
        """
        if len(filenames) == 0:
            print('Filename should be passed as a list of all file locations. Empty list provided')
        # elif not all(os.path.exists(filename) for filename in filenames):
        #     raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filenames)
        # super(Model, self).__init__()

        self.s = super().create_server_socket(host, port, n_listen)

        self.send_file(filenames)

    def accept_connections(self):
        print("Waiting for client to connect")
        conn, addr = self.s.accept()
        print('Client connected at ' + str(addr[0]) + ':' + str(addr[1]))
        return conn, addr

    def lineno():
        """Returns the current line number in our program."""
        return inspect.currentframe().f_back.f_lineno

    def send_file(self, filenames):

        # try:
            if 'conn' not in locals():
                conn, addr = self.accept_connections()
            print("Waiting for the client to give confirmation to receive data")
            confirm_time = time.time()
            if time.time() - confirm_time < 10:
                confirm = conn.recv(1024)   ## Receive confirmation from the client. Expected value - '1'
                if confirm.decode('utf-8') == '1':
                    print("Confirmation received.")

                    # Sending Total number of files being sent to the client
                    no_files = len(filenames)

                    # TODO: Put valid file check in a separate utility Function
                    for filename in filenames:
                        if not os.path.exists(filename):
                            print('Error : ' + str(filename) + ' does not exist. Check the file location. Skipping transfer of this file')
                            no_files -= 1
                            continue

                    conn.send(str.encode(str(no_files)))
                    pbar1 = tqdm(total = int(no_files), initial = 0)

                    for filename in filenames:
                        if not os.path.exists(filename):
                            # print('Error : ' + str(filename) + ' does not exist. Check the file location. Skipping transfer of this file')
                            continue
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
                        conn.send(str.encode(''))
                        pbar1.update(1)

                    pbar1.close()
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
        no_files = int(self.s.recv(1024))
        pbar1 = tqdm(total = no_files, initial = 0)
        no_files_received = 0

        for i in range(no_files):
            file_name = self.s.recv(1024)
            print(file_name)
            file_ext = file_name.split('.')[-1]
            file_size = float(self.s.recv(1024))

            with open(os.path.join(self.save_path, str(file_name)), 'wb') as f:
                print('Receiving File')
                print(floor(file_size/1024))
                pbar = tqdm(total = int(file_size)//1024)
                if floor(file_size/1024) - ceil(file_size/1024) == 0:
                    for _ in range(floor(file_size/1024)):
                        print("In the integral multiple section")
                        data = self.s.recv(1024)
                        pbar.update(1)
                        f.write(data)
                else:
                    print("NOT In the integral multiple section")
                    for _ in range(floor(file_size/1024)):
                        data = self.s.recv(1024)
                        pbar.update(1)
                        f.write(data)
                    print("NOT In the integral multiple section")
                    # Receiving one more time as the file size is not a multiple of 1024
                    # Hence, One last chunk of data is still yet to be received
                    data = self.s.recv(1024)
                    pbar.update(1)
                    f.write(data)
                pbar.close()
                f.close()
            no_files_received += 1
            pbar1.update(1)
        pbar1.close()
        print('Successfully received ' + str(no_files_received) + ' files.')
        self.s.close()
        print('connection closed')
