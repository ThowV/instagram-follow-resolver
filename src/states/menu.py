from instagram_private_api import Client

from input_helper import do_input_loop
from main import console, base_color
from states import logout, action

prefix = "(menu): "
action_idx = 0


def start(client: Client):
    global action_idx

    console.print("\nChoose one of the following options:", style=base_color)
    console.print("\t1. List people who don't follow you back."
                  "\n\t2. List people who you don't follow back."
                  "\n\t3. Log out.")

    response = do_input_loop(prefix, range(3))

    action_idx = response
    if response == 3:
        logout.start(client)
    else:
        action.start(client)
