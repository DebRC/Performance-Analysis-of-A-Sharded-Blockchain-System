import requests, os

def getNumberOfValidators():
    url = f"{os.getenv('PROXY_NETWORK')}/v1.0/node/heartbeatstatus"
    response = requests.get(url)
    if response.status_code == 200:
        res=response.json()['data']['heartbeats']
        for node in res:
            count=0
            if node["peerType"]=="validator":
                count+=1
            return count
    else:
        print("Error:", response.status_code)
        return -1
    