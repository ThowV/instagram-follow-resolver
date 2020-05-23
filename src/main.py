from instagram_private_api import Client

from input_states import login_state, menu_state, followers_unshared_state
from input_states.abstract_input_state import AbstractInputState

client: Client
input_state: AbstractInputState
prefix: str


def start_input_receive():
    global input_state, client

    while True:
        input_state.list_info()
        handle_input(*input_state.handle_input(prefix, input_state, client))


def handle_input(new_input_state, new_client):
    global client, input_state

    if new_input_state != input_state:
        switch_input_state(new_input_state)
    if new_client != client:
        client = new_client


def switch_input_state(new_input_state):
    global input_state, prefix, client

    input_state = new_input_state

    if isinstance(input_state, login_state.LoginInputState):
        prefix = "(login): "
    elif isinstance(input_state, menu_state.MenuInputState):
        prefix = "(menu): "
    elif isinstance(input_state,  followers_unshared_state.FollowersUnsharedInputState):
        prefix = "(menu/followers_unshared): "

    handle_input(*input_state.on_enter(input_state, client))


if __name__ == "__main__":
    client = None
    prefix = "test"
    switch_input_state(login_state.LoginInputState())

    start_input_receive()
