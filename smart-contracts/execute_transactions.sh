#!/bin/bash

# Check if the taquito command is installed
if ! command -v taq &>/dev/null; then
  echo "Error: taq command not found. Please install the taquito command-line tool."
  exit 1
fi

# Function to perform a single transaction
perform_transaction() {
  local to_address="$1"
  local sender="$2"
  local mutez_amount="$3"

  echo "Performing transaction: Send $mutez_amount mutez to $to_address from $sender"

  # Perform the transaction using the taquito command
  taq transfer "$to_address" --sender "$sender" --mutez "$mutez_amount" --env testing
}

# Check if the number of transactions is provided as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <number_of_transactions>"
  exit 1
fi

# Validate that the input is a positive integer
if ! [[ $1 =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: Please provide a positive integer as the number of transactions."
  exit 1
fi

number_of_transactions=$1
to_address="tz1N8ke2sXBX8J87UtNgZHZG7yaJXD9e6JoY"
sender="bob"
mutez_amount=100  # Change this value to set the amount in mutez for each transaction

# Perform the specified number of transactions
for ((i = 1; i <= number_of_transactions; i++)); do
  perform_transaction "$to_address" "$sender" "$mutez_amount"
done

echo "All transactions completed."
