# importing the socket module to create socket for the host
import socket
#importing the threading module to create threads for each connection
import threading
#importing the os module to commuciate with the current operating system
import os
#useful for parsing database file of the local server.
import json
#this will help us create different random values using the string module
import random
import string

# Define constants for the server
HOST = 'localhost'
PORT = 5555
# this parameter is only there to help business
MAX_CLIENTS = 10

# Create a dictionary to hold all connected clients and their usernames
connectedClients = {}
usernameToSocket = {}
usernamesSet = set()

#next check if the usernames are already set in the network by checking 
#local database of the server
if not os.path.isfile("database.json"):
    open("database.json", 'w').close()

database    = open("database.json", "r")
data        = str(database.read())
database    = json.loads( data if data else "{}" )
#this is the total registered users in the database and their info
users       = database["login"] if "login" in database else list()
#this hel the system detect if the user name entered is the already
#registered one or a new one.
usernamesSet = set()
#this maps the users with their corresponding password
usersMap     = dict()

#doing the pre mapping for the already registered users.
for user in users :
    if "username" in user :
        usernamesSet.add( user["username"] )
        if "userpwd" in user :
            usersMap[user["username"]] = user["userpwd"]






# Create a socket object
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
serverSocket.bind((HOST, PORT))

# Listen for incoming connections
serverSocket.listen(MAX_CLIENTS)


# Function to handle incoming client connections
def handleClient(clientSocket, clientAddress):
    # Prompt the client for their username
    clientSocket.send("zPlease enter your username: ".encode())
    username = clientSocket.recv(1024).decode()
    password = False
    isRegister = True               
                
    while username in usernamesSet:
        # clientSocket.send(
            # "zThis username is already taken, please choose another one: ".encode())
        
        # username = clientSocket.recv(1024).decode()
        clientSocket.send(
            "zThis username is already taken, please choose another one or enter your password. Enter your password with this %% sign before the password and the username with this ## sign before the username to register your account with this server: ".encode())
        checkname = clientSocket.recv(1024).decode()
                
        if "##" in checkname :
            username    = checkname.split("##")
            username    = username[1]
            clientSocket.send(
                "zPlease Enter the Password Associated With this User Name: ".encode())
            password = clientSocket.recv(1024).decode()
                    
        elif "%%" in checkname :
            password    = checkname.split("%%")
            password    = password[1]
            isRegister  = False
                
        else :
            clientSocket.send(
                "zMessage Format Unsupported. Please re-enter your password with the leading %% or username with leading ## ".encode())
            checkname = clientSocket.recv(1024).decode()
                    
                
        if password and not isRegister :
            #compare the passwords
            while "userpwd" in user and user["userpwd"] != password :
                clientSocket.send(
                    "zYou Have Entered a Wrong Password, Please Try Again: ".encode())
                password = clientSocket.recv(1024).decode()
    
    #register the user 
    if not username in usernamesSet and not password :                
        clientSocket.send("zPlease enter your password: ".encode())
        password        = clientSocket.recv(1024).decode()
        clientSocket.send("zPlease enter your Full Name: ".encode())
        fullname        = clientSocket.recv(1024).decode()
        newUser         = dict()
        UID     = random.choices( string.ascii_uppercase + string.digits, k=10)
        UID     = ''.join(UID)
        newUser["username"]     = username
        newUser["fullname"]     = fullname
        newUser["USERID"]       = UID
        newUser["userpwd"]      = password
        newUser["usertype"]     = "USER"
        newUser["status"]       = "active"
        

    # Add the client to the dictionary of connected clients
    connectedClients[clientSocket] = username
    usernameToSocket[username] = clientSocket
    usernamesSet.add(username)
    my_string = ', '.join(str(element) for element in usernamesSet)
    
    with open('usernames.txt', 'w') as file:
        file.write(my_string)

    # Send a welcome message to the client
    clientSocket.send(f"wWelcome to the MaxChat room, {username}!\n".encode())
    clientSocket.send(f"O{','.join(usernamesSet)}".encode())
    for c in connectedClients.keys():
        if c != clientSocket:
            c.send(f"o{username}".encode())

    while True:
        try:
            # Receive data from the client
            data = clientSocket.recv(1024).decode()

            if not data:
                break

            if data.startswith("@"):
                splitted = data.split(' ')
                currUsername = splitted[0]
                currUsername = currUsername[1:]
                if currUsername in usernamesSet:
                    message = ' '.join(splitted[1:])
                    usernameToSocket[currUsername].send(
                        f"d{connectedClients[clientSocket]} (private): {message}".encode())
            else:
                # Broadcast the message to all connected clients
                for c in connectedClients.keys():
                    if c != clientSocket:
                        c.send(
                            f"n{connectedClients[clientSocket]}: {data}".encode())
        except Exception as e:
            print(e)
            # Remove the client from the dictionary of connected clients

            del connectedClients[clientSocket]
            del usernameToSocket[username]
            usernamesSet.remove(username)

            clientSocket.close()
            for c in connectedClients.keys():
                c.send(
                    f"o{username}".encode())
            break



# Main loop to handle incoming connections
while True:
    # Accept incoming connections
    clientSocket, clientAddress = serverSocket.accept()
    print( clientSocket )
    # Create a new thread to handle the client connection
    clientThread = threading.Thread(
        target=handleClient, args=(clientSocket, clientAddress))
    clientThread.start()
