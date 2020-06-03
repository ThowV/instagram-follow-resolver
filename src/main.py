from rich.console import Console

from states import login

console = Console()

# Colors used by the console
base_color = "light_salmon3"
success_color = "spring_green3"
fail_color = "red3"


def main():
    login.start()


if __name__ == "__main__":
    main()
