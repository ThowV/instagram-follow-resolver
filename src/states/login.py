import sys

from getpass import getpass
from instagram_private_api import Client, ClientLoginError, ClientError

from main import console, base_color, success_color, fail_color
from states import menu


def start():
    console.print("\nFill in your Instagram credentials to allow authorization. Type :quit to exit the application",
                  style=base_color)

    while True:
        try:
            username = input("\tUsername: ")
            if username == ":quit":
                sys.exit()

            password = getpass("\tPassword: ")
            if password == ":quit":
                sys.exit()

            console.print("\tLogging in...")
            client = Client(username, password)
            console.print("\tLogin successful!", style=success_color)

            menu.start(client)
        except ClientLoginError:
            console.print("\tUsername or password were incorrect, try again.", style=fail_color)
        except ClientError:
            console.print("\tYou made too many API requests, try again later.", style=fail_color)
