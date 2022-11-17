import argparse
import socket
import sys

BUFFER_SIZE = 1024 * 1024

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

def findCustomerInDB(name: str, db: dict) -> str | None:
    if name in db:
        return f'{name}|{db[name]["age"]}|{db[name]["address"]}|{db[name]["phone"]}'
    return None

def addCustomerInDB(name: str, age: int, address: str, phone: str, db: dict) -> str:
    if name in db:
        return f'{name} already exists in database'
    db[name] = {
        'age': age,
        'address': address,
        'phone': phone
    }
    return f'{name} added to database'

def deleteCustomerInDB(name: str, db: dict) -> str:
    if name in db:
        del db[name]
        return f'{name} deleted from database'
    return f'{name} not found in database'


def updateCustomerAgeInDB(name: str, age: int, db: dict) -> str:
    if name in db:
        db[name]['age'] = age
        return f'Updated age for {name}'
    return f'{name} not found in database'


def updateCustomerAddressInDB(name: str, address: str, db: dict) -> str:
    if name in db:
        db[name]['address'] = address
        return f'Updated address for {name}'
    return f'{name} not found in database'

def updateCustomerPhoneNumberInDB(name: str, phone: str, db: dict) -> str:
    if name in db:
        db[name]['phone'] = phone
        return f'Updated phone number for {name}'
    return f'{name} not found in database'

def printReportInDB(db: str) -> str:
    report = '\n** Python DB Content **\n'
    for customer in db:
        report += f'{customer}|{db[customer]["age"]}|{db[customer]["address"]}|{db[customer]["phone"]}'
    
    return report

def handleInput(clientSocket: socket.socket, input: str, dbInstance: dict) -> str:

    def findCustomer() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        print('Finding customer: ', name)
        response = findCustomerInDB(name, dbInstance)
        if response == None:
            return f'{name} not found in database'
        return response

    def addCustomer() -> str:

        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        clientSocket.send('Enter customer age: '.encode('utf-8'))
        age: int = int(clientSocket.recv(BUFFER_SIZE).decode('utf-8'))
        clientSocket.send('Enter customer address: '.encode('utf-8'))
        address: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        clientSocket.send('Enter customer phone number: '.encode('utf-8'))
        phone: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')

        print('Adding customer: ', name)
        return addCustomerInDB(name, age, address, phone, dbInstance)

    def deleteCustomer() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        print('Deleting customer: ', name)
        return deleteCustomerInDB(name, dbInstance)

    def updateCustomerAge() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        clientSocket.send('Enter customer age: '.encode('utf-8'))
        age: int = int(clientSocket.recv(BUFFER_SIZE).decode('utf-8'))
        print('Updating customer age: ', name)
        return updateCustomerAgeInDB(name, age, dbInstance)

    def updateCustomerAddress() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        clientSocket.send('Enter customer address: '.encode('utf-8'))
        address: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        print('Updating customer address: ', name)
        return updateCustomerAddressInDB(name, address, dbInstance)
        

    def updateCustomerPhoneNumber() -> str:
        clientSocket.send('Enter customer name: '.encode('utf-8'))
        name: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        clientSocket.send('Enter customer phone number: '.encode('utf-8'))
        phone: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        print('Updating customer phone number: ', name)
        return updateCustomerPhoneNumberInDB(name, phone, dbInstance)

    def printReport() -> str:
        return printReportInDB(dbInstance)


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
        clientSocket.send('Goodbye'.encode('utf-8'))
        return 'exit'
    else:
        clientSocket.send('Invalid Input'.encode('utf-8'))

def handleClient(clientSocket: socket.socket, databaseInstance: dict) -> None:
    selectMessage = '\nSelect an option: '
    clientSocket.send(printDatabaseMenuString().encode('utf-8') + selectMessage.encode('utf-8'))
    while True:
        data = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
        if not data:
            break
        try:
            response = handleInput(clientSocket, data, databaseInstance)
            if response is not None:
                clientSocket.send(response.encode('utf-8') + "\n".encode('utf-8') + printDatabaseMenuString().encode('utf-8') + selectMessage.encode('utf-8'))
            if response == 'exit':
                break
            else:
                clientSocket.send('Error processing request\n'.encode('utf-8')  + "\n".encode('utf-8') + printDatabaseMenuString().encode('utf-8') + selectMessage.encode('utf-8'))
        except Exception as e:
            try:
                clientSocket.send('Error handling input'.encode('utf-8') + selectMessage.encode('utf-8'))
            except Exception as e:
                break

    try:
        print('Client disconnected', clientSocket.getpeername())
    except:
        print('Client disconnected unexpectedly')

    clientSocket.close()

def testLoadDatabase(path: str) -> dict:
    try:
        f = open(path, 'r')
    except:
        print('Error loading database: ', path)
        sys.exit(1)
    
    # create a nested dictionary of customers
    customers = {}
    for line in f:
        line = line.split('|')
        customers[line[0]] = {
            'age': line[1],
            'address': line[2],
            'phone': line[3]
        }

    f.close()

    return customers

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
    
    # load database -> nested dictionary
    # instruction says to load database into memory and modify it only in memory
    databaseInstance = testLoadDatabase(config['database'])

    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((config['address'], config['port']))
    s.listen(5)

    print(f'Listening on {config["address"]}:{config["port"]}')


    while True:
        # Establish connection with client.
        clientSocket, addr = s.accept()

        print('Got connection from', addr)

        handleClient(clientSocket, databaseInstance)




if __name__ == '__main__':
    main()
