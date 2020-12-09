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
import io
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
        Class constructor
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = 0
        self.port = None
        self.host = None
        self.name = "Anonymous"

    def getSelfInfo(self):
        host = input('Enter the server IP Address: (default is 127.0.0.1)')
        if host is None:
            host = "127.0.0.1"
        port = input('Enter the server port: (default is 12000)')
        port = int(port)
        if port is None:
            port = 12000
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
            print("Client Name: ", self.name)
            print("Client ID: ", client_id)
            print()
        except:
            print('%s cannot connect to server %s/%d' % (self.name, host, port))
            self.close()
            return

        # data dictionary already created for you. Don't modify.
        # data = {'student_name': self.student_name, 'github_username': self.github_username, 'sid': self.sid}
        data = {'client_name': self.name, 'clientid': self.client_id}

        while True:  # client is put in listening mode to retrieve data from server.
            try:
                self.send(data)
                print("trying to recieve menu and use...")
                data = self.receive()
                print(data)
                if not data:
                    break
                menu = data["menu"]
                menu.show_menu() # it works! :D
            except KeyboardInterrupt:
                print("\n[!] Keyboard Interrupted!")
                self.close()
                break
            except Exception as e:
                print("[!] {}:\n -  {}".format(type(e).__name__, str(e)))


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
        try:
            raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE)  # deserializes the data from server
            return pickle.loads(raw_data)
        except KeyboardInterrupt:
            print("\n[!] Keyboard Interrupted!")
            self.close()
        except Exception as e:
            print("[!] {}:\n -  {}".format(type(e).__name__, str(e)))

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        self.clientSocket.shutdown(socket.SHUT_RDWR)
        self.clientSocket.close()
        print("client closed.")

# potential workaround for shitty pathing issues. NOT WORKING
# note to self:
# NEVER STRUCTURE, OR ALLOW OTHERS TO STRUCTURE FILES WITH THIS SCHEME:
# base
# |
# ----client
# |   |
# |   ----- client.py
# |
# ----server
#   |
#   ------- main.py
#
# Without a fancy workaround, python only checks the base level structure of main.py.
# attempting to "import client.py" or "import client.client.py" into main.py WILL NOT WORK. it will barf in your
# face and leave you speechless as to why its failing besides "module client not found.".

# class RenameUnpickler(pickle.Unpickler):
#     def find_class(self, module, name):
#         renamed_module = module
#         if module == "menu":
#             renamed_module = "server.menu"
#
#             return super(RenameUnpickler, self).find_class(renamed_module, name)
#
# def renamed_load(file_obj):
#     return RenameUnpickler(file_obj).load()
#
# def renamed_loads(pickled_bytes):
#     file_obj = io.BytesIO(pickled_bytes)
#     return renamed_load(file_obj)


if __name__ == '__main__':
    client = Client()
    data = client.getSelfInfo()  # returns a dictionary containing {ip adress, port, name}
    client.connect(data["host"], data["port"])
