########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Client Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name:
# Student ID:
# Student Github Username:
# Instructions: Read each problem carefully, and implement them correctly. Your grade in labs is based on passing
#               all the unit tests provided.
#               No partial credit will be given. Labs must be completed in class, and must be commited to your
#               personal repository by 9:45 pm on iLearn.
########################################################################################################################

# don't modify this imports.
import socket
import pickle


######################################## Client Socket ###############################################################3
"""
Client class that provides functionality to create a client socket is provided. Implement all the TODO parts 
"""

class Client(object):

    def __init__(self):
        """
        Class constructor
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = None
        self.student_name = "Raymond Rees Jr"
        self.github_username = "Landsoul"
        self.sid = 918690921

    def connect(self, server_ip_address, server_port):
        """
        :param server_ip_address:
        :param server_port:
        :return:
        """
        try:
            self.client.connect((server_ip_address, server_port))
            self.set_client_id()
        except:
            print('Client cannot connect to server %s/%d' % (server_ip_address, server_port))

        # data dictionary already created for you. Don't modify.
        data = {'student_name': self.student_name, 'github_username': self.github_username, 'sid': self.sid}

        while True:  # client is put in listening mode to retrieve data from server.
            try:
                self.send(data)
                data = self.receive()
                if not data:
                    break
                print("Message from server: ", data['data'])
                # break
            except:
                pass
        # self.close()

    def send(self, data):
        """
        Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data) # serialized data
        self.client.send(data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.client.recv(MAX_BUFFER_SIZE) # deserializes the data from server
        return pickle.loads(raw_data)

    def set_client_id(self):
        """
        Sets the client id assigned by the server to this client after a succesfull connection
        :return:
        """
        data = self.receive() # deserialized data
        client_id = data['clientid'] # extracts client id from data
        self.client_id = client_id # sets the client id to this client
        print("Client id " + str(self.client_id) + " assigned by server")

    def close(self):
        """
        :return: VOID
        """
        try:
            self.client.close()
        except:
            print('Error, the client cant close')


# main execution
if __name__ == '__main__':
    server_ip_address = "127.0.0.1"  # TODO: change this to the server ip address provided by instructor in class
    server_port = 5112
    client = Client()
    client.connect(server_ip_address, server_port)

# If your data was successfully sent to the server run by the instructor in class, you'll get full credit for this lab.


