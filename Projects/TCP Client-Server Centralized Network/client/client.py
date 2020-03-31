#######################################################################
# File:             client.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are 
#                   free to drop this client class, and add yours instead. 
# Running:          Python 2: python client.py 
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle

class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server 
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_id = 0
        self.name = "Anonymous"

    def getSelfInfo(self):
        host = input('Enter the server IP Address: ')
        if host is None:
            host = "127.0.0.1"
        port = input('Enter the server port: ')
        port = int(port)
        if port is None:
            port = 12005
        self.name = input('Your id key (i.e your name): ')
        if self.name is None:
            self.name = "Anonymous"
        userData = {"host": host, "port": port, "name": self.name}
        return userData

    def get_client_id(self):
        return self.client_id

    
    def connect(self, host="127.0.0.1", port=12000):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
	    Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        try:
            self.clientSocket.connect((host, port))
            data = self.receive()  # deserialized data
            client_id = data['clientid']  # extracts client id from data
            self.clientid = client_id  # sets the client id to this client
            print("Successfully connected to server with IP: %s and port: %d" % (host, port))
            print("Your client info is:")
            print("Client Name:", self.name)
            print("Client ID:", client_id)
            print("Client id " + str(self.clientid) + " assigned by server")
        except:
            print('%s cannot connect to server %s/%d' % (self.name, host, port))

        # data dictionary already created for you. Don't modify.
        # data = {'student_name': self.student_name, 'github_username': self.github_username, 'sid': self.sid}
        data = {'client_name': self.name, 'clientid': self.client_id}

        while True:  # client is put in listening mode to retrieve data from server.
            try:
                self.send(data)
                data = self.receive()
                if not data:
                    break
                print("Message from server: ", data['data'])
                break
            except:
                pass
        self.close()


    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data)  # serialized data
        self.clientSocket.send(data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE)  # deserializes the data from server
        return pickle.loads(raw_data)
        

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        try:
            self.clientSocket.close()
        except:
            print('Error, the clientSocket cant close')

		

if __name__ == '__main__':
    client = Client()
    data = client.getSelfInfo()  # returns a dictionary containing {ip adress, port, name}
    client.connect(data["host"], data["port"])
