import socket
import threading
from caesar import caesar_encode, caesar_decode


# threads allows us to separate code out so its not waiting for
# other code to finish before it's able to execute

HEADER = 64 # we dont know how long the next message will be, the first msg to the server each time will be length 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # gets the ip address automatically, avoids hardcoding
ADDR = (SERVER, PORT) # when we bind our server, it needs to be in tuple form
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tells the socket what type of address we'll be accepting
server.bind(ADDR)

current_connections = [] # array to keep track of connected clients

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    conn.send("[SERVER] Hello, what is your name?".encode(FORMAT))
    name_length = conn.recv(HEADER).decode(FORMAT)
    name_length = int(name_length)
    name = conn.recv(name_length).decode(FORMAT) # receive name from client
    
    conn.send(f'[SERVER] To encrypt our messages, please enter a value for the Caesar shift.'.encode(FORMAT)) # ask client for caesar shift
    caesar_shift_length = conn.recv(HEADER).decode(FORMAT) # receive length of caesar shift from client
    caesar_shift_length = int(caesar_shift_length)
    caesar_shift = conn.recv(caesar_shift_length).decode(FORMAT) # receive actual caesar shift from client
    # print(caesar_shift)
    conn.send(f'[SERVER] Caesar shift of {caesar_shift} has been received!'.encode(FORMAT))
    conn.send(f'[SERVER] Welcome to the chatroom, {name}!\n[SERVER] To disconnect, type "!dc" without the quotation marks.'.encode(FORMAT))

    while connected:
        # everytime we send a message, we need to encode it in byte format, so decode reverses that
        msg_length = conn.recv(HEADER).decode(FORMAT) # this is a blocking line of code, we wont pass it until we receive a message from the client
        if msg_length: # if this message has some content.. (if its not None)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            decrypted_msg = caesar_decode(msg, -1 * int(caesar_shift))
            print(f"[{name}] {decrypted_msg}")
            if msg == DISCONNECT_MESSAGE:
                current_connections.remove(conn)
                connected = False
                break
            
            for connection in current_connections: # this loop sends the ENCRYPTED message to all other clients
                if connection == conn: # avoids echoing the same message back to the client who sent it
                    #continue
                    pass
                connection.send(f"{name}: {msg}".encode(FORMAT))
                connection.send(f"\n[DECRYPTED] {name}: {decrypted_msg}".encode(FORMAT))

    print(f"[CLOSING CONNECTION] {addr}")
    conn.close() # close the current connection cleanly


def start():
    server.listen() # listen for connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # we will wait on this line for a new connection to the server and store the connection/address
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # when a new connection occurs, we pass that connection to handle_client, we give it the arguments specified
        thread.start()
        for connection in current_connections: # when a new client is connected, inform the other clients
            connection.send(f'[NEW CONNECTION!] {addr} connected.\n'.encode(FORMAT))
            connection.send(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n".encode(FORMAT))
        current_connections.append(conn) # adds to the list of total connections
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") # shows how many clients are connected
        

print("[STARTING] The server is starting...")
start()

# Mac:
# sudo lsof -i:5050
# kill [id]

# Windows
# netstat -ano | findstr :5050
# taskkill/pid [id] /F














