from pprint import pprint

from instagram_private_api import Client, ClientThrottledError

from input_state import InputState
from input_states.abstract_input_state import AbstractInputState
from account_helper import list_account_entries


class FollowersUnsharedInputState(AbstractInputState):
    unshared: list = []

    def on_enter_old(self, input_state, client) -> (InputState, Client):
        print("\nLooking for people who don't follow you back.",
              "\nComparing following with followers...")

        following = client.user_following(client.authenticated_user_id, client.generate_uuid()).get("users")

        for account in following:
            try:
                followers_matching_following = client.user_followers(
                    client.authenticated_user_id, client.generate_uuid(), query=account.get("username")).get("users")
                if len(followers_matching_following) == 0:
                    self.unshared.append(account)
            except ClientThrottledError:
                print("You made too many API requests, try again later.")
                return InputState.MAIN_MENU, client

        return input_state, client

    def on_enter(self, input_state, client) -> (InputState, Client):
        print("\nLooking for people who don't follow you back.",
              "\nComparing following with followers...")

        try:
            following = client.user_following(client.authenticated_user_id, client.generate_uuid()).get("users")
            followers = client.user_followers(client.authenticated_user_id, client.generate_uuid()).get("users")
        except ClientThrottledError:
            print("You made too many API requests, try again later.", 'bB')
            return InputState.MAIN_MENU, client

        pprint(len(followers))

        '''for account in following:
            try:
                followers_matching_following = client.user_followers(
                    client.authenticated_user_id, client.generate_uuid(), query=account.get("username")).get("users")
                if len(followers_matching_following) == 0:
                    self.unshared.append(account)
            except ClientThrottledError:
                print("You made too many API requests, try again later.")
                return InputState.MAIN_MENU, client'''

        return input_state, client

    def list_info(self):
        print("Found {} people who don't follow you back!".format(len(self.unshared)))
        print("What do you want to do:",
              "\n\t1. List all.",
              "\n\t2. List all with extended information.",
              "\n\t3. Show one-by-one. (Here you can remove people one-by-one.)",
              "\n\t4. Show one-by-one with extended information. (Here you can remove people one-by-one.)",
              "\n\t5. Remove all.")

    def handle_input(self, prefix, input_state, client) -> (InputState, Client):
        response = input(prefix)

        if response == "1":
            list_account_entries(self.unshared, "\t")
        elif response == "2":
            list_account_entries(self.unshared, "\t", client)

        return input_state, client
