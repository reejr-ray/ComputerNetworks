"""
Lab 8: peer.py
This file contains a basic template of the Peer class. In this lab, your job 
is to implement all the parts marked as TODO. Note that you don´t need to run
the code of this lab. The goal of this lab is to see how your logic works, and
therefore, to make sure that you understood how peers perform the downloading 
and uploading process in the network, and also which challenges you may encounter
when implementing those functionalities. 
"""
from server import Server
class Peer (Server):

    SERVER_PORT = 5000
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010

    def __init__(self, server_ip_address):
        Server.__init__(server_ip_address, self.SERVER_PORT)


    def run_server(self):
        """
        Already implemented. puts this peer to listen for connections requests from other peers
        :return: VOID
        """
        self.run()


    def _connect_to_peer(self, client_port_to_bind, peer_ip_address):
        """
        TODO: Create a new client object and bind the port given as a
              parameter to that specific client. Then use this client
              to connect to the peer (server) listening in the ip
              address provided as a parameter
        :param client_port_to_bind: the port to bind to a specific client
        :param peer_ip_address: the peer ip address that
                                the client needs to connect to
        :return: VOID
        """
        try:
            client = Client()
            client.bind(peer_ip_address, client_port_to_bind)
            client.connect(peer_ip_address)
            client.recv()
            client_port_to_bind += 1

            # initiate a TCP client-server connection
            # open a client socket
            # have it bound to port, and listen on that port
        except:
            print("Uh Oh, Spaghettios")

    def connect(self, peers_ip_addresses):
        """
        TODO: Initialize a temporal variable to the min client port range, then
              For each peer ip address, call the method _connect_to_peer()
              method, and then increment the client´s port range that
              needs to be bind to the next client. Break the loop when the
              port value is greater than the max client port range.

        :param peers: list of peer´s ip addresses in the network
        :return: VOID
        """
        pass # your code here
        for port in range(self.CLIENT_MIN_PORT_RANGE, self.CLIENT_MAX_PORT_RANGE + 1):
            peer_address_increment = len(peers_ip_addresses) - 1  # sub 1 because we don't want to go over CLIENT_MAX_PORT_RANGE
            peer_number = (port % 100) - 1  # port % 100 will return a number between 0-99
            if port > (self.CLIENT_MIN_PORT_RANGE + peer_address_increment):
                break
            else:
                # TODO thread this call
                self._connect_to_peer(port, peers_ip_addresses[peer_number])


