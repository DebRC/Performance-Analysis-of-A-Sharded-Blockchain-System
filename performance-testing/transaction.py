from multiversx_sdk_core import *
from multiversx_sdk_network_providers import *
from multiversx_sdk_wallet import *
from glob import glob
import os, random, sys, random
from dotenv import load_dotenv
from user import *
from performance import *

load_dotenv()

def sendTxnFromAddress(users, senderUsername, numOfTxn=1):
    """
    Sends transaction(s) from a particular address
    """
    # Limit the number of transactions to max nonce
    numOfTxn=min(numOfTxn,int(os.getenv("MAX_NONCE")))
    
    print(f"Sending {numOfTxn} Transactions...")
    
    # Get all the accounts
    accounts = users.usersAccount+users.validatorsAccount
    
    # Get the sender using the username
    sender=None
    for user in accounts:
        if user.username == senderUsername:
            sender = user
            break
    
    if not sender:
        print("Sender not found")
        return
    
    txns=[]
    for _  in range(numOfTxn):
        # Select a random receiver
        receiver: User = random.choice(accounts)
        while sender == receiver:
            receiver = random.choice(accounts)
    
        # Prepare the transaction
        txns.append(prepareTxn(sender, receiver))
    
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Send the transactions
    t=time.time()
    hashes = provider.send_transactions(txns)
    
    # Comment if performance script running in different machine
    # time.sleep(int(os.getenv("SLEEP_TIME")))
    
    # Save the transaction hash
    saveTxnList(list(hashes[1].values()),t)
    
    # Comment if performance script running in different machine
    # updateTxnList()
    
    print(f"Number of transactions sent successfully :: {hashes[0]}") 

def sendTxn(users: Users, numOfTxn=1):
    """
    Sends transaction(s) 
    between any two random users
    of any two random shards
    """
    print(f"Sending {numOfTxn} Transactions...")
    
    # Get all the accounts
    accounts = users.usersAccount+users.validatorsAccount
    txns=[]
    
    # Map for counting no of transactions (nonce) sent per account
    nonceCount=defaultdict(int)
    for _ in range(numOfTxn):
        # Select a random sender
        sender: User = random.choice(accounts)
        
        # Check if the sender has reached the maximum nonce
        tries=0
        while(nonceCount[sender.username]==int(os.getenv("MAX_NONCE")) and tries<10):
            sender: User = random.choice(accounts)
            tries+=1
        if tries==10:
            continue
        
        # Select a random receiver
        receiver: User = random.choice(accounts)
        while sender == receiver:
            receiver = random.choice(accounts)
            
        # Prepare the transaction
        txns.append(prepareTxn(sender, receiver))
        
        # Increment the nonce count
        nonceCount[sender.username]+=1
        # print(f"Sender: {sender.username}, Receiver: {receiver.username}, Nonce: {txns[-1].nonce}")
    
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Send the transactions
    t=time.time()
    hashes = provider.send_transactions(txns)
    
    # Comment if performance script running in different machine
    # time.sleep(int(os.getenv("SLEEP_TIME")))
    
    # Save the transaction hash
    saveTxnList(list(hashes[1].values()),t)
    
    # Comment if performance script running in different machine
    # updateTxnList()
    
    print(f"Number of transactions sent successfully :: {hashes[0]}") 

def sendIntraShardTxn(users: Users, numOfTxn=1):
    """
    Sends a transaction between any two random users
    of a particular shard chosen randomly
    """
    print(f"Sending {numOfTxn} Intra-Shard Transactions...")
    txns=[]
    
    shardCounts=defaultdict(int)
    
    # Get user list by shard
    usersByShard = users.returnAccountsByShard()
    
    # Map for counting no of transactions (nonce) sent per account
    nonceCount=defaultdict(int)
    for _ in range(numOfTxn):
        # Get a random shard to pick up accounts from
        getRandomShard = random.choice(list(usersByShard.keys()))
        
        # Check if there are atleast 2 users in the shard
        while(len(usersByShard[getRandomShard])<2):
            getRandomShard = random.choice(list(usersByShard.keys()))
        
        # Select a random sender
        sender: User = random.choice(usersByShard[getRandomShard])
        
        # Check if the sender has reached the maximum nonce
        tries=0
        while(nonceCount[sender.username]==int(os.getenv("MAX_NONCE")) and tries<10):
            sender: User = random.choice(usersByShard[getRandomShard])
            tries+=1
        if tries==10:
            continue
            
        # Select a random receiver
        receiver: User = random.choice(usersByShard[getRandomShard])
        while sender == receiver:
            receiver = random.choice(usersByShard[getRandomShard])
            
        # Prepare the transaction
        txns.append(prepareTxn(sender, receiver))
        
        # Increment the nonce count
        nonceCount[sender.username]+=1
        
        shardCounts[getRandomShard]+=1
        
    for shard in shardCounts:
        print("Shard :",shard,":: Transaction :",shardCounts[shard])
        
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Send the transactions
    t=time.time()
    hashes = provider.send_transactions(txns)
    
    # Comment if performance script running in different machine
    # time.sleep(int(os.getenv("SLEEP_TIME")))
    
    # Save the transaction hash
    saveTxnList(list(hashes[1].values()),t)
    
    # Comment if performance script running in different machine
    # updateTxnList()
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")

