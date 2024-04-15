from collections import defaultdict
from multiversx_sdk_network_providers import *
import os

def measureTime(txnHash):
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Get the transaction from the network
    tx_on_network = provider.get_transaction(txnHash)
    txn=tx_on_network.to_dictionary()
    
    # Get the process time
    p=txn["timestamp"]
    c=0
    # If the transaction is confirmed, get the confirmation time
    if txn["hyperblockHash"]!='':
        c=(provider.get_hyperblock(txn["hyperblockHash"]))["timestamp"]
    return p,c
    
def calculateTPS():
    try:
        f=open(f"./user_wallets/txn_list.csv","r")
    except:
        return 0
    # Get the transactions
    txns=f.readlines()
    f.close()
    
    # If there are no transactions, return 0
    if not txns:
        return 0
    
    # Dictionary which maps a fixed start time 
    # to a list of end times
    txnDic=defaultdict(list)
    
    for txn in txns:
        # t = Start Time
        # p = Process Time
        # c = Confirmation Time
        t,p,c=map(float, (txn.strip().split(","))[1:])
        txnDic[t].append(p)
    
    tps=0
    for t in txnDic:
        # (Maximum of Process Time - Start Time) / Number of Transactions at that Interval
        tps+=len(txnDic[t])/(max(txnDic[t])-t)
    
    # Return the average TPS
    return tps/len(txnDic)
        
        
def calculateTCS():
    try:
        f=open(f"./user_wallets/txn_list.csv","r")
    except:
        return 0
    # Get the transactions
    txns=f.readlines()
    f.close()
    
    # If there are no transactions, return 0
    if not txns:
        return 0
    
    # Dictionary which maps a fixed start time 
    # to a list of end times
    txnDic=defaultdict(list)
    
    for txn in txns:
        # t = Start Time
        # p = Process Time
        # c = Confirmation Time
        t,p,c=map(float, (txn.strip().split(","))[1:])
        txnDic[t].append(c)
    
    tcs=0
    for t in txnDic:
        # (Maximum of Confirm Time - Start Time) / Number of Transactions at that Interval
        tcs+=len(txnDic[t])/(max(txnDic[t])-t)
    
    # Return the average TCS
    return tcs/len(txnDic)