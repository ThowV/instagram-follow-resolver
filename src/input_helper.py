from rich.console import Console


def do_input_loop(prefix: str, options_range: range) -> int:
    console = Console()

    while True:
        result = input(prefix)

        for option in options_range:
            if result == str(option + 1):
                return int(result)

        console.print("Please pick a valid option.")
