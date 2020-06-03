from instagram_private_api import Client
from rich.progress import Progress

import account_helper

from input_helper import do_input_loop, request_do_delay, request_extra_confirmation
from main import console, base_color, fail_color
from states import menu

prefix = "(menu): "

unshared: list = []


def start(client: Client):
    global unshared

    account_helper.do_data_check(client, prefix)

    # Compare following and followers
    unshared = compare(account_helper.account_following, account_helper.account_followers)

    input(client)


def input(client: Client):
    # Present results and get input on what to do
    console.print("\nFound {} people who don't follow you back!".format(len(unshared)), style=base_color)
    console.print("What do you want to do:"
                  "\n\t1. List all."
                  "\n\t2. Show one-by-one. (Here you can remove people one-by-one.)"
                  "\n\t3. Unfollow all. (This could result in many API calls.)"
                  "\n\t4. Return.")

    response = do_input_loop(prefix, range(4))

    if response == 1:
        list_all()
        input(client)
    elif response == 2:
        show_obo(client)
        start(client)
    elif response == 3:
        unfollow_all(client)
        start(client)
    elif response == 4:
        menu.start(client)


def compare(following: list, followers: list) -> list:
    compared_hits: list = []

    # Compare and display progress
    with Progress() as progress:
        # Progress bar
        compare_task_length = len(following) * len(followers)
        compare_task = progress.add_task("Comparing...", total=compare_task_length)

        for account in following:
            for idx, follower in enumerate(followers):
                # Update the progress bar
                progress.update(compare_task, advance=1)

                # Compare following with follower
                if account.get("pk") == follower.get("pk"):
                    progress.update(compare_task, advance=len(followers) - idx)
                    break  # This account follows us so we stop comparing
                if idx == len(followers) - 1:
                    compared_hits.append(account)  # This account does not follow us back

    return compared_hits


def list_all():
    console.print("\nListing all accounts:", style=base_color)
    account_helper.list_accounts(unshared)


def show_obo(client: Client):
    for i, account in enumerate(unshared):
        account_helper.list_accounts([account], forced_idx=i + 1)

        while True:
            console.print("\t1. Get extended information.\n\t2. Unfollow.\n\t3. Next. \n\t4. Return")

            response = do_input_loop(prefix, range(4))
            if response == 1:
                account_helper.list_accounts([account], client, i + 1)
            elif response == 2:
                account_helper.unfollow_accounts(client, [account])
                break
            elif response == 3:
                break
            elif response == 4:
                return


def unfollow_all(client: Client):
    # Request confirmation
    confirmation = request_extra_confirmation(prefix)

    if confirmation:
        # Request do delay
        do_delay = request_do_delay(prefix)

        console.print("\nUnfollowing all accounts", style=base_color)
        account_helper.unfollow_accounts(client, unshared, do_delay)
