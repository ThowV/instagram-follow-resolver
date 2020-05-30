from input_helper import do_input_loop
from input_states import menu_state
from input_states.abstract_input_state import AbstractInputState
from account_helper import list_account_entries
import input_states.followers_unshared_state as followers_unshared_state


class FollowersUnsharedSOBOInputState(AbstractInputState):
    def list_info(self): pass

    def handle_input(self, prefix, curr_input_state, client):
        for i, account in enumerate(followers_unshared_state.unshared):
            list_account_entries([account],  forced_idx=i+1)

            self.console.print("\t1. Get extended information.\n\t2. Unfollow.\n\t3. Next. \n\t4. Return")

            keep_loop = True
            while keep_loop:
                keep_loop = False

                response = do_input_loop(prefix, range(4))
                if response == 1:
                    keep_loop = True
                    list_account_entries([account], client, i + 1)
                elif response == 2:
                    client.friendships_destroy(account.get("pk"))
                    followers_unshared_state.unshared.remove(account)
                elif response == 3:
                    continue
                elif response == 4:
                    return followers_unshared_state.FollowersUnsharedInputState(), client

        return menu_state.MenuInputState(), client
