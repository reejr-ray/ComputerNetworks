########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: Server support for multiple clients
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Raymond Rees Jr
# Student ID: 918690921
# Student Github Username: landsoul
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################
import threading
import pickle


class ClientHandler(object):
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """
    def __init__(self, server_instance, clienthandler, addr):
        """
        Class constructor already implemented for you.
        :param server_instance:
        :param clienthandler:
        :param addr:
        """
        self.clientid = addr[1] # the id of the client that owns this handler
        self.server_ip = addr[0]
        self.server = server_instance
        self.clienthandler = clienthandler

    def send(self, clienthandler, data):
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        serialized_data = pickle.dumps(data)
        clienthandler.send(serialized_data)
        return None

    def receive(self, clienthandler, MAX_ALLOC_MEM=4096):
        """
        # TODO: Deserialized the data from client
        :param MAX_ALLOC_MEM: default set to 4096
        :return: the deserialized data.
        """
        # print("Calling recv() on clientsocket... ")
        data_from_client = clienthandler.recv(MAX_ALLOC_MEM)
        data = pickle.loads(data_from_client)
        return data

    def print_lock(self):
        """
        TODO: create a new print lock
        :return: the lock created
        """
        lock = threading.Lock()
        lock.acquire()
        return lock

    def data_toString(self, data):
        student_name = data['student_name']
        github_user = data['github_username']
        sid = data['sid']

        print("Student ", student_name, " has connected to the server.")
        print("Their Github username is", github_user, "and SID is", sid, ".")

    def process_client_data(self):
        """
        TODO: receives the data from the client
        TODO: prepares the data to be printed in console
        # create a lock - done in print_lock()
        # adquire the lock - done in print_lock()
        TODO: prints the data in server console
        TODO: release the print lock
        :return: VOID
        """
        while True:
            try:
                client_data = self.receive(self.clienthandler)
                if not client_data:
                    break
                data = {'data': "The server got the data."}
                self.send(self.clienthandler, data)
                lock = self.print_lock() # creates and aquires the lock.
                self.data_toString(client_data) # prepares and prints data to console
                lock.release()
            except Exception as e:
                print("Error handling client", self.clientid)
                print(e.args)
            return None