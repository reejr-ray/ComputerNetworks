

import torrent_parser as tp

import socket
import math
import hashlib
import os

class Tracker():
    def __init__(self, server_obj):
        self.server = server_obj
        self.peer_table = []
        dir = os.path.dirname(__file__)
        self.torrent_name = os.path.join(dir, 'torrents\\age.torrent')
        torrent_data = self.decode_torrent(self.torrent_name)
        self.ip_port = torrent_data['announce'].split(":")

        announce_list = torrent_data['announce-list']
        for connection in announce_list:
            self.peer_table.append(socket.gethostbyname(socket.gethostname()))

        self.file_name = torrent_data['info']['name']
        self.tracker_ip = self.ip_port[0]
        self.tracker_port = self.ip_port[1]
        self.num_pieces = math.ceil(int(torrent_data['info']['length']) / int(torrent_data['info']['piece length']))

        hash = hashlib.sha1()
        hash.update(repr(torrent_data['info']).encode('utf-8'))
        self.info_hash = hash.hexdigest()
        print(self.info_hash)

    def check_if_announcer(self):
        if self.peer_table[0] == self.tracker_ip:
            print("You're the announce!")
            return True
        else:
            print("Peer: Connecting to announce Tracker")
            return False

    def broadcast_peer_list(self, client):
        print("broadcasting peer list")
        data = self.peer_table
        clienthandlers = self.peer_table
        try:
            for clients in clienthandlers:
                print(clients)
                self.server.send(clients, data[0])
            #self.server.send(client, data)
        except Exception as e:
            print("Error in broadcasting peer_list: " + str(e))

    def broadcast_not_send(self):
        print("HELLO WORLDS")
        print(self.peer_table)

    def decode_torrent(self, torrent_path):
        data = tp.parse_torrent_file(torrent_path)
        return data

    def set_file_name(self, torrent_data):
        dir = os.path.dirname(__file__)
        info = torrent_data['info']
        self.file_path = os.path.join(dir, 'torrents\\' + info['name'])

    def get_file_path(self):
        return self.file_path

    def get_file_name(self):
        return self.file_name

    def to_string(self):
        print("This is a tracker for ", self.file_name)
        print("announce is: ")

    def find_peers(self):
        return self.peer_table
