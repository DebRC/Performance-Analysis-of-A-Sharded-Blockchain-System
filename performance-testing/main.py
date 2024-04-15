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

# sendTxnFromSender(users)

while(True):
    print()
    print("Enter 1 to Create Users")
    print("Enter 2 to Print Accounts")
    print("Enter 3 to Print Accounts by Shard")
    print("Enter 4 to Print Accounts Balance")
    print("Enter 5 to Print Nodes")
    print("Enter 6 to Print Nodes by Shard")
    print("Enter 7 to Send Transaction")
    print("Enter 8 to Update Transactions Details")
    print("Enter 9 to Print Sent Transactions Timestamp")
    print("Enter 10 to Print Sent Transactions Details")
    print("Enter 11 to print TPR")
    print("Enter 12 to print TCR")
    print("Enter 13 to Send Max Number of Transactions")
    print("Enter 14 to exit")
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
        if x==1:
            sendTxn(users, n)
        elif x==2:
            sendIntraShardTxn(users, n)
        elif x==3:
            sendCrossShardTxn(users, n)
        else:
            print("Invalid choice")
            continue
    elif choice == 8:
        updateTxnList()
    elif choice == 9:
        printTxnListTimestamp()
    elif choice == 10:
        txnHash=input("Enter the transaction hash :: ")
        printTxnListDetails(txnHash)
    elif choice == 11:
        print("TPR ::",calculateTPR())
    elif choice == 12:
        print("TCR ::",calculateTCR())
    elif choice == 13:
        sendMaxTxns(users)
    elif choice == 14:
        break
    else:
        print("Invalid choice")
        continue