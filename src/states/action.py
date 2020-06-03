from instagram_private_api import Client

import account_helper
from actions import following_unshared, followers_unshared

from input_helper import do_input_loop, request_do_delay, request_extra_confirmation
from main import console, base_color, fail_color
from states import menu

prefix = "(menu): "

unshared: list = []


def start(client: Client):
    global unshared

    account_helper.do_data_check(client, prefix)

    # Compare to get hits
    if menu.action_idx == 1:
        unshared = following_unshared.compare()
    elif menu.action_idx == 2:
        unshared = followers_unshared.compare()

    input(client)


def input(client: Client):
    # Present results and get input on what to do
    console.print("\nFound {} people who match the chosen criteria!".format(len(unshared)), style=base_color)
    console.print("What do you want to do:"
                  "\n\t1. List all."
                  "\n\t2. Show one-by-one. (Here you can remove people one-by-one.)"
                  "\n\t3. Remove all. (This could result in many API calls.)"
                  "\n\t4. Return.")

    response = do_input_loop(prefix, range(4))

    if response == 1:
        list_all()
        input(client)
    elif response == 2:
        show_obo(client)
        start(client)
    elif response == 3:
        remove_all(client)
        start(client)
    elif response == 4:
        menu.start(client)


def list_all():
    console.print("\nListing all accounts:", style=base_color)
    account_helper.list_accounts(unshared)


def show_obo(client: Client):
    for i, account in enumerate(unshared):
        account_helper.list_accounts([account], forced_idx=i + 1)

        while True:
            console.print("\t1. Get extended information.\n\t2. Remove.\n\t3. Next. \n\t4. Return")

            response = do_input_loop(prefix, range(4))
            if response == 1:
                account_helper.list_accounts([account], client, i + 1)
            elif response == 2:
                if menu.action_idx == 1:
                    account_helper.unfollow_accounts(client, [account])
                elif menu.action_idx == 2:
                    account_helper.remove_accounts(client, [account])
                break
            elif response == 3:
                break
            elif response == 4:
                return


def remove_all(client: Client):
    # Request confirmation
    confirmation = request_extra_confirmation(prefix)

    if confirmation:
        # Request do delay
        do_delay = request_do_delay(prefix)

        console.print("\nRemoving all accounts.", style=base_color)

        if menu.action_idx == 1:
            account_helper.unfollow_accounts(client, unshared, do_delay)
        elif menu.action_idx == 2:
            account_helper.remove_accounts(client, unshared, do_delay)
