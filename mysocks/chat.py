import socket
import inspect
import os
import ntpath
import errno
from tqdm import tqdm
import time
from math import floor, ceil
import threading    # threading library is used to create separate threads for every clients connected
import select
from queue import Queue

from mysocks import gui

from . import Model


# TODO: Messenger  send/receive instead of chat

class chat(Model):
    """This class is parent class to chat module

    :param host: IP Address of the socket that the server will bind to. Defaults to 127.0.01
    :type host: string, optional
    :param port: port of the socket server. Defaults to 5660
    :type port: int
    :param n_listen: Max. number of clients to connect to at one time. Defaults to 5
    :type n_listen: int

    """


    def __init__(self, host = '127.0.0.1', port = 5660, n_listen = 5):


        super(Model, self).__init__()
        self.s = super().create_socket(host, port, n_listen)

    def accept_connections(self):

        conn, addr = self.accept()
        print('Client connected ' + str(addr[0]) + ' ' + str(addr[1]))
        return conn, addr



class server(Model):
    """This class is a parent class for all text message sending methods.
        Call this class to start a chat server. CLients will be able to connect to this server and
        all the clients will be able to chat with each other.
        Server will not participate in the server.


    :param host: IP Address of the socket that the server will bind to. Defaults to 127.0.01
    :type host: string, optional
    :param port: port of the socket server. Defaults to 5660
    :type port: int
    :param n_listen: Max. number of clients to connect to at one time. Defaults to 5
    :type n_listen: int
    :attr clients_connected: Total number of clients connected till now including the ones which may have left in between the chat.
    :type clients_connected: list
    :attr all_connections: socket object of all client connections. Deleted connections will be replaced by the keyword `deleted`.
    :type all_connections: list
    :attr type all_names: User names of all clients connected.
    :type all_names: list
    :attr type active_connections: Total number of active clients connected to the chat server.
    :type active_connections: list
    :attr s: server socket object.
    :type s: socket object

    """

    def __init__(self, host = '127.0.0.1', port = 5660, n_listen = 5, **kwargs):
        """Constructor to start the chat server

        :param host: IP Address of the socket that the server will bind to. Defaults to 127.0.01
        :type host: string, optional
        :param port: port of the socket server. Defaults to 5660
        :type port: int
        :param n_listen: Max. number of clients to connect to at one time. Defaults to 5
        :type n_listen: int


        """


        self.clients_connected = 0
        self.all_connections = []
        self.all_names = []
        self.active_connections = 0
        super(Model, self).__init__()
        # self.s = super().create_server_socket(host, port, n_listen)
        self.gui = kwargs.get('gui', False)
        self.isCalledFromGUI = kwargs.get('isCalledFromGUI', False)
        if self.isCalledFromGUI == False:
            if self.gui == True:    # If isCalledFromGUI == False and gui == True, launch gui from chat server but do not start the chat server
                self._gui = gui.launch(isCalledFromServer = True)
                self.gui_thread()
            else:
                self.start_server(host, port, n_listen) # If isCalledFromGUI == False and gui == False, start the chat server but do not launch the gui
        else:   #If isCalledFromGUI == True, only return the chat server object to the gui class
            pass

    def start_server(self, host, port, n_listen):
        self.s = super().create_server_socket(host, port, n_listen)
        if self._server_running == True:    # Variable from _init_ while creating a new socket server
            self.accept_connections()
        else:
            print('Server already running at the specified IP and port')

    def accept_connections(self):
        """ Method to accept client connections.
        Creates a separate thread for each client to receive_data from clients

        :return: tuple of conn and addr of the connected client
        :rtype: tuple


        """
        self.message_queue = Queue()
        ## TODO: Handle the function when self.active_connections > self.n_listen:
        # print(self._gui.Id)
        while self.active_connections <= self.n_listen:
            print("Waiting for client to connect")
            conn, addr = self.s.accept()
            temp = 'Client connected at ' + str(addr[0]) + ':' + str(addr[1])
            print(temp)
            self.message_queue.put(temp)
            self.clients_connected += 1
            self.active_connections += 1
            self.all_connections.append(conn)
            self.all_names.append('/<unkown username>/')
            self.thread = threading.Thread(target = self.receive_data, args = (conn, addr, self.clients_connected - 1))
            self.thread.daemon = True
            self.thread.start()

    def receive_data(self, conn, addr, client_no):
        """Method to receive data from clients.

        :param conn: socket object of the client
        :type conn: socket object
        :param addr: Address of the socket object
        :type addr: socket object
        :param client_no: Integer identifier of a client
        :type n_listen: int

        """


        u_name = conn.recv(1024)
        u_name = u_name.decode('utf-8')
        temp = 'Client name ' + str(u_name) + ' joined'
        print(temp)
        self.message_queue.put(temp)
        self.all_names[client_no] = u_name
        while True:

            try:
                data = conn.recv(1024)
                data = data.decode('utf-8')
                if conn is None or data == '':
                    temp = 'Client ' + str(u_name) + ' got disconnected'
                    print(temp)
                    self.message_queue.put(temp)
                    break

                print('Client : ' + str(u_name) + '> ' + str(data))
                msg = 'Client ' + str(u_name) + ' : ' + str(data)
                self.message_queue.put(msg)
                for connection in self.all_connections:
                    if conn is not connection and connection != 'deleted':
                        try:
                            ready_to_read, ready_to_write, in_error = select.select([connection,], [connection,], [], 1)
                        except select.error as e:
                            connection.shutdown(2)
                            connection.close()
                            print('Error in chat.server.receive_data.connection')
                        if ready_to_write:
                            connection.send(str.encode(msg))

            except Exception as e:
                print(e)
                print('Error in chat.server.receive_data')
                print('Client got disconnected')
                self.message_queue.put('Client got disconnected')
                conn.shutdown(2)
                conn.close()
                self.all_connections[client_no] = 'deleted'
                self.all_names[client_no] = 'deleted'
                self.active_connections -= 1
                break

    def gui_thread(self):
        self.gui_thread = threading.Thread(target = self._gui.launch_gui, args = ())
        self.gui_thread.daemon = True
        self.gui_thread.start()


