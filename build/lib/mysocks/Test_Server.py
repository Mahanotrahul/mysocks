import socket
import argparse
import sys

parser = argparse.ArgumentParser(description = 'Create socket server', prog = 'SocketServer')
parser.add_argument('host', nargs='?', default = '127.0.0.1', help = 'Socket IP address')
parser.add_argument('port', nargs='?', default = 5560, type = int, help='Socket port number')
parser.add_argument('n_listen', nargs='?', default=1, type=int, help='Max. number of clients that can connect to the server')
parser.add_argument('--version', action='version', version='1.0.0')

args = parser.parse_args()

class sockets:

    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.listen = args.n_listen

    def create_socket(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.host, self.port))
            self.s.listen(self.listen)  # Sets max. number of clients that can connect to the server simulatneously
            self.s.setblocking(1)   #   To prevent from timeout

            print('Socket Server created at host = ', self.host, ':', str(self.port))
            return self.s
        except Exception as e:
            print("Error: ", e)
            sys.exit()

    def accept_connections(self):
        while True:
        	conn, addr = s.accept()
        	print('New client connected. Address = ' + str(addr[0]) + ' ' + str(addr[1]))
        	u_name = conn.recv(1024)
        	u_name = u_name.decode('utf-8')
        	u_name = u_name.replace('USER ', '')
        	print('user id = ' + str(u_name))
        	g_name = conn.recv(1024)
        	g_name = g_name.decode('utf-8')
        	g_name = g_name.replace('JOIN ', '')
        	print('group_id = ' + str(g_name))
        	all_connections.append(conn)
        	all_names.append(u_name)


        	if(g_name in group_names):
        		t = threading.Thread(target = receive_data, args = (g_name, conn, u_name))
        		t.daemon = True
        		t.start()
        	else:
        		group_names.append(g_name)
        		t = threading.Thread(target = receive_data, args = (g_name, conn, u_name))
        		t.daemon = True
        		t.start()

    def file_transfer(self, src, dest):
        pass



sock = sockets(args)
s = sock.create_socket()
