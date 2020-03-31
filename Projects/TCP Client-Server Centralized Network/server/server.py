#######################################################################
# File:             server.py
# Author:           Jose Ortiz
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
import menu


class Server(object):
    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=12005):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        # TODO: bind the socket to a public host, and a well-known port
        self.host = ip_address
        self.port = port

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

    def thread_client(self, clientsocket, addr):
        handler = self.client_handler_thread(clientsocket, addr)
        # do something with the clienthandler

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                # TODO: Accept a client
                # TODO: Create a thread of this client using the client_handler_threaded class
                clientsocket, addr = self.serversocket.accept()
                # TODO: from the addr variable, extract the client id assigned to the client
                # TODO: send assigned id to the new client. hint: call the send_clientid(..) method
                Thread(target=self.thread_client,
                       args=(clientsocket, addr)).start()  # receive, process, send response to client.
            except:
                # TODO: Handle exceptions
                self.serversocket.close()
                print("Closing server socket, error in accepting clients.")

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
        self.send_client_id(clientsocket, address[1])
        # TODO: create a new client handler object and return it
        handler = client_handler.ClientHandler(self.serversocket, clientsocket, address)
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
