import json

def load_accounts_map():
    json_file_path = "/home/andrea/master-thesis-project/benchmarking/utils/accountsFile.json"

    with open(json_file_path, "r") as file:
        # Load the JSON data into a Python object
        data = json.load(file)
    return data

def load_accounts_list():
    accounts = load_accounts_map()
    # convert the accounts map to a list
    accounts_list = list(accounts.values())
    return accounts_list