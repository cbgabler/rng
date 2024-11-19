import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while True:
    defaultReq = input("Which action would you like to perform:\n"
                       "1. Provide the set of the numbers 1-your choice in a random order\n"
                       "2. Give the random number generator an upper and lower bound where it will ignore the last generated number: ")

    if defaultReq == "1" or defaultReq == "2":
        defaultReq = int(defaultReq)
        break
    else:
        print("Invalid input. Please enter either 1 or 2.\n")


match defaultReq:
    case 1:
        socket.send(b"1")
        message = socket.recv()
        print(f"Server recieved: {message}")
        numChoice = input("Please enter a value: ")
        socket.send(numChoice.encode()) # Encode converts the message into bytes
        message = socket.recv()
        arr = json.loads(message.decode())
        print(f"Recieved array: {arr}")
    case 2:
        socket.send(b"2")
        message = socket.recv()
        print(f"Server recieved: {message}")
        rangeChoice = input("Please enter a lower bound then an upper bound in the format (lowerBound-upperBound): ")
        socket.send(rangeChoice.encode())
        message = socket.recv()
        print(f"Generated random number: {message.decode()}")
    case _: # If there is any errors, the pipeline will stop
        print("Invalid case")
        message = "Stop"
        socket.send(message.encode()) 
