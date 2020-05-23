from pprint import pprint

from instagram_private_api import ClientThrottledError

from input_states import menu_state
from input_states.abstract_input_state import AbstractInputState
from account_helper import list_account_entries


class FollowersUnsharedInputState(AbstractInputState):
    unshared: list = []

    def on_enter(self, curr_input_state, client):
        self.console.print("\nLooking for people who don't follow you back."
                           "\nComparing following with followers...")

        try:
            following = client.user_following(client.authenticated_user_id, client.generate_uuid()).get("users")
            followers = client.user_followers(client.authenticated_user_id, client.generate_uuid()).get("users")

            for account in following:
                for idx, follower in enumerate(followers):
                    if account.get("pk") == follower.get("pk"):
                        break  # This account follows us so we stop comparing
                    if idx == len(followers) - 1:
                        self.unshared.append(account)  # This account does not follow us back
        except ClientThrottledError:
            self.console.print("You made too many API requests, try again later.", style="red3")
            return menu_state.MenuInputState(), client

        return curr_input_state, client

    def list_info(self):
        self.console.print("Found {} people who don't follow you back!".format(len(self.unshared)))
        self.console.print("What do you want to do:"
                           "\n\t1. List all."
                           "\n\t2. List all with extended information."
                           "\n\t3. Show one-by-one. (Here you can remove people one-by-one.)"
                           "\n\t4. Show one-by-one with extended information. (Here you can remove people one-by-one.)"
                           "\n\t5. Remove all."
                           "\n\t6. Return.")

    def handle_input(self, prefix, curr_input_state, client):
        response = input(prefix)

        if response == "1":
            list_account_entries(self.unshared, "\t")
        elif response == "2":
            list_account_entries(self.unshared, "\t", client)
        elif response == "6":
            return menu_state.MenuInputState(), client

        return curr_input_state, client
