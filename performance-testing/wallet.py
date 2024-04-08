from multiversx_sdk_network_providers import *
from multiversx_sdk_wallet import *
from multiversx_sdk_core import *
from pathlib import Path
import os, random
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
    selectedValidator=random.choice(users.validators)
    txn=prepareFunding(selectedValidator, receiver)
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    hashes = provider.send_transactions([txn])
    print(f"{receiver.username} wallet funded successfully")
    return list(hashes[1].values())

def saveWallet(userPEM: UserPEM, username: str):
    os.makedirs("./user_wallets", exist_ok=True)
    path="./user_wallets/{0}_wallet.pem".format(username)
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
        value=99900000000000000000000,
        gas_limit=70000,
        chain_id="local-testnet",
    )
    
    # Get the proxy network provider
    provider=ProxyNetworkProvider(os.getenv("PROXY_NETWORK"))
    
    # Get the nonce of the txn sender
    sender_on_network = provider.get_account(sender.address)
    nonce_holder = AccountNonceHolder(sender_on_network.nonce)
    transaction.nonce = nonce_holder.get_nonce_then_increment()
    
    # Sign the transaction
    transaction_computer = TransactionComputer()
    transaction.signature = sender.signer.sign(transaction_computer.compute_bytes_for_signing(transaction))
    
    return transaction