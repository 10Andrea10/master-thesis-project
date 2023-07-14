from utils.accounts import load_accounts_list
from utils.money import execute_deposit, withdraw
from utils.signature import sign_withdraw


PRIVATE_SIGNER_KEY = "edskRiwYcjGZY1MhC7thsL6zWg8QzywLTZH6qQVsd3GysLouUKKMzy5Cfb22XAu3qNc3Xq8pG9qyLJy1LWEYyDSHs4ocmXKpF4"


def register_deposit_withdraw_second_part():
    """Second part of the test."""
    print("Execuntin the second part of the test")

    # Load the accounts from the JSON file
    accounts_list = load_accounts_list()
    # Get the first two accounts
    account1 = accounts_list[0]

    # execute_deposit(PRIVATE_SIGNER_KEY)
    signature = sign_withdraw(account1["privateKey"], 1, 49)
    if signature is None:
        print("Error: signature1 is None")
        return
    withdraw(PRIVATE_SIGNER_KEY, 1, 49, signature.text)


register_deposit_withdraw_second_part()
