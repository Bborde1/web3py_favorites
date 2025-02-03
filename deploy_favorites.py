from vyper import compile_code


def main():
    print("Let's read in the Vyper code and deploy it")
    with open("favorites.vy", "r") as favorites_file:
        favorites_code = favorites_file.read()
        compliation_details = compile_code(favorites_code, output_formats=["bytecode"])
        # print(compliation_details)


if __name__ == "__main__":
    main()
