import time

from utils.register import send_register
from utils.accounts import load_accounts_list
from utils.signature import sign_register

PRIVATE_SIGNER_KEY = "edskRiwYcjGZY1MhC7thsL6zWg8QzywLTZH6qQVsd3GysLouUKKMzy5Cfb22XAu3qNc3Xq8pG9qyLJy1LWEYyDSHs4ocmXKpF4"


def register_deposit_withdraw_first_part():
    """Register the first two accounts, wait for manual deposit, execute deposit queue
    and withdraw from the first account.
    """

    # Load the accounts from the JSON file
    accounts_list = load_accounts_list()
    # Get the first two accounts
    account1 = accounts_list[0]
    account2 = accounts_list[1]

    # Register the first account
    signature1 = sign_register(account1["privateKey"], 1, account1["publicKey"])
    if signature1 is None:
        print("Error: signature1 is None")
        return
    send_register(PRIVATE_SIGNER_KEY, 1, account1["publicKey"], signature1.text )
    # Wait 10 seconds to let the blockchain register the first account
    print("Wait 10 seconds")
    time.sleep(10)
    # Register the second account
    signature2 = sign_register(account2["privateKey"], 2, account2["publicKey"])
    if signature2 is None:
        print("Error: signature2 is None")
        return
    send_register(PRIVATE_SIGNER_KEY, 2, account2["publicKey"], signature2.text )
    
    print("Execute a manual deposit of some mutez from the accounts:")
    print(f"Account 1: \n{account1['publicKey']}\n{account1['publicKeyHash']}\nposition: 1")
    print(f"Account 2: \n{account2['publicKey']}\n{account2['publicKeyHash']}\nposition: 2")
    print("And then run the second part of the test")
    


register_deposit_withdraw_first_part()
