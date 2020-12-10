#######################################################################
# File:             client_handler.py
# Author:           Raymond Rees Jr.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
import threading
import menu

class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """

        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.client_name = ""
        self.server = server_instance
        self.clientsocket = clientsocket
        self.unread_messages = []

        self.process_user_info()
        lock = self.aquire_lock() # locks threads to print connection acknowledgement to the server
        self.print_user_connect()
        lock.release()
        self._sendMenu()

    def process_user_info(self):
        """
        handles the initial user info.  __init__ helper class.
        recvs client name and stores a new client object on the server. Needs a lock to prevent unwanted writes during
        object creation.
        """
        data = self.server.receive(self.clientsocket) # listen for the client's login info
        if 'client_name' in data.keys() and data['clientid'] == self.client_id: # make sure its the right data(and same sender)
            self.client_name = data['client_name']
        # add client to server list
        self.server.add_client(self)
        print(str(self.server.clients)) # works!

    def aquire_lock(self):
        """
        This class is necessary whenever any read/write/print is done on the server.
        use with methods print_user_connect, print_user_disconnect
        :return: the lock created
        """
        lock = threading.Lock()
        lock.acquire()
        return lock

    def print_user_connect(self):
        print("Client %s:%s has successfully connected to the server." % (self.client_name, self.client_id))

    def print_user_disconnect(self):
        print("Client %s:%s has disconnected from the server." % (self.client_name, self.client_id))


    def _sendMenu(self):
        """
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        m = menu.Menu()
        data = {'menu': m}
        self.server.send(self.clientsocket, data)

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        :return:
        """
        data = self.server.receive(self.clientsocket)
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6:  # validates a valid option selected
            option = data['option_selected']
            if option == 1:
                self._send_user_list()
            elif option == 2:
                recipient_id = data['recipient_id']
                message = data['message']
                self._save_message(recipient_id, message)
            elif option == 3:
                self._send_messages()
            elif option == 4:
                room_id = data['room_id']
                self._create_chat(room_id)
            elif option == 5:
                room_id = data['room_id']
                self._join_chat(room_id)
            elif option == 6:
                self._disconnect_from_server()
        else:
            print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        return None

    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        pass

    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        pass

    def _create_chat(self, room_id):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        pass

    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        pass

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        pass

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        try:
            self.delete_client_data()
            self.clientsocket.close()
        except:
            print("Error disconnecting client", self.client_id)
        pass













