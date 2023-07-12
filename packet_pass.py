from socket import *
from typing import Any
import pickle
from packet import *

myserverName = "192.168.1.183"

    
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive.")

while True:
    print()
    connectionSocket, addr = serverSocket.accept()
    serialized_packet = connectionSocket.recv(1024)
    if serialized_packet == b'':
        print("empty packet")
        connectionSocket.close()
        continue
    
    packet = pickle.loads(serialized_packet)
    if isinstance(packet, Packet):
        print("{} received packet from {}".format(myserverName, addr))
    else:
        print("pck_rec is not a Packet object.")
        connectionSocket.close()
        continue
    print(packet)
    
    connectionSocket.close()
