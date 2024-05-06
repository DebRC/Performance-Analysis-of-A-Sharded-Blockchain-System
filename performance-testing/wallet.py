from multiversx_sdk_network_providers import *
from multiversx_sdk_wallet import *
from multiversx_sdk_core import *
from pathlib import Path
import os, random, time
from dotenv import load_dotenv

load_dotenv()
       
def generateWallet(username):
    mnemonic = Mnemonic.generate()
    UserWallet.from_mnemonic(mnemonic.get_text(), "password")
    secret_key = mnemonic.derive_key(0)
    public_key = secret_key.generate_public_key()
    label = Address(public_key.buffer, "erd").to_bech32()
    pem = UserPEM(label=label, secret_key=secret_key)
    saveWallet(pem, username)
    return pem
    
def fundWallet(users,receiver):
    selectedValidator=random.choice(users.validatorsAccount)
    txn=prepareFunding(selectedValidator, receiver)
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    hash = provider.send_transaction(txn)
    # print(f"{receiver.username} wallet funded successfully with transaction hash :: {hash}")

def saveWallet(userPEM: UserPEM, username: str):
    os.makedirs(os.getenv("LOG_FOLDER")+"/user_wallets", exist_ok=True)
    path=os.getenv("LOG_FOLDER")+"user_wallets/{0}_wallet.pem".format(username)
    userPEM.save(Path(path))
    return path

def prepareFunding(sender, receiver):
    """
    Prepare a transaction and
    sends between sender and receiver
    """
    # Create a transaction
    transaction = Transaction(
        sender=sender.address.to_bech32(),
        receiver=receiver.address.to_bech32(),
        value=int(os.getenv('FUND_VALUE')),
        gas_limit=int(os.getenv('GAS_LIMIT')),
        chain_id="local-testnet",
    )
    
    transaction.nonce = sender.nonce_holder.get_nonce_then_increment()
    
    # Sign the transaction
    transaction_computer = TransactionComputer()
    transaction.signature = sender.signer.sign(transaction_computer.compute_bytes_for_signing(transaction))
    
    return transaction