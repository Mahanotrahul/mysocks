"""
sockets module.
Provides a library to create socket server and clients to chat or transfer files
"""

import socket
import sys
import threading

"""
Threading module will be used to create threads for each clienr connection
connected to the Server
"""

__author__ = 'Rahul Mahanot'
__version__ = '1.0.1'

class Model(object):
    """Base Model Class for mysocks package

    Attributes
    ----------
    host : string
        IP Address of the socket that the server will bind to. Defaults to localhost
    port : int
        port of the socket server. Defaults to 5560

    """

    # Class Variable
    host = ''
    port = 5560
    def __init__(self):

        """
        Default constructor for abstract base class Model
        """

    def create_server_socket(self, host, port, n_listen):
        """Function to create a socket for a server that can handle `n_listen` number of clients at a time

            Args:
                host (string): IP address of the socket to be created on in decimal notation or in hexadecimal notation
                port (integer): Port number of the server that will be open for the clients
                n_listen (integer): Maximum number of clients that the server can handle at a time

        Parameters
        ----------
        host : string
            IP Address of the socket that the server will bind to. Defaults to localhost
        port : int
            port of the socket server. Defaults to 5560
        n_listen : int
            Max. number of clients to connect to at one time


        Returns
        -------
        s : socket object
            socket object
        """


        self.host = host            ## Socket IP address
        self.port = port            ## Socket port number
        self.n_listen = n_listen    ## Max. number of clients that can connect to the server

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, self.port))
            s.listen(self.n_listen)  # Sets max. number of clients that can connect to the server simulatneously
            s.setblocking(1)   #   To prevent from timeout

            print('Socket Server created at host = ', self.host, ':', str(self.port))
            self.s = s
            return self.s

        except Exception as e:
            if e.errno == 10048:
                print('Socket already exists')
                return self.s
            else:
                print("Error: ", e)
                print('Error with creating sockets')
                sys.exit()

    def create_client_socket(self, host, port):
        """
        Function to create a socket for a server that can handle `n_listen` number of clients at a time

        Args:
            host (string): IP address of the socket to be created on in decimal notation or in hexadecimal notation
            port (integer): Port number of the server that will be open for the clients


        Parameters
        ----------
        host : string
            IP Address of the socket that the server will bind to. Defaults to localhost
        port : int
            port of the socket server. Defaults to 5560

        Returns
        -------
        s : socket object
            socket object
        """

        self.host = host            ## Socket IP address
        self.port = port            ## Socket port number

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))

            print('Connected to socket server at host = ', self.host, ':', str(self.port))
            self.s = s
            return self.s

        except Exception as e:
            if e.errno == 10048:
                print('Socket already exists')
                return self.s
            else:
                print("Error: ", e)
                print('Error with connecting to socket server')
                sys.exit()


    def accept_connections(self):
        conn, addr = self.s.accept()
        print('Client connected' + str(addr[0]) + ' ' + str(addr[1]))
        data = conn.recv(1024)
        print(data.decode('utf-8'))
        filename = 'client.py'
        conn.send(str.encode(filename))
        f =  open(filename, 'rb')
        l = f.read(1024)
        while(l):
            conn.send(l)
            l = f.read(1024)
        f.close()
        print('Done sending')
        conn.send(str.encode('Thank you'))
        conn.close()

    def file_transfer(self, src, dest):
        pass
