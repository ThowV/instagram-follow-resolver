import abc

from instagram_private_api import Client
from input_state import InputState
from rich.console import Console


class AbstractInputState(abc.ABC):
    def __init__(self):
        self.console = Console()

    def on_enter(self, input_state: InputState, client: Client) -> (InputState, Client):
        return input_state, client

    @abc.abstractmethod
    def list_info(self): pass

    @abc.abstractmethod
    def handle_input(self, prefix: str, input_state: InputState, client: Client) -> (InputState, Client): pass
