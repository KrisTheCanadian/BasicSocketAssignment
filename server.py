import argparse
import socket
import sys

def commandLineParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='Port to listen on', type=int, required=False)
    parser.add_argument('-a', '--address', help='Address to listen on', type=str, required=False)
    parser.add_argument('-d', '--database', help='Database file to load', type=str, required=False)
    args = parser.parse_args()
    return args


def printDatabaseMenuString() -> str:
    return '''Python Db Menu
    1. Find customer
    2. Add customer
    3. Delete customer
    4. Update customer age
    5. Update customer address
    6. Update customer phone number
    7. Print report
    8. Exit
    '''

def findCustomerInDB(name: str, db: str) -> str | None:
    try:
        f = open(db, 'r')
        for line in f:
            _name = line.split('|')[0]
            if name == _name:
                return line
        return None
    except:
        print('Error loading database: ', db)
        sys.exit(1)

def addCustomerInDB(name: str, age: int, address: str, phone: str, db: str) -> str:
    try:
        f = open(db, 'a')
        f.write(f'{name}|{age}|{address}|{phone}\n')
        f.close()
        return f'{name} added to database'
    except:
        print('Error loading database: ', db)
        sys.exit(1)

def deleteCustomerInDB(name: str, db: str) -> str:
    if(findCustomerInDB(name, db) == None):
        return f'{name} not found in database'
    try:
        f = open(db, 'r')
        lines = f.readlines()
        f.close()
        f = open(db, 'w')

        for line in lines:
            _name = line.split('|')[0]
            if name == _name:
                continue
            f.write(line)
        f.close()
        return f'{name} deleted from database'
    except:
        print('Error loading database: ', db)
        sys.exit(1)


def updateCustomerAgeInDB(name: str, age: int, db: str) -> str:
    if(findCustomerInDB(name, db) == None):
        return f'{name} not found in database'
    try:
        f = open(db, 'r')
        lines = f.readlines()
        f.close()
        f = open(db, 'w')

        for line in lines:
            _name = line.split('|')[0]
            if name in _name:
                line = line.split('|')
                line[1] = age
                line = '|'.join(line)
            f.write(line)
        f.close()
        return f'{name} age updated to {age} in database'
    except:
        print('Error loading database: ', db)
        sys.exit(1)


def updateCustomerAddressInDB(name: str, address: str, db: str) -> str:
    if(findCustomerInDB(name, db) == None):
        return f'{name} not found in database'
    try:
        f = open(db, 'r')
        lines = f.readlines()
        f.close()
        f = open(db, 'w')

        for line in lines:
            if name in line:
                line = line.split('|')
                line[2] = address
                line = '|'.join(line)
            f.write(line)
        f.close()
        return f'{name} address updated to {address} in database'
    except:
        print('Error loading database: ', db)
        sys.exit(1)

def updateCustomerPhoneNumberInDB(name: str, phone: str, db: str) -> str:
    if(findCustomerInDB(name, db) == None):
        return f'{name} not found in database'
    try:
        f = open(db, 'r')
        lines = f.readlines()
        f.close()
        f = open(db, 'w')

        for line in lines:
            if name in line:
                line = line.split('|')
                line[3] = phone
                line = '|'.join(line)
            f.write(line)
        f.close()
        return f'{name} phone number updated to {phone} in database'
    except:
        print('Error loading database: ', db)
        sys.exit(1)

def printReportInDB(db: str) -> str:
    try:
        f = open(db, 'r')
        report = '** Python Db Report **\n'
        for line in f:
            report += line
        return report
    except:
        print('Error loading database: ', db)
        sys.exit(1)

