from time import sleep

from instagram_private_api import ClientThrottledError
from rich.progress import Progress

from input_helper import do_input_loop
from input_states import menu_state
from input_states.abstract_input_state import AbstractInputState
import input_states.followers_unshared_state as followers_unshared_state


class FollowersUnsharedRemoveAllInputState(AbstractInputState):
    def list_info(self): pass

    def handle_input(self, prefix, curr_input_state, client):
        do_delay = True

        # Confirm action
        self.console.print("\nAre you sure you want to unfollow every account you follow but does not follow you back?",
                           style="light_salmon3")
        self.console.print("\t1. No.\n\t2. Yes.")

        response = do_input_loop(prefix, range(2))
        if response == 1:
            return menu_state.MenuInputState(), client

        # Request delay option
        self.console.print("\nNotice: Here you are presented with 2 options, safe and quick mode."
                           "\n\tThe quick option can be used when you're unfollowing around 10 accounts."
                           "\n\tThe safe option should be used when you're unfollowing many accounts."
                           "\n\tThe safe option makes sure you don't make too many API calls.",
                           "\n\tUse the quick option at your own risk!",
                           style="light_salmon3")
        self.console.print("\t1. Safe.\n\t2. Quick.")

        response = do_input_loop(prefix, range(2))
        if response == 2:
            do_delay = False

        with Progress() as progress:
            index = 0
            followers_unshared_len = len(followers_unshared_state.unshared)

            # Progress bar
            compare_task = progress.add_task("Unfollowing...", total=followers_unshared_len)

            while followers_unshared_state.unshared:
                index += 1
                account = followers_unshared_state.unshared.pop(0)

                # Remove account
                try:
                    client.friendships_destroy(account.get("pk"))

                    # Update the progress bar
                    progress.update(compare_task, advance=1)

                    # Sleep so we don't do too many API calls
                    if do_delay and index != followers_unshared_len:
                        sleep(3)
                except ClientThrottledError:
                    followers_unshared_state.unshared.append(account)
                    self.console.print("You made too many API requests, try again later.", style="red3")
                    break

        return menu_state.MenuInputState(), client
