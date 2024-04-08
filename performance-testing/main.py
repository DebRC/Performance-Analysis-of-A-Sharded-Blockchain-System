from user import *
from transaction import *
from wallet import *
from performance import *

users = Users()
users.initiateValidators()
users.initiateOldUsers()

while(True):
    print()
    print("Enter 1 to Create Users")
    print("Enter 2 to Print Users and Validators")
    print("Enter 3 to Print Validators by Shard")
    print("Enter 4 to Print Users by Shard")
    print("Enter 5 to Send Transaction")
    print("Enter 6 to Print Sent Transactions Timestamp")
    print("Enter 7 to Print Sent Transactions Details")
    print("Enter 8 to exit")
    choice = int(input("Enter Your Choice :: "))
    print()
    if choice == 1:
        n=int(input("Enter number of users to create :: "))
        users.createUsers(n)
    elif choice == 2:
        users.printUsers()
    elif choice == 3:
        users.printValidatorByShard()
    elif choice == 4:
        users.printUserByShard()
    elif choice == 5:
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
    elif choice == 6:
        print("Printing sent Transactions :: ")
        updateTxnList()
        printTxnListTimestamp()
    elif choice == 7:
        print("Printing sent Transactions :: ")
        updateTxnList()
        printTxnListDetails()
    elif choice == 8:
        break
    else:
        print("Invalid choice")
        continue