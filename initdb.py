# initialize database data.txt
# arguments
# -a amount of data to generate
# -f file to write to


import argparse

from faker import Faker


def commandLineParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file to write to', type=str, required=False)
    parser.add_argument('-a', '--amount', help='amount of data to generate', type=int, required=False)
    args = parser.parse_args()
    return args

def generateData(amount: int, file: str) -> None:
    # initalize faker
    fake = Faker()

    f = open(file, 'w')


    for _ in range(amount):
        user = {
            'name': fake.name(),
            'age': fake.random_int(min=0, max=100),
            'street_address': fake.street_address(),
            'phone_number': fake.phone_number(),
        }

        f.write(f"{user['name']}|{user['age']}|{user['street_address']}|{user['phone_number']}\n")

    f.close()

def main():
    args: argparse.ArgumentParser = commandLineParser()

    amount: int = 20
    file: str = 'data.txt'

    if(args.amount):
        amount = int(args.amount)

    if(args.file):
        file = args.file

    generateData(amount, file)


if __name__ == '__main__':
    main()