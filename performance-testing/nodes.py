import requests, os
from collections import defaultdict

class Nodes:
    def __init__(self):
        self.nodes=[]
    
    def initiateNodes(self):
        f=open(os.getenv("PATH_TO_VALIDATOR_KEY"),"r")
        nodes=[]
        for line in f:
            if line.startswith("-----BEGIN PRIVATE KEY"):
                publicKey=(line.removeprefix("-----BEGIN PRIVATE KEY for ")).removesuffix("-----\n")
                nodes.append(publicKey)
        f.close()
        
        for i in range(len(nodes)):
            node=Node()
            node.name=f"node_{i}"
            node.publicKey=nodes[i]
            self.nodes.append(node)
    
    def printNodes(self):
        for node in self.nodes:
            print(node)
            
    def getNodesByShard(self):
        nodes = {"eligible":defaultdict(list),"observer":defaultdict(list),"waiting":defaultdict(list)}
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/node/heartbeatstatus"
        response = requests.get(url)
        if response.status_code == 200:
            res=response.json()['data']['heartbeats']
            for node in self.nodes:
                for resNode in res:
                    if resNode["publicKey"]==node.publicKey:
                        nodes[resNode["peerType"]][resNode["receivedShardID"]].append(node.name)
            return nodes
        else:
            print("Error:", response.status_code)
            return -1
        
    def printNodesByShard(self):
        nodesByShard = self.getNodesByShard()
        for peerType in nodesByShard:
            print(f"Printing {peerType} Nodes by Shard :: ")
            for shardID in nodesByShard[peerType]:
                print(shardID, end=" :: ")
                for node in nodesByShard[peerType][shardID]:
                    print(node, end=" ")
                print()

class Node:
    def __init__(self):
        self.name=None
        self.publicKey=None
    
    def getPeerType(self):
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/node/heartbeatstatus"
        response = requests.get(url)
        if response.status_code == 200:
            res=response.json()['data']['heartbeats']
            for node in res:
                if node["publicKey"]==self.publicKey:
                    return node["peerType"]
        else:
            print("Error:", response.status_code)
            return -1
        return None
    
    def getShardID(self):
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/node/heartbeatstatus"
        response = requests.get(url)
        if response.status_code == 200:
            res=response.json()['data']['heartbeats']
            for node in res:
                if node["publicKey"]==self.publicKey:
                    return node["receivedShardID"]
        else:
            print("Error:", response.status_code)
            return -1
        return None
    
    def __str__(self) -> str:
        return f"Node: {self.name}\nPublic Key: {self.publicKey}\n"