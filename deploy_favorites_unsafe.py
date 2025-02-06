from vyper import compile_code
from web3 import Web3
from dotenv import load_dotenv
import os

"""This project requries that a .env file in the directory with the variable below"""

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
MY_ADDRESS = os.getenv("MY_ADDRESS")
MY_KEY = os.getenv("MY_KEY")


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
    signed_transaction = w3.eth.account.sign_transaction(
        transaction, private_key=MY_KEY
    )
    print(signed_transaction)
    # breakpoint()


if __name__ == "__main__":
    main()
