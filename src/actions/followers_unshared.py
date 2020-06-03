from rich.progress import Progress

from account_helper import account_following, account_followers


def compare() -> list:
    compared_hits: list = []

    # Compare and display progress
    with Progress() as progress:
        # Progress bar
        compare_task_length = len(account_following) * len(account_followers)
        compare_task = progress.add_task("Comparing...", total=compare_task_length)

        for follower in account_followers:
            for idx, following in enumerate(account_following):
                # Update the progress bar
                progress.update(compare_task, advance=1)

                # Compare following with follower
                if follower.get("pk") == following.get("pk"):
                    progress.update(compare_task, advance=len(account_following) - idx)
                    break  # We follow this account so we stop comparing
                if idx == len(account_following) - 1:
                    compared_hits.append(follower)  # We do not follow this account back

    return compared_hits
