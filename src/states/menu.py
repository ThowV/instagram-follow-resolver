from instagram_private_api import Client

from input_helper import do_input_loop
from main import console, base_color
from states import logout, following

prefix = "(menu): "


def start(client: Client):
    console.print("\nChoose one of the following options:", style=base_color)
    console.print("\t1. List people who don't follow you back."
                  "\n\t2. List people who you don't follow back."
                  "\n\t3. List dead accounts that you follow."
                  "\n\t4. List dead accounts that follow you."
                  "\n\t5. Log out.")

    response = do_input_loop(prefix, range(5))

    if response == 1:
        following.start(client)
    elif response == 5:
        logout.start(client)
