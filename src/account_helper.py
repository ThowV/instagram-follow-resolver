from time import sleep

from instagram_private_api import Client, ClientThrottledError
from rich.progress import Progress
from rich.table import Table

from input_helper import request_use_stored, request_do_delay
from main import fail_color, console
from states import menu

account_following: list = []
account_followers: list = []


def do_data_check(client: Client, prefix: str):
    use_stored = False

    if account_following or account_followers:
        use_stored = request_use_stored(prefix)

    if not use_stored:
        do_delay = request_do_delay(prefix)
        collect_account_friendships(client, do_delay)


def collect_account_friendships(client: Client = None, do_delay: bool = True):
    global account_following, account_followers

    if client is None:
        return account_following, account_followers

    if account_following:
        account_following.clear()

    if account_followers:
        account_followers.clear()

    try:
        rank_token = client.generate_uuid()

        following_res = client.user_following(client.authenticated_user_id, rank_token)
        account_following.extend(following_res.get("users"))
        next_max_following_id = following_res.get("next_max_id")

        followers_res = client.user_followers(client.authenticated_user_id, rank_token)
        account_followers.extend(followers_res.get("users"))
        next_max_followers_id = followers_res.get("next_max_id")

        while next_max_following_id or next_max_followers_id:
            if next_max_following_id:
                following_res = client.user_following(client.authenticated_user_id, rank_token,
                                                      max_id=next_max_following_id)
                account_following.extend(following_res.get("users"))
                next_max_following_id = following_res.get("next_max_id")

            if next_max_followers_id:
                followers_res = client.user_followers(client.authenticated_user_id, rank_token,
                                                      max_id=next_max_followers_id)
                account_followers.extend(followers_res.get("users"))
                next_max_followers_id = followers_res.get("next_max_id")

            if do_delay:
                sleep(3)
    except ClientThrottledError:
        console.print("You made too many API requests, try again later.", style=fail_color)
        menu.start(client)


def list_accounts(accounts: list, client: Client = None, forced_idx: int = None):
    table = create_table(client)

    # Add table content
    for i, account in enumerate(accounts):
        if not forced_idx:
            account_info = [str(i + 1)]
        else:
            account_info = [str(forced_idx)]

        account_info.extend(get_account_info(account))
        if client is not None:
            extended_account_info = get_extended_account_info(account, client)

            if not extended_account_info:
                console.print("You made too many API requests, try again later.", style="red3")
                return

            account_info.extend(extended_account_info)

        table.add_row(*account_info)

    # Output table
    console.print(table)
    console.print("\n")


def get_account_info(account) -> list:
    username = account.get("username")
    full_name = account.get("full_name")

    is_private = "No"
    if account.get("is_private"):
        is_private = "Yes"

    is_verified = "No"
    if account.get("is_verified"):
        is_verified = "Yes"

    return [username, full_name, is_private, is_verified]


def get_extended_account_info(account, client: Client) -> list:
    try:
        account_extended = client.user_info(account.get("pk")).get("user")
        follower_count = str(account_extended.get("follower_count"))
        following_count = str(account_extended.get("following_count"))
        biography = str(account_extended.get("biography"))
        return [follower_count, following_count, biography]
    except ClientThrottledError:
        return []


def create_table(client: Client) -> Table:
    table = Table(show_header=True, header_style="light_salmon3")

    # Create table header
    table.add_column("Idx")
    table.add_column("Username")
    table.add_column("Full name")
    table.add_column("Private")
    table.add_column("Verified")

    if client is not None:
        table.add_column("Followers")
        table.add_column("Following")
        table.add_column("Biography")

    return table


def unfollow_accounts(client: Client, accounts: list, do_delay: bool = False):
    with Progress() as progress:
        # Progress bar
        if len(accounts) != 1:
            compare_task = progress.add_task("Removing...", total=len(accounts))
        else:
            console.print("Removing...")

        try:
            for i, account in enumerate(accounts):
                # Sleep so we don't do too many API calls
                if do_delay:
                    sleep(3)

                # Unfollow account
                client.friendships_destroy(account.get("pk"))

                # Remove account from data
                to_rem = None

                for following in account_following:
                    if following.get("pk") == account.get("pk"):
                        to_rem = following
                        break

                account_following.remove(to_rem)

                # Update progress
                if len(accounts) != 1:
                    progress.update(compare_task, advance=1)
        except ClientThrottledError:
            console.print("You made too many API requests, try again later.", style=fail_color)


def remove_accounts(client: Client, accounts: list, do_delay: bool = False):
    with Progress() as progress:
        # Progress bar
        if len(accounts) != 1:
            compare_task = progress.add_task("Removing...", total=len(accounts))

        try:
            for i, account in enumerate(accounts):
                # Sleep so we don't do too many API calls
                if do_delay:
                    sleep(3)

                # Unfollow account
                client.remove_follower(account.get("pk"))

                # Remove account from data
                to_rem = None

                for follower in account_followers:
                    if follower.get("pk") == account.get("pk"):
                        to_rem = follower
                        break

                account_followers.remove(to_rem)

                # Update progress
                if len(accounts) != 1:
                    progress.update(compare_task, advance=1)
        except ClientThrottledError:
            console.print("You made too many API requests, try again later.", style=fail_color)
