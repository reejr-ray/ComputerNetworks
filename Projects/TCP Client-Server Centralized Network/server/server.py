#######################################################################
# File:             server.py
# Author:           Raymond Rees Jr.
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################

from builtins import object
import socket
from threading import Thread
import pickle
import client_handler



class Server(object):
    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=12000):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an IPv4, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("Server socket created in IPv4, streaming mode.")
        print("SO_REUSEADDR enabled to allow IP/Ports to be reused.")
        self.clients = {}  # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        # bound to a port in _bind()
        self.host = ip_address
        self.port = port

    def close(self):
        self.serversocket.shutdown(socket.SHUT_RDWR)
        self.serversocket.close()
        print("server closed.")

    def _bind(self):
        """
        Bind host and port to server socket
        :return: VOID
        """
        try:
            self.serversocket.bind((self.host, self.port))
        except:
            print("failure in binding %s/%d to server socket." % (self.host, self.port))

    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        # TODO: your code here
        try:
            self._bind()
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server is listening at %s/%d" % (self.host, self.port))
        except:
            self.serversocket.close()
            print("Error setting socket to listen at %s/%d" % (self.host, self.port))

    """
    Threaded Function with the purpose of listening for updates from the client via menu
    :param clientsocket:
    :param addr:
    """
    def thread_client(self, clientsocket, addr):
        handler = self.client_handler_thread(clientsocket, addr)
        # handler._sendMenu()
        # do something with the client socket

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        client_id = 0
        while True:
            try:
                # print ("Server listening to new clients.")
                clienthandler, addr = self.serversocket.accept()
                client_id = addr[1]
                self.send_client_id(clienthandler, client_id)
                # recieve, process, and send responses to client
                Thread(target=self.thread_client, args=(clienthandler, addr)).start()
                print("Sending confirmation of handshake to client %s." % (str(client_id)))
            except KeyboardInterrupt:
                print("\n[!] Keyboard Interrupted!")
                self.close()
                break
            except Exception as e:
                print("[!] {}:\n -  {}".format(type(e).__name__, str(e)))

    def send(self, clientsocket, data):
        """
        TODO: Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        serialized_data = pickle.dumps(data)
        clientsocket.send(serialized_data)

    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        """
        TODO: Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        data_from_client = clientsocket.recv(MAX_BUFFER_SIZE)
        data = pickle.loads(data_from_client)
        return data

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        # self.send_client_id(clientsocket, address[1])
        handler = client_handler.ClientHandler(self, clientsocket, address)
        return handler

    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()
