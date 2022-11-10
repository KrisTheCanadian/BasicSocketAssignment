import argparse
import socket
import sys


def commandLineParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='Port to connect on', type=int, required=False)
    parser.add_argument('-a', '--address', help='Address to connect on', type=str, required=False)
    args = parser.parse_args()
    return args


def userInput(s: socket.socket) -> None:
    while True:
        data = s.recv(1024)
        data = input(data.decode('utf-8'))

        if data == 'exit' or data == ' ':
            break

        s.send(data.encode('utf-8'))


def main():
    args: argparse.ArgumentParser = commandLineParser()

    port: int = 9999
    address: str = '127.0.0.1'

    if(args.port):
        port = int(args.port)

    if(args.address):
        address = args.address

    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, port))

    if s:
        print(f'Connected to {address}:{port}')
    else:
        print('Connection failed')
        sys.exit(1)

    print('Type "exit" to quit')


    userInput(s);
    

if __name__ == '__main__':
    main()
