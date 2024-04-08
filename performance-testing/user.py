from multiversx_sdk_network_providers import *
from multiversx_sdk_wallet import *
from multiversx_sdk_core import *
from collections import defaultdict
import os, random,requests
from dotenv import load_dotenv
from wallet import *
from validator import *
import time

load_dotenv()

class Users:
    def __init__(self):
        self.addedUsers = []
        self.validators = []
        
    def initiateValidators(self):
        f=open(os.getenv("PATH_TO_VALIDATOR_WALLET"),"r")
        validatorList=[]
        for line in f:
            if line.startswith("-----BEGIN PRIVATE KEY"):
                bech32=(line.removeprefix("-----BEGIN PRIVATE KEY for ")).removesuffix("-----\n")
                validatorList.append(bech32)
        f.close()
        numOfVal=getNumberOfValidators()
        assert len(validatorList)==numOfVal
        for i in range(numOfVal):
            user=User()
            user.username=f"validator{i}"
            user.address=Address.new_from_bech32(validatorList[i])
            user.shardID=user.computeShardID()
            user.signer = UserSigner.from_pem_file(Path(os.getenv("PATH_TO_VALIDATOR_WALLET")),index=i)
            user.secret_key=user.signer.secret_key.hex()
            user.public_key=user.signer.secret_key.generate_public_key().hex()
            self.validators.append(user)
            
    def initiateOldUsers(self):
        # try:
        with open("./user_wallets/user_list.csv", "r") as f:
            for line in f:
                username, address = line.strip().split(",")
                user = User()
                user.username=username
                user.address=Address.new_from_bech32(address)
                user.shardID=user.computeShardID()
                user.signer = UserSigner.from_pem_file(Path(f"./user_wallets/{username}_wallet.pem"))
                user.secret_key=user.signer.secret_key.hex()
                user.public_key=user.signer.secret_key.generate_public_key().hex()
                self.addedUsers.append(user)
        # except FileNotFoundError:
        #     return
    
    def __generateUser(self, username):
        user=User()
        user.username = username
        pemWallet=generateWallet(username)
        user.address=Address.new_from_bech32(pemWallet.public_key.to_address("erd").to_bech32())
        user.secret_key = pemWallet.secret_key.hex()
        user.public_key = pemWallet.public_key.hex()
        user.shardID = user.computeShardID()
        user.signer = UserSigner.from_pem_file(Path(f"./user_wallets/{username}_wallet.pem"))
        fundWallet(self, user)
        return user
    
    def createUsers(self, num=1):
        for _ in range(num):
            username=str(random.randint(1,9999))
            user=self.__generateUser(username)
            self.addedUsers.append(user)
            self.saveUser(user)
            print(f"User :: {username} created successfully")
            
    def saveUser(self, user):
        os.makedirs("./user_wallets", exist_ok=True)
        f=open(f"./user_wallets/user_list.csv","a")
        f.write(f"{user.username},{user.address.to_bech32()}\n")
        f.close()

    def returnUserListByShard(self):
        usersByShard = defaultdict(list)
        for user in self.addedUsers:
            usersByShard[user.shardID].append(user)
        return usersByShard
    
    def returnValidatorByShard(self):
        validatorsByShard = defaultdict(list)
        for user in self.validators:
            validatorsByShard[user.shardID].append(user)
        return validatorsByShard
    
    def printUserByShard(self):
        print("Printing Users by Shard :: ")
        usersByShard = self.returnUserListByShard()
        for shardID in usersByShard:
            print(shardID, end=" ")
            for user in usersByShard[shardID]:
                print(user.username, end=" ")
            print()

    def printValidatorByShard(self):
        print("Printing Validators by Shard :: ")
        validatorsByShard = self.returnValidatorByShard()
        for shardID in validatorsByShard:
            print(shardID, end=" ")
            for user in validatorsByShard[shardID]:
                print(user.username, end=" ")
            print()
            
    def printUsers(self):
        print("Printing Added Users :: ")
        for user in self.addedUsers:
            print(user)
        print()
        print("Printing Validators :: ")
        for user in self.validators:
            print(user)
        print()

class User:
    def __init__(self):
        self.username = None
        self.address=None
        self.secret_key=None
        self.public_key=None
        self.shardID=None
        self.signer=None
       
    def computeShardID(self):
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/address/{self.address.to_bech32()}/shard"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']['shardID']
        else:
            print("Error:", response.status_code)
        
    def __str__(self) -> str:
        return f"Username: {self.username}\nbech32: {self.address.to_bech32()}\nShardID: {self.shardID}\nSecret-Key: {self.secret_key}\nPublic-Key: {self.public_key}"