def sendCrossShardTxn(users: Users, numOfTxn=1):
    """
    Sends a transaction between any two random users
    of different shards chosen randomly
    """
    print(f"Sending {numOfTxn} Cross-Shard Transactions...")
    txns=[]
    
    # Get all the accounts
    accounts = users.usersAccount+users.validatorsAccount
    accountsByShard = users.returnAccountsByShard()
    
    shardCounts=defaultdict(int)
    
    # Map for counting no of transactions (nonce) sent per account
    nonceCount=defaultdict(int)
    for _ in range(numOfTxn):
        # Select a random sender
        sender: User = random.choice(accounts)
        
        # Check if the sender has reached the maximum nonce
        tries=0
        while(nonceCount[sender.username]==int(os.getenv("MAX_NONCE")) and tries<100):
            # Select a new sender
            sender: User = random.choice(accounts)
            tries+=1
        if tries==100:
            continue
        
        senderShardID=sender.getShardID()
        # Select a random receiver
        receiverShardID=random.choice(list(accountsByShard.keys()))

        while senderShardID==receiverShardID:
            receiverShardID=random.choice(list(accountsByShard.keys()))
        
        receiver = random.choice(accountsByShard[receiverShardID])
        
        # Prepare the transaction
        txns.append(prepareTxn(sender, receiver))
        
        # Increment the nonce count
        nonceCount[sender.username]+=1
        
        shardCounts[senderShardID]+=1
        # print(f"Sender: {sender.username}, Receiver: {receiver.username}")
    
    for shard in shardCounts:
        print("Shard :",shard,":: Transaction :",shardCounts[shard])
    
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Send the transactions
    t=time.time()
    hashes = provider.send_transactions(txns)
    
    # Comment if performance script running in different machine
    # time.sleep(int(os.getenv("SLEEP_TIME")))
    
    # Save the transaction hash
    saveTxnList(list(hashes[1].values()),t)

    # Comment if performance script running in different machine
    # updateTxnList()
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")

def sendMaxTxns(users: Users):
    """
    Sends maximum number of transactions
    """
    print("Sending Maximum Number of Transactions...")
    
    # Get all the accounts
    accounts = users.usersAccount+users.validatorsAccount
    txns=[]
    
    # Take each sender
    for sender in accounts:
        # Send maximum number of transactions
        for _ in range(int(os.getenv("MAX_NONCE"))):
            # Select a random receiver
            receiver: User = random.choice(accounts)
            while sender == receiver:
                receiver = random.choice(accounts)
                
            # Prepare the transaction
            txns.append(prepareTxn(sender, receiver))
            
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Send the transactions
    t=time.time()
    hashes = provider.send_transactions(txns)
    
    # Comment if performance script running in different machine
    # time.sleep(int(os.getenv("SLEEP_TIME")))
    
    # Save the transaction hash
    saveTxnList(list(hashes[1].values()),t)

    # Comment if performance script running in different machine
    # updateTxnList()
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")

def sendMaxIntraShardTxns(users: Users):
    """
    Sends maximum number of transactions
    """
    print("Sending Maximum Number of Intra-Shard Transactions...")
    
    accountsByShard = users.returnAccountsByShard()
    
    txns=[]
    
    # Take each sender
    for shard in accountsByShard:
        count=0
        for account in accountsByShard[shard]:
            # Send maximum number of transactions
            for _ in range(int(os.getenv("MAX_NONCE"))):
                # Select a random receiver
                receiver: User = random.choice(accountsByShard[shard])
                while account == receiver:
                    receiver = random.choice(accountsByShard[shard])
                    
                # Prepare the transaction
                txns.append(prepareTxn(account, receiver))
                count+=1
        print("Shard :",shard,":: Transaction :",count)
            
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Send the transactions
    t=time.time()
    hashes = provider.send_transactions(txns)
    
    # Comment if performance script running in different machine
    # time.sleep(int(os.getenv("SLEEP_TIME")))
    
    # Save the transaction hash
    saveTxnList(list(hashes[1].values()),t)

    # Comment if performance script running in different machine
    # updateTxnList()
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")

