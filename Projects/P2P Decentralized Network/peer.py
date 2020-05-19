from client import Client
from server import Server
from tracker import Tracker
from PWP import PWP
import message

import math

import threading as thread
from tracker import Tracker

import uuid

class Peer(Client, Server):

    DEFAULT_SERVER_PORT = 5000
    MIN_PORT = 5001
    MAX_PORT = 5010

    def __init__(self):
        """
            Initializes a peer on the network
        """
        self.server = Server()
        Server.__init__(self)
        self.client = Client()
        Client.__init__(self)
        self.id = uuid.uuid4()
        self.clienthander_list = []

    def run_server(self):
        """
        Already implemented. puts this peer to listen for connections requests from other peers
        :return: VOID
        """
        try:
            # must thread the server, otherwise it will block the main thread
            thread.Thread(target=peer.server.run, daemon=True).start()
        except Exception as error:
            print(error)  # server failed to run

    def peer_client_connector(self, client_port_to_bind, peer_ip_address, peer_port=5000):
        print("\npeer_client_connector")
        client = Client()
        tracker = Tracker(self.server)
        # print(client_port_to_bind)
        # print(peer_ip_address)
        try:
            # binds the client to the ip address assigned by LAN
            client.bind('0.0.0.0', client_port_to_bind)  # note: when you bind, the port bound will be the client id
            print("successfully bound to 0.0.0.0 " + str(client_port_to_bind))
            self.clienthander_list.append(client)
            thread.Thread(target=client.connect, args=(peer_ip_address, peer_port)).start()  # threads server
            tracker.broadcast_not_send()
            return True
        except Exception as error:
            print(error)
            client.close()
            return False

    def connect_to_all_peers(self, peer_ip_addresses):
        print("connecting to all peers")
        peer_client_port = self.MIN_PORT
        default_peer_port = self.DEFAULT_SERVER_PORT

        for peer_ip in peer_ip_addresses:
            if peer_client_port > self.MAX_PORT:
                break
            if "/" in peer_ip:
                ip_and_port = peer_ip.split("/")
                peer_ip = ip_and_port[0]
                default_peer_port = int(ip_and_port[1])
            # if self.peer_client_connector(peer_client_port, peer_ip, default_peer_port):
            if self.peer_client_connector(peer_client_port, peer_ip):
                peer_client_port += 1


    def peer_threader(self, ip_addresses):
        try:
            print("running server")
            self.run_server()
            print(thread.active_count())
            print("connecting to all peers")
            self.connect_to_all_peers(ip_addresses)


        except Exception as e:
            print(e)


if __name__ == '__main__':
    peer = Peer()
    tracker = Tracker(peer.server)
    ip_addresses = tracker.find_peers()
    print(ip_addresses)
    peer.peer_threader(ip_addresses)

    tracker.broadcast_peer_list(peer.server)

    pwp = PWP(tracker.num_pieces)
    peer.handshake_message = pwp.handshake(tracker.info_hash, id)
