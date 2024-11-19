import zmq
from random import randint
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

prev = 0

while True:
    message = socket.recv()
    decoded = message.decode() # Decode the message so our switch case can read it
    
    message = f"Received request: {decoded}"
    print(message)
    socket.send(message.encode())

    match decoded:
        case "1":
            params = int(socket.recv().decode())
            # Init arr to the size of the number the user gives
            # This way we can directly insert the value into arr in O(1)
            arr = [0] * params
            for i in range(params):
                randVal = randint(0, params - 1)  # Generate a random index in the range of the array
                while arr[randVal] != 0:  # If the slot is already taken (not 0), generate a new random value
                    randVal = randint(0, params - 1)
                arr[randVal] = i + 1  # Insert the unique number into the array
            arrJSON = json.dumps(arr) # Convert to JSON for sending
            socket.send(arrJSON.encode())
        case "2":
            params = socket.recv().decode().split('-') # Splits the array into [lowerBound, upperBound]
            lowerBound, upperBound = int(params[0]), int(params[1]) # Return vals back to integers 
            randVal = str(randint(lowerBound, upperBound)) # Lower and upper are inclusive
            while randVal == f"{prev}":
                randVal = str(randint(lowerBound, upperBound))
            prev = randVal
            socket.send(f"{randVal}".encode())
        case "Stop":
            print("Stopping RNG")
            break

