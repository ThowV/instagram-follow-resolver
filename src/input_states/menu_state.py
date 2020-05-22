from instagram_private_api import Client

from input_state import InputState
from input_states.abstract_input_state import AbstractInputState


class MenuInputState(AbstractInputState):
    def list_info(self):
        print("\nChoose one of the following options:",
              "\n\t1. List people who don't follow you back.",
              "\n\t2. List people who you don't follow back.",
              "\n\t3. List dead accounts that you follow.",
              "\n\t4. List dead accounts that follow you.",
              "\n\t5. Log out.")

    def handle_input(self, prefix, input_state, client) -> (InputState, Client):
        response = input(prefix)

        if response == "1":
            return InputState.FOLLOWERS_UNSHARED, client
        elif response == "5":
            return InputState.LOGIN, client

        return input_state, client
