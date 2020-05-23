from instagram_private_api import Client
from rich.console import Console
from rich.table import Table


def list_account_entries(accounts, client=None):
    console = Console()
    console.print("\nListing all accounts:", style="light_salmon3")

    # Create a table
    table = Table(show_header=True, header_style="light_salmon3")

    table.add_column("Idx")
    table.add_column("Username")
    table.add_column("Full name")
    table.add_column("Private")
    table.add_column("Verified")

    if client is not None:
        table.add_column("Followers")
        table.add_column("Following")
        table.add_column("Biography")

    for i, account in enumerate(accounts):
        account_info = [str(i + 1)]

        account_info.extend(get_account_info(account))
        if client is not None:
            account_info.extend(get_extended_account_info(account, client))

        table.add_row(*account_info)

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
    account_extended = client.user_info(account.get("pk")).get("user")

    followers = str(account_extended.get("follower_count"))
    following = str(account_extended.get("following_count"))
    biography = str(account_extended.get("biography"))

    return [followers, following, biography]
