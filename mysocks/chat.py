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

from . import Model


# TODO: Messenger  start/receive instead of chat

class chat(Model):


    def __init__(self, host = '127.0.0.1', port = 5660, n_listen = 5):


        super(Model, self).__init__()
        self.s = super().create_socket(host, port, n_listen)

    def accept_connections(self):

        conn, addr = self.accept()
        print('Client connected ' + str(addr[0]) + ' ' + str(addr[1]))
        return conn, addr



class server(Model):

    def __init__(self, host = '127.0.0.1', port = 5660, n_listen = 5):

        self.clients_connected = 0
        self.all_connections = []
        self.all_names = []
        self.active_connections = 0
        self.s = super().create_server_socket(host, port, n_listen)
        self.accept_connections()

    def accept_connections(self):
        """ Method to accept client connections

        :return: tuple of conn and addr of the connected client
        :rtype: tuple


        """
        while self.active_connections <= self.n_listen:
            print("Waiting for client to connect")
            conn, addr = self.s.accept()
            print('Client connected at ' + str(addr[0]) + ':' + str(addr[1]))
            self.clients_connected += 1
            self.active_connections += 1
            self.all_connections.append(conn)
            self.all_names.append('/<unkown username>/')
            self.thread = threading.Thread(target = self.receive_data, args = (conn, addr, self.clients_connected - 1))
            self.thread.daemon = True
            self.thread.start()

    def receive_data(self, conn, addr, client_no):


        u_name = conn.recv(1024)
        u_name = u_name.decode('utf-8')
        print('Client name ' + str(u_name) + ' joined')
        self.all_names[client_no] = u_name
        while True:
            # try:
            #     ready_to_read, ready_to_write, in_error = select.select([conn], [], [], 1)
            #     print(ready_to_read)
            #     print(ready_to_write)
            #     print(str(in_error))
            # except select.error as e:
            #     conn.shutdown(2)
            #     conn.close()
            #     print('Error - socket not readable')
            #     print('Client ' + str(u_name) + ' disconnected')
            #     break

            # try:
            #     if len(ready_to_read) > 0:
            #         data = conn.recv(1024)
            #         data = data.decode('utf-8')
            #     else:
            #         print('Client ' + str(u_name) + ' got disconnected')
            #         break
            #
            #     if conn is None or data == '':
            #         print('Client ' + str(u_name) + ' got disconnected')
            #         break
            #
            #         print('Client : ' + str(u_name) + '> ' + str(data))
            try:
                data = conn.recv(1024)
                data = data.decode('utf-8')
                if conn is None or data == '':
                    print('Client ' + str(u_name) + ' got disconnected')
                    break

                print('Client : ' + str(u_name) + '> ' + str(data))
                msg = 'Client ' + str(u_name) + ' : ' + str(data)
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
                conn.shutdown(2)
                conn.close()
                self.all_connections[client_no] = 'deleted'
                self.all_names[client_no] = 'deleted'
                self.active_connections -= 1
                break



class client(Model):

    def __init__(self, host = '127.0.0.1', port = 5660):

        self.s = super().create_client_socket(host, port)

        ## Thread to receive data from the server
        self.receive_thread = threading.Thread(target = self.receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        ## Thread to send data to the server
        # self.send_thread = threading.Thread(target = self.send_data)
        # self.send_thread.daemon = True
        # self.send_thread.start()
        self.send_data()

    def send_data(self):

        try:
            u_name = input('Your username? ')
            self.s.send(str.encode(u_name))
            time.sleep(0.1)
            while True:
                try:
                    ready_to_read, ready_to_write, in_error = select.select([self.s,], [self.s,], [], 1)
                except select.error as e:
                    self.s.shutdown(2)
                    self.s.close()

                    print('Client ' + str(u_name) + ' disconnected')
                    break

                data = input('Your Message : ')
                time.sleep(0.1)
                if len(ready_to_write) > 0:
                    self.s.send(str.encode(data))
                else:
                    print('Client got disconnected')
                    break
        except Exception as e:
            print(e)
            print('disconnected from the server')

    def receive_data(self):

        try:
            while True:
                try:
                    ready_to_read, ready_to_write, in_error = select.select([self.s,], [self.s,], [], 1)
                except select.error as e:
                    self.s.shutdown(2)
                    self.s.close()

                    print('Client ' + str(u_name) + ' disconnected')
                    break

                if len(ready_to_read) > 0:
                    msg = self.s.recv(1024)
                    msg = msg.decode('utf-8')
                    print(msg)
        except Exception as e:
            print(e)
            print('Client got disconnected')
