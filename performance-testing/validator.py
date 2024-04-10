import requests, os
from collections import defaultdict

def getNumberOfEligibleValidators():
    url = f"{os.getenv('PROXY_NETWORK')}/v1.0/node/heartbeatstatus"
    response = requests.get(url)
    if response.status_code == 200:
        res=response.json()['data']['heartbeats']
        count=0
        for node in res:
            if node["peerType"]=="eligible":
                count+=1
        return count
    else:
        print("Error:", response.status_code)
        return -1
    
def getValidatorsByShard():
    validatorsByShard = {"eligible":defaultdict(list),"observer":defaultdict(list),"waiting":defaultdict(list)}
    url = f"{os.getenv('PROXY_NETWORK')}/v1.0/node/heartbeatstatus"
    response = requests.get(url)
    if response.status_code == 200:
        res=response.json()['data']['heartbeats']
        i=0
        for node in res:
            validatorsByShard[node["peerType"]][node["computedShardID"]].append(f"node{i}")
            i+=1
        return validatorsByShard
    else:
        print("Error:", response.status_code)
        return -1

def printValidatorsByShard():
    validatorsByShard = getValidatorsByShard()
    for peerType in validatorsByShard:
        print(f"Printing {peerType} Validators by Shard :: ")
        for shardID in validatorsByShard[peerType]:
            print(shardID, end=" :: ")
            for user in validatorsByShard[peerType][shardID]:
                print(user, end=" ")
            print()

    
# UNDONEEEE
# def getValidatorDetails():
#     url = f"{os.getenv('PROXY_NETWORK')}/v1.0/node/heartbeatstatus"
#     response = requests.get(url)
#     if response.status_code == 200:
#         res=response.json()['data']['heartbeats']
#         for node in res:
#             if node["peerType"]=="eligible":
#                 count+=1
#         return count
#     else:
#         print("Error:", response.status_code)
#         return -1
    