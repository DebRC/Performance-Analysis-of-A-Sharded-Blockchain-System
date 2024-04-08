import requests, os

def measureTime(txnHash):
    url = f"{os.getenv('PROXY_NETWORK')}/v1.0/transaction/{txnHash}?withResults=true"
    response = requests.get(url)
    p=c=-1
    if response.status_code == 200:
        res=response.json()['data']["transaction"]
        if "blockHash" in res:
            p=res["timestamp"]
        if "notarizedAtDestinationInMetaHash" in res:
            c=getConfirmationTime(res["notarizedAtDestinationInMetaHash"])
    else:
        print("Error in Getting Time:", response.status_code)
    return p,c
        
def getConfirmationTime(hyperBlockHash):
    url = f"{os.getenv('PROXY_NETWORK')}/v1.0/hyperblock/by-hash/{hyperBlockHash}"
    response = requests.get(url)
    if response.status_code == 200:
        res=response.json()['data']["hyperblock"]
        return res["timestamp"]
    else:
        print("Error in getting Confirmation Time:", response.status_code)
        return -1