def handleInput(clientSocket: socket.socket, input: str, config: dict) -> str:

    def findCustomer() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(1024).decode('utf-8')
        print('Finding customer: ', name)
        response = findCustomerInDB(name, config["database"])
        if response == None:
            return f'{name} not found in database'
        return response

    def addCustomer() -> str:

        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(1024).decode('utf-8')
        clientSocket.send('Enter customer age: '.encode('utf-8'))
        age: int = int(clientSocket.recv(1024).decode('utf-8'))
        clientSocket.send('Enter customer address: '.encode('utf-8'))
        address: str = clientSocket.recv(1024).decode('utf-8')
        clientSocket.send('Enter customer phone number: '.encode('utf-8'))
        phone: str = clientSocket.recv(1024).decode('utf-8')

        print('Adding customer: ', name)
        return addCustomerInDB(name, age, address, phone, config["database"])

    def deleteCustomer() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(1024).decode('utf-8')
        print('Deleting customer: ', name)
        return deleteCustomerInDB(name, config["database"])

    def updateCustomerAge() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(1024).decode('utf-8')
        clientSocket.send('Enter customer age: '.encode('utf-8'))
        age: int = int(clientSocket.recv(1024).decode('utf-8'))
        print('Updating customer age: ', name)
        return updateCustomerAgeInDB(name, age, config["database"])

    def updateCustomerAddress() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(1024).decode('utf-8')
        clientSocket.send('Enter customer address: '.encode('utf-8'))
        address: str = clientSocket.recv(1024).decode('utf-8')
        print('Updating customer address: ', name)
        return updateCustomerAddressInDB(name, address, config["database"])
        

    def updateCustomerPhoneNumber() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(1024).decode('utf-8')
        clientSocket.send('Enter customer phone number: '.encode('utf-8'))
        phone: str = clientSocket.recv(1024).decode('utf-8')
        print('Updating customer phone number: ', name)
        return updateCustomerPhoneNumberInDB(name, phone, config["database"])

    def printReport() -> str:
        print('Printing report')
        return printReportInDB(config["database"])


    if input == '1':
        return findCustomer()
    elif input == '2':
        return addCustomer()
    elif input == '3':
        return deleteCustomer()
    elif input == '4':
        return updateCustomerAge()
    elif input == '5':
        return updateCustomerAddress()
    elif input == '6':
        return updateCustomerPhoneNumber()
    elif input == '7':
        return printReport()
    elif input == '8':
        sys.exit(0)
    else:
        return print('Invalid input')

def handleClient(clientSocket: socket.socket, config: dict) -> None:
    selectMessage = '\nSelect an option: '
    clientSocket.send(printDatabaseMenuString().encode('utf-8') + selectMessage.encode('utf-8'))
    while True:
        data = clientSocket.recv(1024).decode('utf-8')
        if not data:
            break
        try:
            response = handleInput(clientSocket, data, config)
            print("Response: ", response)
            if response is not None:
                clientSocket.send(response.encode('utf-8') + "\n".encode('utf-8') + printDatabaseMenuString().encode('utf-8') + selectMessage.encode('utf-8'))
            else:
                clientSocket.send('Error processing request\n'.encode('utf-8')  + "\n".encode('utf-8') + printDatabaseMenuString().encode('utf-8') + selectMessage.encode('utf-8'))
        except Exception as e:
            print('Error handling input')
            print(e)
            clientSocket.send('Error handling input'.encode('utf-8') + selectMessage.encode('utf-8'))

    clientSocket.close()

def testLoadDatabase(path: str) -> dict:
    try:
        f = open(path, 'r')
    except:
        print('Error loading database: ', path)
        sys.exit(1)
    f.close()

def main():
    args: argparse.ArgumentParser = commandLineParser()

    config = {
        "port": 9999,
        "address": '127.0.0.1' ,
        "database": 'data.txt',
    }

    if(args.port):
        config['port'] = int(args.port)
    
    if(args.address):
        config['address'] = args.address

    if(args.database):
        config['database'] = args.database
    
    testLoadDatabase(config['database'])

    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((config['address'], config['port']))
    s.listen(5)

    print(f'Listening on {config["address"]}:{config["port"]}')


    while True:
        # Establish connection with client.
        clientSocket, addr = s.accept()

        print('Got connection from', addr)

        handleClient(clientSocket, config)




if __name__ == '__main__':
    main()
