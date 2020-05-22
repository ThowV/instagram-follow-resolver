from instagram_private_api import Client


def list_account_entries(accounts, print_prefix, client=None):
    print("\n{}Listing all accounts:".format(print_prefix))

    header = ["Idx", "Username", "Full name", "Private", "Verified"]
    if client is not None:
        header.extend(["Followers", "Following", "Biography"])

    output = [header]

    for i, account in enumerate(accounts):
        account_info = [i + 1]

        account_info.extend(get_account_info(account))
        if client is not None:
            account_info.extend(get_extended_account_info(account, client))

        output.append(account_info)

    #print(AsciiTable(output).table, "\n")----------------------------------------------------------------------------


def get_account_info(account) -> list:
    username = account.get("username")
    full_name = account.get("full_name")

    is_private = "No"
    if account.get("is_private"):
        is_private = "Yes"

    is_verified = "No"
    if account.get("is_verified"):
        is_verified = "Yes"

    return [username, full_name, is_private, is_verified]


def get_extended_account_info(account, client: Client) -> list:
    account_extended = client.user_info(account.get("pk")).get("user")

    followers = account_extended.get("follower_count")
    following = account_extended.get("following_count")
    biography = account_extended.get("biography")

    return [followers, following, biography]
