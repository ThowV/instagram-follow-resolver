from instagram_private_api import Client, ClientError, ClientThrottledError

from main import console, base_color, fail_color
from states import login

import account_helper


def start(client: Client):
    # Log out
    console.print("\nLogging out...", style=base_color)

    try:
        client.logout()
    except (ClientError, ClientThrottledError):
        console.print("\tYou made too many API requests, forcefully logging out...", style=fail_color)

    # Clean data
    console.print("Cleaning past data...", style=base_color)
    account_helper.account_followers.clear()
    account_helper.account_following.clear()

    # Login
    login.start()
