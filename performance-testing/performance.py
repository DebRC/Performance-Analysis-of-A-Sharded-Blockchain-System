from collections import defaultdict
from multiversx_sdk_network_providers import *
import os, requests

def getTxnDetails(txnHash):
    provider = ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))

    txnDetails = {
        "blockTimestamp": 0,
        "blockNonce": None,
        "hyperblockTimestamp": 0,
        "hyperblockHash": "",
        "hyperblockNonce": None,
    }

    # Get the transaction from the network
    tx_on_network = provider.get_transaction(txnHash)
    txn = tx_on_network.to_dictionary()

    # Get the process time
    txnDetails["blockTimestamp"] = txn["timestamp"]
    txnDetails["blockNonce"] = txn["blockNonce"]
    txnDetails["hyperblockHash"] = txn["hyperblockHash"]
    txnDetails["hyperblockNonce"] = txn["hyperblockNonce"]
    provider.get_
    # If the transaction is confirmed, get the confirmation time
    if txn["hyperblockHash"] != "":
        txnDetails["hyperblockTimestamp"] = (provider.get_hyperblock(txn["hyperblockHash"]))["timestamp"]
    return txnDetails

def getMiniBlocksByRound(startRound,endRound=None):
    if not endRound:
        endRound=startRound
    provider = ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    miniBlocks={}
    for round in range(startRound,endRound+1):
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/blocks/by-round/{round}"
        response = requests.get(url)
            
        blocks=response.json()['data']['blocks']
        for block in blocks:
            if block["shard"]==4294967295:
                for sb in (provider.get_hyperblock(block["hash"]))["shardBlocks"]:
                    if "miniBlockHashes" not in sb:
                        continue
                    for mbhash in sb["miniBlockHashes"]:
                        if mbhash in miniBlocks:
                            miniBlocks[mbhash]["round"].append(round)
            else:
                if "miniBlocks" not in block:
                    continue
                for mb in block["miniBlocks"]:
                    if mb["hash"] not in miniBlocks:
                        miniBlocks[mb["hash"]]={
                            "source":mb["sourceShard"],
                            "dest":mb["destinationShard"],
                            "txns":int(mb["indexOfLastTxProcessed"])-int(mb["indexOfFirstTxProcessed"])+1,
                            "round": [round]
                        }
                    else:
                        miniBlocks[mb["hash"]]["round"].append(round)
    return miniBlocks

def getThroughput(startRound,endRound):
    miniBlocks=getMiniBlocksByRound(startRound,endRound)
    txnsProcessed=0
    txnsConfirmed=0
    for block in miniBlocks:
        mb=miniBlocks[block]
        if mb["source"]==mb["dest"]:
            txnsProcessed+=mb["txns"]
            txnsConfirmed+=mb["txns"] if len(mb["round"])==2 else 0
        else:
            txnsProcessed+=mb["txns"] if len(mb["round"])==3 else 0
            txnsConfirmed+=mb["txns"] if len(mb["round"])==4 else 0
    time=(endRound-startRound+1)*int(os.getenv("ROUND_TIME"))
    return {"TPS": txnsProcessed/time, "CPS": txnsConfirmed/time}