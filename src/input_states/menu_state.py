from input_states import followers_unshared_state, login_state
from input_states.abstract_input_state import AbstractInputState
from input_helper import do_input_loop


class MenuInputState(AbstractInputState):
    def list_info(self):
        self.console.print("\nChoose one of the following options:", style="light_salmon3")
        self.console.print("\t1. List people who don't follow you back."
                           "\n\t2. List people who you don't follow back."
                           "\n\t3. List dead accounts that you follow."
                           "\n\t4. List dead accounts that follow you."
                           "\n\t5. Log out.")

    def handle_input(self, prefix, curr_input_state, client):
        response = do_input_loop(prefix, range(5))

        if response == 1:
            return followers_unshared_state.FollowersUnsharedInputState(), client
        elif response == 5:
            return login_state.LoginInputState(), client

        return curr_input_state, client
