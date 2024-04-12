from user import *
from transaction import *
from wallet import *
from performance import *
from nodes import *
import time

users = Users()
users.initiateValidatorsAccount()
users.initiateOldUsers()

nodes = Nodes()
nodes.initiateNodes()

while(True):
    print()
    print("Enter 1 to Create Users")
    print("Enter 2 to Print Accounts")
    print("Enter 3 to Print Accounts by Shard")
    print("Enter 4 to Print Accounts Balance")
    print("Enter 5 to Print Nodes")
    print("Enter 6 to Print Nodes by Shard")
    print("Enter 7 to Send Transaction")
    print("Enter 8 to Print Sent Transactions Timestamp")
    print("Enter 9 to Print Sent Transactions Details")
    print("Enter 10 to exit")
    choice = int(input("Enter Your Choice :: "))
    print()
    if choice == 1:
        n=int(input("Enter number of users to create :: "))
        users.createUsers(n)
    elif choice == 2:
        users.printAccounts()
    elif choice == 3:
        users.printAccountsByShard()
    elif choice == 4:
        users.printAccountsBalance()
    elif choice == 5:
        nodes.printNodes()
    elif choice == 6:
        nodes.printNodesByShard()
    elif choice == 7:
        print("1. Send Mixed Transaction")
        print("2. Send Intra-Shard Transaction")
        print("3. Send Cross-Shard Transaction")
        x=int(input("Enter the type of transaction :: "))
        n=int(input("Enter number of transactions :: "))
        t=time.time()
        if x==1:
            txnsHashList=sendTxn(users, n)
        elif x==2:
            txnsHashList=sendIntraShardTxn(users, n)
        elif x==3:
            txnsHashList=sendCrossShardTxn(users, n)
        else:
            print("Invalid choice")
            continue
        saveTxnList(txnsHashList,t)
    elif choice == 8:
        print("Printing sent Transactions :: ")
        updateTxnList()
        printTxnListTimestamp()
    elif choice == 9:
        print("Printing sent Transactions :: ")
        updateTxnList()
        printTxnListDetails()
    elif choice == 10:
        break
    else:
        print("Invalid choice")
        continue