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
    print("--------------------------------")
    print("1. Create Accounts")
    print("2. Print Accounts")
    print("3. Print Accounts by Shard")
    print("4. Print Accounts Balance")
    print("--------------------------------")
    print("5. Print Nodes")
    print("6. Print Nodes by Shard")
    print("--------------------------------")
    print("7. Send Transaction")
    print("8. Update Transactions Timestamp in CSV")
    print("9. Print Sent Transactions Timestamp")
    print("10. Print a Transactions Detail")
    print("--------------------------------")
    print("11. Print TPS")
    print("12. Print TCS")
    print("--------------------------------")
    print("13. Exit")
    print("--------------------------------")
    choice = int(input("Enter Your Choice :: "))
    print()
    if choice == 1:
        n=int(input("Enter number of accounts to create :: "))
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
        print("4. Send Transaction from an Account")
        print("5. Send Max Number of Transactions")
        x=int(input("Enter the type of transaction :: "))
        print()
        if x==1:
            n=int(input("Enter number of transactions :: "))
            sendTxn(users, n)
        elif x==2:
            n=int(input("Enter number of transactions :: "))
            sendIntraShardTxn(users, n)
        elif x==3:
            n=int(input("Enter number of transactions :: "))
            sendCrossShardTxn(users, n)
        elif x==4:
            username=input("Enter the account username :: ")
            n=int(input("Enter number of transactions :: "))
            sendTxnFromAddress(users,username,n)
        elif x==5:
            sendMaxTxns(users)
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
        print("TPS ::",calculateTPS())
    elif choice == 12:
        print("TCS ::",calculateTCS())
    elif choice == 13:
        break
    else:
        print("Invalid choice")
        continue