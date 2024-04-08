from user import *
from transaction import *
from wallet import *
import time    
    
def measureTime(users):
    pass

users = Users()

users.initiateValidators()
users.initiateOldUsers()
users.createUsers(100)

users.printValidatorByShard()
users.printUserByShard()

print(time.time())
print(sendTxn(users, 10000))

while(True):
    print("Enter 1 to Create Users")
    print("Enter 2 to Print Users and Validators")
    print("Enter 3 to Print Validators by Shard")
    print("Enter 4 to Print Users by Shard")
    print("Enter 5 to print validators by shard")
    print("Enter 6 to exit")
    choice = int(input())
    if choice == 1:
        print("Enter sender username")
        sender = input()
        print("Enter receiver username")
        receiver = input()
        print("Enter amount")
        amount = int(input())
        print(sendTxn(users, amount, sender, receiver))
    elif choice == 2:
        users.printUsers()
    elif choice == 3:
        users.printValidatorByShard()
    elif choice == 4:
        users.printUserByShard()
    elif choice == 5:
        users.printValidatorByShard()
    elif choice == 6:
        break
    else:
        print("Invalid choice")
        continue
    print(time.time())
    print("Transaction successful