class client(Model):
    """This class is a parent class for all text message client methods.
        Call this class to start a chat client.
        This method connects to the server at the provided host and port


    :param host: IP Address of the socket that the client will connect to. Defaults to 127.0.01
    :type host: string, optional
    :param port: port of the socket server. Defaults to 5660
    :type port: int

    """

    def __init__(self, host = '127.0.0.1', port = 5660, **kwargs):
        """Constructor to start the chat client

        :param host: IP Address of the socket that the client will connect to. Defaults to 127.0.01
        :type host: string, optional
        :param port: port of the socket server. Defaults to 5660
        :type port: int

        """

        super(Model, self).__init__()
        self.message_queue = Queue()

        self.gui = kwargs.get('gui', False)
        self.isCalledFromGUI = kwargs.get('isCalledFromGUI', False)
        if self.isCalledFromGUI == False:
            if self.gui == False:   # If isCalledFromGUI == False and gui == False, start the chat client but do not launch the gui
                self.start_client(host, port)
            else:   # If isCalledFromGUI == False and gui == True, launch gui from chat client but do not start the chat client
                self._gui = gui.launch(isCalledFromClient = True)
                self.gui_thread()
        else:   #If isCalledFromGUI == True, only return the chat client object to the gui class
            pass

    def start_client(self, host, port):
        self.s = super().create_client_socket(host, port)

        if self._connected_as_client == True:
            if self.isCalledFromGUI == True:        # For gui, send_data function will be called by the gui
                self.receive_data()
            else:
                ## Thread to receive data from the server
                self.receive_thread = threading.Thread(target = self.receive_data)
                self.receive_thread.daemon = True
                self.receive_thread.start()

                self.set_username()
                self.send_data()
        else:
            print('Client could not connect to any server. Try again.')

    def set_username(self, **kwargs):
        try:
            if self.isCalledFromGUI == True:
                self.u_name = kwargs.get('username')
            else:
                self.u_name = input('Your username? ')
            self.s.send(str.encode(self.u_name))
            time.sleep(0.1)
        except Exception as e:
            print(e)
            print('disconnected from the server')
            self._connected_as_client = False

    def send_data(self, **kwargs):
        """Method to send text messages to the server that will be relayed to other clients

        """

        if self.isCalledFromGUI == True:
            try:
                ready_to_read, ready_to_write, in_error = select.select([self.s,], [self.s,], [], 1)
            except select.error as e:
                self.s.shutdown(2)
                self.s.close()
                self._connected_as_client = False
                print('Client ' + str(self.u_name) + ' disconnected')
                return

            data = kwargs.get('message')
            msg = 'Your message : ' + str(data)
            self.message_queue.put(msg)
            time.sleep(0.1)
            try:
                if len(ready_to_write) > 0:
                    self.s.send(str.encode(data))
                    # print(str(data) + '- Message sent')
            except:
                self._connected_as_client = False
                print('Disconnecting client.')
                print('Client got disconnected')
                return

        else:
            try:
                while True:
                    try:
                        ready_to_read, ready_to_write, in_error = select.select([self.s,], [self.s,], [], 1)
                    except select.error as e:
                        self.s.shutdown(2)
                        self.s.close()

                        print('Client ' + str(self.u_name) + ' disconnected')
                        break

                    data = input('Your Message : ')
                    time.sleep(0.1)
                    try:
                        if len(ready_to_write) > 0:
                            self.s.send(str.encode(data))
                    except:
                        print('Client got disconnected')
                        break
            except Exception as e:
                print(e)
                print('disconnected from the server')

    def receive_data(self):
        """Method to receive data from the server


        """
        try:
            while True:
                try:
                    ready_to_read, ready_to_write, in_error = select.select([self.s,], [self.s,], [], 1)
                except select.error as e:
                    self.s.shutdown(2)
                    self.s.close()

                    print('Client ' + str(self.u_name) + ' disconnected')
                    break

                if len(ready_to_read) > 0:
                    msg = self.s.recv(1024)
                    msg = msg.decode('utf-8')
                    print(msg)
                    self.message_queue.put(msg)
        except Exception as e:
            print(e)
            print('Disconnecting client.')
            self._connected_as_client = False
            print('Client got disconnected')

    def gui_thread(self):
        self.gui_thread = threading.Thread(target = self._gui.launch_gui, args = ())
        self.gui_thread.daemon = True
        self.gui_thread.start()
