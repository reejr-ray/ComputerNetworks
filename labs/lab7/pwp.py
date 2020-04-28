"""
Lab 7: Peer Wire Protocol (PWP)
Create a class with the basic implementation for the bitTorrent peer wire protocol
A basic template structure is provided, but you may need to implement more methods
For example, the payload method depending of the option selected
"""

class PWP(object):
    # pstr and pstrlen constants used by the handshake process
    PSTR = "BitTorrent protocol"
    PSTRLEN = 19
    # TODO: Define ID constants for all the message fields such as unchoked, interested....
    ID_CHOKE = 0
    ID_UNCHOKE = 1
    ID_INTERESTED = 2
    ID_NOT_INTERESTED = 3
    ID_HAVE = 4
    ID_BITFIELD = 5
    ID_REQUEST = 6
    ID_PIECE = 7
    ID_CANCEL = 8

    def __init__(self):
        """
        Empty constructor
        """
        pass

    def handshake(self, info_hash, peer_id, pstrlen=PSTRLEN, pstr=PSTR):
        """
        TODO: implement the handshake
        :param options:
        :return: the handshake message
        """
        pass

    def message(self, len, message_id, payload):
        """
        TODO: implement the message
        :param len:
        :param message_id:
        :param payload:
        :return: the message
        """
        pass


