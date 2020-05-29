import abc

from instagram_private_api import Client
from rich.console import Console


class AbstractInputState(abc.ABC):
    def __init__(self):
        self.console = Console()

    def on_enter(self, prefix: str, curr_input_state, client: Client):
        return curr_input_state, client

    @abc.abstractmethod
    def list_info(self): pass

    @abc.abstractmethod
    def handle_input(self, prefix: str, curr_input_state, client: Client): pass
