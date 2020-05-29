from time import sleep

from instagram_private_api import Client, ClientThrottledError
from rich.console import Console
from rich.table import Table

following: list = []
followers: list = []


def get_account_friendships(client: Client = None, do_delay: bool = True) -> (list, list):
    global following, followers

    if client is None:
        return following, followers

    if following:
        following.clear()

    if followers:
        followers.clear()

    rank_token = client.generate_uuid()

    following_res = client.user_following(client.authenticated_user_id, rank_token)
    following.extend(following_res.get("users"))
    next_max_following_id = following_res.get("next_max_id")

    followers_res = client.user_followers(client.authenticated_user_id, rank_token)
    followers.extend(followers_res.get("users"))
    next_max_followers_id = followers_res.get("next_max_id")

    while next_max_following_id or next_max_followers_id:
        if next_max_following_id:
            following_res = client.user_following(client.authenticated_user_id, rank_token,
                                                  max_id=next_max_following_id)
            following.extend(following_res.get("users"))
            next_max_following_id = following_res.get("next_max_id")

        if next_max_followers_id:
            followers_res = client.user_followers(client.authenticated_user_id, rank_token,
                                                  max_id=next_max_followers_id)
            followers.extend(followers_res.get("users"))
            next_max_followers_id = followers_res.get("next_max_id")

        if do_delay:
            sleep(3)

    return following, followers


def list_account_entries(accounts: list, client: Client = None, forced_idx: int = None):
    console = Console()
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
        followers = str(account_extended.get("follower_count"))
        following = str(account_extended.get("following_count"))
        biography = str(account_extended.get("biography"))
        return [followers, following, biography]
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
