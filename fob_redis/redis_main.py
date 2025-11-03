import socket
import threading
import time

from resp_decoder import RESPDecoder

database = {}


def handle_ping(client_connection):
    client_connection.send(b"+PONG\r\n")


def handle_echo(client_connection, args):
    client_connection.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))


def handle_rpush(client_connection, args):
    expiry = None
    # Check for "px" argument and extract expiry value
    print(f'this is list for rpush  {args[1:]}')
    if b"px" in args:
        expiry_index = args.index(b"px") + 1
        expiry = int(args[expiry_index])
        expiry = int(time.time() * 1000) + expiry
        args = args[: expiry_index - 1] + args[expiry_index + 1:]

    print("Database: ", database)
    if args[0] in database:
        value, expiry = database[args[0]]
        # value = list(value).extend(args[1:])
        database[args[0]] = (value, expiry)
    else:
        database[args[0]] = (args[1:], expiry)
    print("Database: ", database)
    client_connection.send(b"+OK\r\n")


def handle_set(client_connection, args):
    expiry = None
    # Check for "px" argument and extract expiry value
    if b"px" in args:
        expiry_index = args.index(b"px") + 1
        expiry = int(args[expiry_index])
        expiry = int(time.time() * 1000) + expiry
        args = args[: expiry_index - 1] + args[expiry_index + 1:]

    database[args[0]] = (args[1], expiry)
    client_connection.send(b"+OK\r\n")


def handle_lpop(client_connection, args):
    print(args[0])
    key = args[0]
    print("Database in Lpop:", database)
    entry = database.get(key)
    if entry is None:
        client_connection.send(b"$-1\r\n")
        return
    print(entry)
    value, expiry = entry
    if expiry is not None and expiry <= int(time.time() * 1000) or len(list(value)) == 0:
        del database[key]
        client_connection.send(b"$-1\r\n")
    else:
        values = list(value)
        value = values.pop()
        database[key] = (values, None)
        print(f'this is sybase {database}')
        print(f'this is sybase {values}')
        print(f'this is value {value}')
        client_connection.send(b"$%d\r\n%b\r\n" % (len(value), value))
        # client_connection.send(b"$%d\r\n%b\r\n" % (10,  value))


def handle_get(client_connection, args):
    print(args)
    key = args[0]
    entry = database.get(key)
    if entry is None:
        client_connection.send(b"$-1\r\n")
        return

    value, expiry = entry
    if expiry is not None and expiry <= int(time.time() * 1000):
        del database[key]
        client_connection.send(b"$-1\r\n")
    else:
        client_connection.send(b"$%d\r\n%b\r\n" % (len(value), value))


def handle_connection(client_connection):
    while True:
        try:
            command, *args = RESPDecoder(client_connection).decode()
            command = command.decode("ascii").lower()
            if command == "ping":
                handle_ping(client_connection)
            elif command == "echo":
                handle_echo(client_connection, args)
            elif command == "set":
                handle_set(client_connection, args)
            elif command == "get":
                handle_get(client_connection, args)
            elif command == "rpush":
                handle_rpush(client_connection, args)
            elif command == "lpop":
                handle_lpop(client_connection, args)
            else:
                client_connection.send(b"-ERR unknown command\r\n")
        except ConnectionError:
            break  # Stop serving if the client connection is closed


def main():
    # use reuse_port arg when running on non Windows Machine / Server
    # server_socket = socket.create_server(("", 6379),reuse_port=True)
    server_socket = socket.create_server(("", 6379))

    while True:
        client_connection, _ = server_socket.accept()  # wait for client
        threading.Thread(target=handle_connection, args=(client_connection,)).start()


if __name__ == "__main__":
    main()
