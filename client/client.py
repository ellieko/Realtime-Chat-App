from socket import AF_INET, SOCK_STREAM, socket, gethostbyname, gethostname
from threading import Thread


# GLOBAL CONSTANTS
HOST = gethostbyname(gethostname()) # IP addr, 'localhost', or '127.0.0.1'
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = 'LOGGEDOUT'


# receive messages from server
def receive_messages_from_server(client, connected):
    while connected():
        msg = client.recv(2048).decode(FORMAT)
        print(msg)


# send messages to server
def send_messages_to_server(client, connected):
    while connected:
        msg = input("Message: (q for quit) ")
        if not msg:
            print("[ADMIN] Cannot send empty message")
            continue
        elif msg == 'q':
            msg = DISCONNECT_MESSAGE
            connected = False
        client.sendall(msg.encode())
    return connected


# send messages to the server
def communicate_to_server(client):

    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return # is the same as exit(0)?
    username = input('Enter username: ')
    if username:
        client.sendall(username.encode())
    else:
        print(f"[ADMIN] Username cannot be empty")
        return
    
    connected = True
    thread = Thread(target=receive_messages_from_server, args=(client, lambda : connected))
    thread.start()
    connected = send_messages_to_server(client, connected)
    thread.join()
    client.close()


def main(): 
    # create the socket class object
    client = socket(AF_INET, SOCK_STREAM)

    try:
        # connect to the server
        client.connect(ADDR)
        print(f"[ADMIN] Successfully connected to server {ADDR}")
    except Exception:
        print(f"[EXCEPTION] Unable to connect to server {ADDR}")

    communicate_to_server(client)


if __name__ == '__main__':
    main()