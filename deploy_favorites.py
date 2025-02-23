from vyper import compile_code
from web3 import Web3
from dotenv import load_dotenv
import os
from encrypt_key import KEYSTORE_PATH
import getpass
from eth_account import Account

"""This project requries that a .env file in the directory with the variable below"""

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
MY_ADDRESS = os.getenv("MY_ADDRESS")


def main():
    print("Let's read in the Vyper code and deploy it")
    with open("favorites.vy", "r") as favorites_file:
        favorites_code = favorites_file.read()
        compliation_details = compile_code(
            favorites_code, output_formats=["bytecode", "abi"]
        )

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    favorites_contract = w3.eth.contract(
        bytecode=compliation_details["bytecode"], abi=compliation_details["abi"]
    )

    print("Building the transaction...")

    nonce = w3.eth.get_transaction_count(MY_ADDRESS)

    transaction = favorites_contract.constructor().build_transaction(
        {"nonce": nonce, "from": MY_ADDRESS, "gasPrice": w3.eth.gas_price}
    )
    my_key = decrypt_key()
    signed_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=my_key
    )
    print(signed_transaction)
    # breakpoint()

    tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    print(f"My Tx hash is {tx_hash}")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


def decrypt_key():
    with open(KEYSTORE_PATH) as fp:
        encrypted_account = fp.read()
        password = getpass.getpass("Enter your password: \n")
        key = Account.decrypt(encrypted_account, password)
        print("Decrypted Key!")
        return key


if __name__ == "__main__":
    main()
