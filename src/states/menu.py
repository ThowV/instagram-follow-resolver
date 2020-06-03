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
                  "\n\t3. List dead accounts that you follow."
                  "\n\t4. List dead accounts that follow you."
                  "\n\t5. Log out.")

    response = do_input_loop(prefix, range(5))

    if response == 1:
        action_idx = 1
        action.start(client)
    elif response == 2:
        action_idx = 2
        action.start(client)
    elif response == 3:
        action_idx = 3
    elif response == 4:
        action_idx = 4
    elif response == 5:
        logout.start(client)
