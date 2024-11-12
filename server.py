#server listen to client connection request 

import socket
import threading #for concurrency 

HOST = '127.0.0.1'
PORT = 1234 #any port 0-65535
LISTENER_LIMIT = 5
active_clients = [] #list of all currently connected users

#keep listening for messages
def listen_for_messages(client, username):
    while 1:
        message  = client.recv(2048).decode('utf-8')
        if message:
            final_msg = username + '>>>>>' + message
            send_messages_to_all(final_msg)
        else: 
            print(f"The message send from client {username} is empty")

#function to send message to a single client
def send_messages_to_client(client, message):
    client.sendall(message.encode())


#send new msg to all connected clients
def send_messages_to_all(message):
    for user in active_clients:
        send_messages_to_client(user[1], message)

# function to handle client 
def client_handler(client):
    #server will listen for client message that will contain the username 
    while 1:
        username = client.recv(2048).decode('utf-8')
        if not username:
            print("Username cannot be empty.")
        else:
            active_clients.append((username, client))
            prompt_message = "SERVER>>>>>" + f"{username} joined the chat."
            send_messages_to_all(prompt_message)
            break
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


def main():
    #creating the server socket class object, AF_INET: IPv4 addr, SOCKET_STREAM: TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    #binding a server to a host: 
    try:
        #provide the server with an address in the form of HOST IP and PORT
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")    

    #set server limit
    server.listen(LISTENER_LIMIT)

    #keep listening to client connections
    #address[0]: client ip, address[1]: client port 
    while 1:
       client, address = server.accept()
       print(f"Successfully connected to client {address[0]} {address[1]}")
       
       #this thread will peroform the client_handler function and passing the client socket when a client is connected to the server
       threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__': #only run the main function when run the server.py directly 
    main()
