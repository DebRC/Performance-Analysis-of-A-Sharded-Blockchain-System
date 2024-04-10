from multiversx_sdk_core import *
from multiversx_sdk_network_providers import *
from multiversx_sdk_wallet import *
from glob import glob
import os, random, sys, random
from dotenv import load_dotenv
from user import User
from performance import *

load_dotenv()

def sendTxn(users, numOfTxn=1):
    """
    Sends transaction(s) 
    between any two random users
    of any two random shards
    """
    print(f"Sending {numOfTxn} Transactions...")
    addedUsers = users.addedUsers
    txns=[]
    for _ in range(numOfTxn):
        # Select a random sender and receiver
        sender: User = random.choice(addedUsers)
        receiver: User = random.choice(addedUsers)
        while sender == receiver:
            receiver = random.choice(addedUsers)
        
        txns.append(prepareTxn(sender, receiver))
        # print(f"Sender: {sender.username}, Receiver: {receiver.username}")
    
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    hashes = provider.send_transactions(txns)
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")
    return list(hashes[1].values())

def sendIntraShardTxn(users, numOfTxn=1):
    """
    Sends a transaction between any two random users
    of a particular shard chosen randomly
    """
    print(f"Sending {numOfTxn} Transactions...")
    txns=[]
    for _ in range(numOfTxn):
        # Get a random shard to pick up accounts from
        usersByShard = users.returnUserListByShard()
        getRandomShard = random.choice(list(usersByShard.keys()))
        
        # Check if there are atleast 2 users in the shard
        while(len(usersByShard[getRandomShard])<2):
            getRandomShard = random.choice(list(usersByShard.keys()))
        
        # Select a random sender and receiver
        sender: User = random.choice(usersByShard[getRandomShard])
        receiver: User = random.choice(usersByShard[getRandomShard])
        while sender == receiver:
            receiver = random.choice(usersByShard[getRandomShard])
            
        txns.append(prepareTxn(sender, receiver))
        # print(f"Sender: {sender.username}, Receiver: {receiver.username}")
        
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    hashes = provider.send_transactions(txns)
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")
    return list(hashes[1].values())

def sendCrossShardTxn(users, numOfTxn=1):
    """
    Sends a transaction between any two random users
    of different shards chosen randomly
    """
    print(f"Sending {numOfTxn} Transactions...")
    txns=[]
    addedUsers = users.addedUsers
    for _ in range(numOfTxn):
        # Select a random sender and receiver
        sender: User = random.choice(addedUsers)
        receiver: User = random.choice(addedUsers)
        while sender.shardID == receiver.shardID:
            receiver = random.choice(addedUsers)
        # print(f"Sender: {sender.username}, Receiver: {receiver.username}")
        
        txns.append(prepareTxn(sender, receiver))
    
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    hashes = provider.send_transactions(txns)
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")
    return list(hashes[1].values())

def prepareTxn(sender, receiver):
    """
    Prepare a transaction and
    sends between sender and receiver
    """
    # Create a transaction
    transaction = Transaction(
        sender=sender.address.to_bech32(),
        receiver=receiver.address.to_bech32(),
        gas_limit=70000,
        chain_id="local-testnet",
    )
    
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Get the nonce of the txn sender
    sender_on_network = provider.get_account(sender.address)
    nonce_holder = AccountNonceHolder(sender_on_network.nonce)
    transaction.nonce = nonce_holder.get_nonce_then_increment()
    
    # Sign the transaction
    transaction_computer = TransactionComputer()
    transaction.signature = sender.signer.sign(transaction_computer.compute_bytes_for_signing(transaction))
    
    return transaction

def saveTxnList(txnHashList,t):
    """
    Save the transaction hash
    """
    os.makedirs("./user_wallets", exist_ok=True)
    f=open(f"./user_wallets/txn_list.csv","a")
    for hash in txnHashList:
        f.write(f"{hash},{t},-1,-1\n")
    f.close()

def updateTxnList():
    """
    Update the transaction list
    """
    try:
        f=open(f"./user_wallets/txn_list.csv","r")
    except:
        return
    txns=f.readlines()
    f.close()
    f=open(f"./user_wallets/txn_list.csv","w")
    for txn in txns:
        txnHash,t,p,c=txn.strip().split(",")
        p,c=measureTime(txnHash)
        f.write(f"{txnHash},{t},{p},{c}\n")
    f.close()
    
def printTxnListDetails():
    """
    Print the transaction(s) details
    """
    print("Printing Transactions Details :: ")
    try:
        f=open(f"./user_wallets/txn_list.csv","r")
    except:
        return
    txns=f.readlines()
    f.close()
    for txn in txns:
        txnHash,t,p,c=txn.strip().split(",")
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/transaction/{txnHash}?withResults=true"
        response = requests.get(url)

def printTxnListTimestamp():
    """
    Print the transaction(s) timestamp
    """
    print("Printing Transactions Timestamps :: ")
    try:
        f=open(f"./user_wallets/txn_list.csv","r")
    except:
        return
    txns=f.readlines()
    f.close()
    for txn in txns:
        txnHash,t,p,c=txn.strip().split(",")
        print(txnHash,"::",t,"->",p,"->",c)
    