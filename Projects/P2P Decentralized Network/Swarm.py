
import threading

import tracker
import peer
import server

class Swarm(tracker):

    def __init__(self, torrent_tracker):
        self.peer_list = []
        self.seeder_list = []
        self.leech_list = []
        self.tracker = torrent_tracker

    def add_peer(self, peer):
        self.peer_list.append(peer)

    def change_peer_to_leech(self, peer):
        self.peer_list.remove(peer)
        self.leech_list.append(peer)

    def make_seeder(self, peer):
        self.tracker.peer_table.append('' + peer.server.host + ':' + peer.server.port)  # IP : Port is now a seeder
        self.peer_list.remove(peer)
        self.seeder_list.append(peer)

    # ------  GETTERS -------
    def get_peer_list(self):
        return self.peer_list

    def get_seeder_list(self):
        return self.seeder_list
