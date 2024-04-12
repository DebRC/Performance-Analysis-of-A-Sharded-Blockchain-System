from multiversx_sdk_network_providers import *
from multiversx_sdk_wallet import *
from multiversx_sdk_core import *
from collections import defaultdict
import os, random,requests
from dotenv import load_dotenv
from wallet import *

load_dotenv()

class Users:
    def __init__(self):
        self.usersAccount = []
        self.validatorsAccount = []
        
    def initiateValidatorsAccount(self):
        f=open(os.getenv("PATH_TO_VALIDATOR_WALLET"),"r")
        validatorAccountList=[]
        for line in f:
            if line.startswith("-----BEGIN PRIVATE KEY"):
                bech32=(line.removeprefix("-----BEGIN PRIVATE KEY for ")).removesuffix("-----\n")
                validatorAccountList.append(bech32)
        f.close()
        for i in range(len(validatorAccountList)):
            user=User()
            user.username=f"v{i}_account"
            user.address=Address.new_from_bech32(validatorAccountList[i])
            user.signer = UserSigner.from_pem_file(Path(os.getenv("PATH_TO_VALIDATOR_WALLET")),index=i)
            user.secret_key=user.signer.secret_key.hex()
            user.public_key=user.signer.secret_key.generate_public_key().hex()
            self.validatorsAccount.append(user)
            
    def initiateOldUsers(self):
        try:
            with open("./user_wallets/user_list.csv", "r") as f:
                for line in f:
                    username, address = line.strip().split(",")
                    user = User()
                    user.username=username
                    user.address=Address.new_from_bech32(address)
                    user.signer = UserSigner.from_pem_file(Path(f"./user_wallets/{username}_wallet.pem"))
                    user.secret_key=user.signer.secret_key.hex()
                    user.public_key=user.signer.secret_key.generate_public_key().hex()
                    self.usersAccount.append(user)
        except FileNotFoundError:
            return
    
    def __generateUser(self, username):
        user=User()
        user.username = username
        pemWallet=generateWallet(username)
        user.address=Address.new_from_bech32(pemWallet.public_key.to_address("erd").to_bech32())
        user.secret_key = pemWallet.secret_key.hex()
        user.public_key = pemWallet.public_key.hex()
        user.signer = UserSigner.from_pem_file(Path(f"./user_wallets/{username}_wallet.pem"))
        fundWallet(self, user)
        return user
    
    def createUsers(self, num=1):
        for _ in range(num):
            username=str(random.randint(1,9999))
            user=self.__generateUser(username)
            self.usersAccount.append(user)
            self.saveUser(user)
            print(f"User :: {username} created successfully")
            
    def saveUser(self, user):
        os.makedirs("./user_wallets", exist_ok=True)
        f=open(f"./user_wallets/user_list.csv","a")
        f.write(f"{user.username},{user.address.to_bech32()}\n")
        f.close()

    def returnAccountsByShard(self):
        accountsByShard = defaultdict(list)
        for user in self.usersAccount:
            accountsByShard[user.getShardID()].append(user)
        for user in self.validatorsAccount:
            accountsByShard[user.getShardID()].append(user)
        return accountsByShard
    
    def printAccountsByShard(self):
        print("Printing Accounts by Shard :: ")
        accountsByShard = self.returnAccountsByShard()
        for shardID in accountsByShard:
            print(shardID, end=" :: ")
            for user in accountsByShard[shardID]:
                print(user.username, end=" ")
            print()
        
    def printAccountsBalance(self):
        print("Printing Accounts Balance :: ")
        for user in self.usersAccount:
            print(f"{user.username} :: {user.getBalance()}")
        for user in self.validatorsAccount:
            print(f"{user.username} :: {user.getBalance()}")

    def printAccounts(self):
        print("Printing Accounts :: ")
        for user in self.usersAccount:
            print(user)
        for user in self.validatorsAccount:
            print(user)

class User:
    def __init__(self):
        self.username = None
        self.address=None
        self.secret_key=None
        self.public_key=None
        self.signer=None
       
    def getShardID(self):
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/address/{self.address.to_bech32()}/shard"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']['shardID']
        else:
            print("Error:", response.status_code)
            
    def getBalance(self):
        url = f"{os.getenv('PROXY_NETWORK')}/v1.0/address/{self.address.to_bech32()}/balance"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']['balance']
        else:
            print("Error:", response.status_code)
        
    def __str__(self) -> str:
        return f"Username: {self.username}\nbech32: {self.address.to_bech32()}\nShardID: {self.getShardID()}\nSecret-Key: {self.secret_key}\nPublic-Key: {self.public_key}\nBalance: {self.getBalance()}\n"
