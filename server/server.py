from socket import AF_INET, SOCK_STREAM, socket, gethostbyname, gethostname 
from threading import Thread


# GLOBAL CONSTANTS
HOST = gethostbyname(gethostname()) # IP addr, 'localhost', or '127.0.0.1'
PORT = 5050 # can use any port between 0 to 65535
ADDR = (HOST, PORT)
FORMAT = "utf-8"
MAX_CONNECTION = 10
DISCONNECT_MESSAGE = 'LOGGEDOUT'
active_clients = [] # list of all currently connected users (username, client)


# listen for any incoming messages from a client
# and broadcast them to all the clients that are
# currently connected to this server
def listen_for_messages(client, username):
    connected = True
    while connected:
        response = client.recv(2048).decode(FORMAT)
        if response:
            if response == DISCONNECT_MESSAGE:
                connected = False
                broadcast_messages(f"[ADMIN] User \"{username}\" LOGGED OUT".encode())
                active_clients.remove((username, client))
            else:
                broadcast_messages(f"[{username}] {response}".encode())
        else:
            print(f"[ADMIN] The response from client is empty")
            exit(0)


# broadcase received message to users
def broadcast_messages(msg):
    print(f"[ADMIN] BROADCAST: {msg.decode()}")
    for user in active_clients:
        user[1].sendall(msg)


def client_handler(client):
    # listen for client's username
    while 1:
        username = client.recv(2048).decode(FORMAT)
        if username:
            active_clients.append((username, client))
            broadcast_messages(f"[ADMIN] User \"{username}\" LOGGED IN".encode())
            break
        else:
            print(f"[ADMIN] Client username is empty")
            exit(0)

    Thread(target=listen_for_messages, args=(client, username)).start()


def main():
    # create the socket class object
    # AF_INET: IPv4 addresses
    # SOCK_STREAM: TCP packets
    server = socket(AF_INET, SOCK_STREAM)
    try:
        # provide the server with an address in the form of
        # host IP and port
        server.bind(ADDR)
        print("[ADMIN] Server started: waiting for connection...")
    except Exception:
        print(f"[EXCEPTION] Unable to bind to host {HOST} and port {PORT}")

    # set server limit to 10
    server.listen(MAX_CONNECTION)

    # keep listening to client connections
    while True:

        try:
            # client: socket of the client (connection object)
            # address: (HOST, PORT)
            client, addr = server.accept()
            print(f"[ADMIN] Successfully connected to client {addr}")

            Thread(target=client_handler, args=(client,)).start()

        except Exception as e:
            print("[EXCEPTION]", e)
            break
    
    print("[ADMIN] Server crashed: terminating the server...")
    server.close()


if __name__ == '__main__':
    main()