#######################################################################################
# File:             menu.py
# Author:           Raymond Rees Jr.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly neccessary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################

class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized and sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self):
        """
        Class constractor
        :param client: the client object on client side
        """
        # self.client = client
        # menu is now populated with the messages in a single list, easy to print and send.
        self.menu = []
        self.menu.append("****** TCP CHAT ******")
        self.menu.append("-----------------------")
        self.menu.append("Options Available:")
        self.menu.append("1. Get user list")
        self.menu.append("2. Sent a message")
        self.menu.append("3. Get my messages")
        self.menu.append("4. Create a new channel")
        self.menu.append("5. Chat in a channel with your friends")
        self.menu.append("6. Disconnect from server")

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        """
        TODO: 1. send a request to server requesting the menu.
        TODO: 2. receive and process the response from server (menu object) and set the menu object to self.menu
        TODO: 3. print the menu in client console.
        :return: VOID
        """
        print(self.get_menu())
        return None

    def process_user_data(self):
        """
        TODO: according to the option selected by the user, prepare the data that will be sent to the server.
        :param option:
        :return: VOID
        """
        data = {}
        option = self.option_selected()
        if 1 <= option <= 6: # validates a valid option
           # TODO: implement your code here
           print("Yay, you made it here! I am proud of you. :)")

           # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)

    def option_selected(self):
        """
        TODO: takes the option selected by the user in the menu
        :return: the option selected.
        """
        option = 0
        while True:
            try:
                option = input("Your option <enter a number> : ")
                if option.isdigit():
                    option = int(option)
                    if 1 <= option <= 6:
                        return option
                    else:
                        print("Invalid selection. Option must be an integer between 1 and 6")
                else:
                    print("Invalid selection. Option must be an integer")
            except KeyboardInterrupt:
                print("[!] Keyboard Interrupted!")
                break
            except Exception as e:
                print("[!] {}:\n -  {}".format(type(e).__name__, str(e)))
                break


    def get_menu(self):
        """
        TODO: Inplement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Sent a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a list representing the above menu.
        """
        myMenu = ""
        for line in self.menu:
            myMenu += line + '\n'  # whole menu delimited by
        return myMenu

    def option1(self):
        """
        TODO: Prepare the user input data for option 1 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 1.
        """
        data = {}
        data['option'] = 1
        # Your code here.
        return data

    def option2(self):
        """
        TODO: Prepare the user input data for option 2 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        data = {}
        data['option'] = 2
        # Your code here.
        return data

    def option3(self):
        """
        TODO: Prepare the user input data for option 3 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        data = {}
        data['option'] = 3
        # Your code here.
        return data

    def option4(self):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}
        data['option'] = 4
        # Your code here.
        return data

    def option5(self):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}
        data['option'] = 5
        # Your code here.
        return data

    def option6(self):
        """
        TODO: Prepare the user input data for option 6 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        data = {}
        data['option'] = 6
        # Your code here.
        return data
