########################################################################################################################
# Class: Computer Networks
# Date: 12/01/2020
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Name: Raymond Rees Jr.
# ID: 918690921
# Github Username: reejr-ray
# Program Running instructions:
#               python server.py  # compatible with python version 2
#               python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
from threading import Thread
from client_handler import ClientHandler

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port = 12000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        # creates a server socket set in IPv4 mode, with
        # SO_REUSEADDR enabled to allow IP/Ports to be reused.
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("socket creation successful!")

    def _close():
        self.serversocket.shutdown(socket.SHUT_RDWR)
        self.serversocket.close()
        print("closed.")

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))
        print("Bind to %s / %d succeeded." % (self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server is listening at %s / %d" % (self.host, self.port))
        except KeyboardInterrupt:
            print("[!] Keyboard Interrupted!")
            self._close()
        except Exception as e:
            print("[!] {}:\n -  {}".format(type(e).__name__, str(e)))

    def _handler(self, clienthandler):
        """
        #TODO: receive, process, send response to the client using this handler.
        :param clienthandler:
        :return:
        """
        while True:
            # TODO: receive data from client
            # TODO: if no data, break the loop
            # TODO: Otherwise, send acknowledge to client. (i.e a message saying 'server got the data
            try:
                client_data = self.receive(clienthandler)
                if not client_data:
                    break
                data = {'data': "The server got the data."}
                self.send(clienthandler, data)
                student_name = client_data['student_name']
                github_user = client_data['github_username']
                sid = client_data['sid']
                print("Student ", student_name, " has connected to the server.")
                print("Their Github username is", github_user, "and SID is", sid, ".")
                break
            except KeyboardInterrupt:
                 print("[!] Keyboard Interrupted!")
                 self._close()
            except Exception as e:
                 print("[!] {}:\n -  {}".format(type(e).__name__, str(e)))

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        data = {'clientid': clientid}
        serialized_data = pickle.dumps(data)
        clienthandler.send(serialized_data)
        return None

    def thread_client(self, clienthandler, addr):
        # init the client handler object
        c = ClientHandler(self, clienthandler, addr)
        c.process_client_data()

    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        client_id = 0
        while True:
            try:
                # print("Server listening for new clients.")
                clienthandler, addr = self.serversocket.accept()
                # TODO: from the addr variable, extract the client id assigned to the client
                # TODO: send assigned id to the new client. hint: call the send_clientid(..) method
                client_id = addr[1]
                self._send_clientid(clienthandler, client_id)
                Thread(target=self.thread_client, args=(clienthandler, addr)).start()  # receive, process, send response to client.
                print("Sending confirmation to client %s." % (str(client_id)))
            except KeyboardInterrupt:
                print("[!] Keyboard Interrupted!")
                self._close()
                break
            except Exception as e:
                print("[!] {}:\n -  {}".format(type(e).__name__, str(e)))

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()

# main execution
if __name__ == '__main__':
    server = Server()
    server.run()











