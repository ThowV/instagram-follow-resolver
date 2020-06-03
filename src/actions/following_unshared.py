from rich.progress import Progress

from account_helper import account_following, account_followers


def compare() -> list:
    compared_hits: list = []

    # Compare and display progress
    with Progress() as progress:
        # Progress bar
        compare_task_length = len(account_following) * len(account_followers)
        compare_task = progress.add_task("Comparing...", total=compare_task_length)

        for following in account_following:
            for idx, follower in enumerate(account_followers):
                # Update the progress bar
                progress.update(compare_task, advance=1)

                # Compare following with follower
                if following.get("pk") == follower.get("pk"):
                    progress.update(compare_task, advance=len(account_followers) - idx)
                    break  # This account follows us so we stop comparing
                if idx == len(account_followers) - 1:
                    compared_hits.append(following)  # This account does not follow us back

    return compared_hits
