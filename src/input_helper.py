import re
import datetime

from main import console, base_color


def do_input_loop(prefix: str, options_range: range) -> int:
    while True:
        response = input(prefix)

        for option in options_range:
            if response == str(option + 1):
                return int(response)

        console.print("Please pick a valid option.")


def request_extra_confirmation(prefix: str) -> bool:
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


def request_date(prefix: str) -> datetime.date:
    console.print("\nSpecify how long the account should be inactive for it to be specified as dead "
                  "in the following format: (AMOUNT)d(ay) or (AMOUNT)m(onth) or (AMOUNT)y(ear)."
                  "",
                  style=base_color)

    while True:
        response = input(prefix).lower()

        result = re.match(r"^(\d+)([mdy])$", response, re.I | re.M)

        if result:
            amount = int(result.group(1))
            datetype = result.group(2)
            today = datetime.date.today()

            # Create the new date by subtracting the given date from the current date
            if datetype == "d":
                today = today - datetime.timedelta(days=amount)
            elif datetype == "m":
                today = today - datetime.timedelta(days=amount * 31)
            elif datetype == "y":
                today = today - datetime.timedelta(days=amount * 365)

            # Check if the date is valid
            if today < datetime.date(1, 1, 1):
                console.print("Your value was too large and resulted in a time lower than zero, "
                              "please provide a valid time.")
            else:
                return today
        else:
            console.print("Please provide a valid time.")


