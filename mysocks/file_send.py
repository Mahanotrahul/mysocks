import socket

from . import Model

class file_send(Model):
    """
    This class is parent class to file transfer module.
    """
    def __init__(self, host = '127.0.0.1', port = 5560, n_listen = 1):
        """
        Constructor to start the file sending process
        """

        super(Model, self).__init__()
        self.s = super().create_socket(host, port, n_listen)

    def accept_connections(self, filename):
        conn, addr = self.s.accept()
        print('Client connected' + str(addr[0]) + ' ' + str(addr[1]))
        data = conn.recv(1024)
        print(data.decode('utf-8'))
        conn.send(str.encode('Sending file - ' + filename))
        f =  open(filename, 'rb')
        l = f.read(1024)
        while(l):
            conn.send(l)
            l = f.read(1024)
        f.close()
        print('Done sending')
        conn.send(str.encode('Thank you'))
        conn.close()
