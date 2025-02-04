from vyper import compile_code
from web3 import Web3

MY_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"


def main():
    print("Let's read in the Vyper code and deploy it")
    with open("favorites.vy", "r") as favorites_file:
        favorites_code = favorites_file.read()
        compliation_details = compile_code(
            favorites_code, output_formats=["bytecode", "abi"]
        )

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    favorites_contract = w3.eth.contract(
        bytecode=compliation_details["bytecode"], abi=compliation_details["abi"]
    )

    print("Building the transaction...")

    nonce = w3.eth.get_transaction_count(MY_ADDRESS)
    transaction = favorites_contract.constructor().build_transaction(
        {"nonce": nonce, "from": MY_ADDRESS, "gasPrice": w3.eth.gas_price}
    )
    breakpoint()


if __name__ == "__main__":
    main()
