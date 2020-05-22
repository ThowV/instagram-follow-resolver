from instagram_private_api import Client

from input_state import InputState
from input_states import login_state, menu_state, followers_unshared_state
from input_states.abstract_input_state import AbstractInputState

client: Client = None
state: InputState
input_state: AbstractInputState
prefix: str


def handle_input():
    global input_state, client

    while True:
        input_state.list_info()
        handle_switch(*input_state.handle_input(prefix, input_state, client))


def switch_state(new_state):
    global state, input_state, prefix, client
    state = new_state

    if state == InputState.LOGIN:
        input_state = login_state.LoginInputState()
        prefix = "(login): "
    elif state == InputState.MAIN_MENU:
        input_state = menu_state.MenuInputState()
        prefix = "(menu): "
    elif state == InputState.FOLLOWERS_UNSHARED:
        input_state = followers_unshared_state.FollowersUnsharedInputState()
        prefix = "(menu/followers_unshared): "

    handle_switch(*input_state.on_enter(input_state, client))


def handle_switch(new_state, new_client):
    global client

    if new_state != state:
        switch_state(new_state)
    if new_client != client:
        client = new_client


if __name__ == "__main__":
    switch_state(InputState.LOGIN)
    handle_input()
