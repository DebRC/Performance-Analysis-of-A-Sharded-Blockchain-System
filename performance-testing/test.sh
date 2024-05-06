#!/bin/bash

# Check if the number of arguments provided is correct
if [ $# -ne 1 ]; then
    echo "Usage: $0 <num_transactions>"
    exit 1
fi

num_transactions=$1

# Function to send a transaction
send_transaction() {
    mxpy tx new --recall-nonce --data="Hello, World" --gas-limit=70000 --value=1000 \
    --receiver=erd16rrt4sumqwq9kjw86jex0826tm6cj8rgsmzpyhp4kse3g6v6jtvsn3mffa \
    --pem=~/Documents/RnD/MultiversX/performance-testing/user_wallets/alice.pem \
    --chain=local-testnet --proxy=http://localhost:7950 \
    --send --wait-result
}


# Loop to spawn background jobs for sending transactions
for ((i=1; i<=$num_transactions; i++)); do
    send_transaction &
    echo "Transaction $i of $num_transactions sent."
done

# Wait for all background jobs to finish
wait

echo "All transactions sent."