def sendMaxCrossShardTxns(users: Users):
    """
    Sends maximum number of transactions
    """
    print("Sending Maximum Number of Cross-Shard Transactions...")

    # Get all the accounts
    accountsByShard = users.returnAccountsByShard()
    
    txns=[]
    
    # Take each sender
    for shard in accountsByShard:
        count=0
        for sender in accountsByShard[shard]:
            # Send maximum number of transactions
            for _ in range(int(os.getenv("MAX_NONCE"))):
                # Select a random receiver
                receiverShardID=random.choice(list(accountsByShard.keys()))
                while shard==receiverShardID:
                    receiverShardID=random.choice(list(accountsByShard.keys()))
                
                receiver = random.choice(accountsByShard[receiverShardID])

                # Prepare the transaction
                txns.append(prepareTxn(sender, receiver))
                
                count+=1
        print("Shard :",shard,":: Transaction :",count)
            
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Send the transactions
    t=time.time()
    hashes = provider.send_transactions(txns)
    
    # Comment if performance script running in different machine
    # time.sleep(int(os.getenv("SLEEP_TIME")))
    
    # Save the transaction hash
    saveTxnList(list(hashes[1].values()),t)

    # Comment if performance script running in different machine
    # updateTxnList()
    
    print(f"Number of transactions sent successfully :: {hashes[0]}")

def prepareTxn(sender, receiver):
    """
    Prepare a transaction and
    sends between sender and receiver
    """
    # Create a transaction
    transaction = Transaction(
        sender=sender.address.to_bech32(),
        receiver=receiver.address.to_bech32(),
        gas_limit=int(os.getenv('GAS_LIMIT')),
        chain_id="local-testnet",
    )
    
    transaction.nonce = sender.nonce_holder.get_nonce_then_increment()
    
    # Sign the transaction
    transaction_computer = TransactionComputer()
    transaction.signature = sender.signer.sign(transaction_computer.compute_bytes_for_signing(transaction))
    
    return transaction

def saveTxnList(txnHashList,t):
    """
    Save the transaction hash
    """
    os.makedirs(os.getenv("LOG_FOLDER"), exist_ok=True)
    txnHashList=set(txnHashList)
    f=open(os.getenv("LOG_FOLDER")+"txn_list.csv","a")
    for hash in txnHashList:
        txnDetails={}
        txnDetails["txnHash"]=hash
        txnDetails["txnSentTime"]=t
        f.write(json.dumps(txnDetails)+"\n")
    f.close()

def updateTxnDetails():
    """
    Update the transaction list
    """
    try:
        f=open(os.getenv("LOG_FOLDER")+"txn_list.csv","r")
    except:
        return
    txns=f.readlines()
    f.close()
    
    lines=[]
    for txn in txns:
        txnDetails=json.loads(txn)
        
        updatedTxnDetails={}
        updatedTxnDetails["txnHash"]=txnDetails["txnHash"]
        updatedTxnDetails["txnSentTime"]=txnDetails["txnSentTime"]
        updatedTxnDetails.update(getTxnDetails(txnDetails["txnHash"]))
        
        lines.append(json.dumps(updatedTxnDetails)+"\n")        
    f=open(os.getenv("LOG_FOLDER")+"txn_list.csv","w")
    f.writelines(lines)
    f.close()
    print("Transactions Updated Successfully")
    
def printSingleTxnDetails(txnHash):
    """
    Print the transaction(s) details
    """
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    tx_on_network = provider.get_transaction(txnHash)
    print(tx_on_network.to_dictionary())

def printAllTxnDetails():
    """
    Print the transaction(s) timestamp
    """
    print("Printing Transactions Timestamps :: ")
    try:
        f=open(os.getenv("LOG_FOLDER")+"txn_list.csv","r")
    except:
        return
    txns=f.readlines()
    f.close()
    for txn in txns:
        print(txn)