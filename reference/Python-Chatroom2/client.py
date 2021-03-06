import socket
import threading
import time
from caesar import caesar_encode, caesar_decode

HEADER = 64 # we dont know how long the next message will be, the first msg to the server each time will be length 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!dc"
#SERVER = "10.247.222.133"
SERVER = socket.gethostbyname(socket.gethostname()) # gets the ip address automatically, avoids hardcoding
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connected = True

# this function allows us to send messages from client to server
def send(msg): 
    message = msg.encode(FORMAT) # we have to encode messages in byte format before we send them
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # b' ' is byte space
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length) # blocking message?
    client.send(message) # sends to server bc we connected 
    #print(client.recv(2048).decode(FORMAT))

# this function runs on a thread and actively listens for new messages
def receive():
    while connected:
        time.sleep(3)
        print(client.recv(2048).decode(FORMAT))
        

def initialize():
    print(client.recv(2048).decode(FORMAT)) # server asks what the user's name is
    name = input()
    send(name) # user sends their name
    print(client.recv(2048).decode(FORMAT)) # server asks for caesar shift
    #shift = int(input())
    shift = input()
    send(shift) # user sends the shift
    print(client.recv(2048).decode(FORMAT)) # welcome message from the user
    #return int(shift)
    return shift

shift = int(initialize()) # gets the shift from initialization
thread = threading.Thread(target=receive) # creates a thread to listen to other user messages
thread.start()

while True:
    new_msg = input()
    if new_msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        connected = False # exits the thread loop
        break
    send(caesar_encode(new_msg, shift))

thread.join() # "closes" the thread
print("DISCONNECTING FROM SERVER...")


