from instagram_private_api import ClientThrottledError
from rich.progress import Progress

from input_states import menu_state, followers_unshared_sobo_state
from input_states.abstract_input_state import AbstractInputState
from account_helper import list_account_entries, get_account_friendships
from input_helper import do_input_loop
import account_helper


unshared: list = []


class FollowersUnsharedInputState(AbstractInputState):
    def on_enter(self, prefix, curr_input_state, client):
        use_stored = False
        do_delay = True

        # Get user options
        if account_helper.following or account_helper.followers:
            # Print info
            self.console.print("\nWe have previously retrieved account data stored,"
                               "should this be used or should it be re-retrieved?"
                               "\n\t1. Use stored.\n\t2. Re-retrieve", style="light_salmon3")

            # Get response
            response = do_input_loop(prefix, range(2))
            if response == 1:
                use_stored = True

        if use_stored is False:
            # Print info
            self.console.print("\nNotice: Here you are presented with 2 options, safe and quick mode."
                               "\n\tThe quick option can be used on accounts with around 600 followers or less."
                               "\n\tThe safe option can be used on accounts with more than 600 followers."
                               "\n\tThe safe option makes sure you don't make too many API calls.",
                               style="light_salmon3")
            self.console.print("\t1. Quick.\n\t2. Safe.")

            # Get response
            response = do_input_loop(prefix, range(2))
            if response == 1:
                do_delay = False

        # Get the following and followers
        if use_stored:
            following, followers = get_account_friendships(do_delay=do_delay)
        else:
            self.console.print("\nLooking for people who don't follow you back.", style="light_salmon3")

            try:
                following, followers = get_account_friendships(client, do_delay)
            except ClientThrottledError:
                self.console.print("You made too many API requests, try again later.", style="red3")
                return menu_state.MenuInputState(), client

        # Compare and display progress
        with Progress() as progress:
            # Progress bar
            compare_task_length = len(following) * len(followers)
            compare_task_progress = 0
            compare_task = progress.add_task("Comparing...", total=compare_task_length)

            for account in following:
                for idx, follower in enumerate(followers):
                    # Update the progress bar
                    compare_task_progress += 1
                    progress.update(compare_task, advance=1)

                    # Compare following with follower
                    if account.get("pk") == follower.get("pk"):
                        progress.update(compare_task, advance=len(followers) - idx)
                        break  # This account follows us so we stop comparing
                    if idx == len(followers) - 1:
                        unshared.append(account)  # This account does not follow us back

        return curr_input_state, client

    def list_info(self):
        self.console.print("Found {} people who don't follow you back!".format(len(unshared)))
        self.console.print("What do you want to do:"
                           "\n\t1. List all."
                           "\n\t2. Show one-by-one. (Here you can remove people one-by-one.)"
                           "\n\t3. Remove all. (This could result in many API calls.)"
                           "\n\t4. Return.")

    def handle_input(self, prefix, curr_input_state, client):
        response = do_input_loop(prefix, range(4))

        if response == 1:
            self.console.print("\nListing all accounts:", style="light_salmon3")
            list_account_entries(unshared)
        elif response == 2:
            return followers_unshared_sobo_state.FollowersUnsharedSOBOInputState(), client
        elif response == 4:
            return menu_state.MenuInputState(), client

        return curr_input_state, client
