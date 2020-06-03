from rich.console import Console

from main import console, base_color


def do_input_loop(prefix: str, options_range: range) -> int:
    console = Console()

    while True:
        result = input(prefix)

        for option in options_range:
            if result == str(option + 1):
                return int(result)

        console.print("Please pick a valid option.")


def request_extra_confirmation(prefix: str) -> bool:
    # Confirm action
    console.print("\nThis action is irreversible, are you sure?",
                  style=base_color)
    console.print("\t1. No.\n\t2. Yes.")

    response = do_input_loop(prefix, range(2))
    if response == 1:
        return False
    else:
        return True


def request_do_delay(prefix: str) -> bool:
    console.print("\nNotice: Here you are presented with 2 options, safe and quick mode."
                  "\n\tThe quick option can be used when the chosen action applies to a small amount of accounts."
                  "\n\tThe safe option should be used when the chosen action applies to many accounts."
                  "\n\tThe safe option makes sure you don't make too many API calls.",
                  "\n\tUse the quick option at your own risk!",
                  style=base_color)
    console.print("\t1. Safe.\n\t2. Quick.")

    response = do_input_loop(prefix, range(2))
    if response == 1:
        return True
    else:
        return False


def request_use_stored(prefix: str) -> bool:
    console.print("\nWe have previously retrieved account data stored, "
                  "should this be used or should it be re-retrieved?",
                  style=base_color)
    console.print("\t1. Use stored.\n\t2. Re-retrieve")

    response = do_input_loop(prefix, range(2))
    if response == 1:
        return True
    else:
        return False
