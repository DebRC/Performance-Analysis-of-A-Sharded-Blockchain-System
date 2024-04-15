from multiversx_sdk_network_providers import *
import os

def measureTime(txnHash):
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    tx_on_network = provider.get_transaction(txnHash)
    txn=tx_on_network.to_dictionary()
    p=txn["timestamp"]
    c=0
    if txn["hyperblockHash"]!='':
        c=(provider.get_hyperblock(txn["hyperblockHash"]))["timestamp"]
    return p,c
    
def calculateTPR():
    try:
        f=open(f"./user_wallets/txn_list.csv","r")
    except:
        return 0
    txns=f.readlines()
    f.close()
    if not txns:
        return 0
    t,p,c=map(float, (txns[0].strip().split(","))[1:])
    minTime=t
    maxTime=p
    for txn in txns:
        t,p,c=map(float, (txn.strip().split(","))[1:])
        if p==-1:
            continue
        minTime=min(minTime,t)
        maxTime=max(maxTime,p)
    return len(txns)/(maxTime-minTime)
        
        
def calculateTCR():
    try:
        f=open(f"./user_wallets/txn_list.csv","r")
    except:
        return 0
    txns=f.readlines()
    f.close()
    if not txns:
        return 0
    t,p,c=map(float, (txns[0].strip().split(","))[1:])
    minTime=t
    maxTime=c
    for txn in txns:
        t,p,c=map(float, (txn.strip().split(","))[1:])
        if c==-1:
            continue
        minTime=min(minTime,t)
        maxTime=max(maxTime,c)
    return len(txns)/(maxTime-minTime)