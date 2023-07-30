import socket
from time import sleep
HOST = '127.0.0.1'
PORT = 6009


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
sleep(1)
print("SERVER STARTED....")


while True:
    client, client_address = server_socket.accept()
    print("CONNECTION ESTABLISHED SUCCESSFULLY - ", client_address)
    answer = client.recv(2048).decode()

    print(answer)

    if answer == "IMAGE":
        print(" GETTING IMAGE.....")
        file = open('server.png', 'wb')
        image = client.recv(2048)
        while image:
            file.write(image)
            image = client.recv(2048)
        file.close()
        print("*** IMAGE RECEIVED 'server.png' ***")
        print()
        sleep(1)

    elif answer == "SENDIMAGE":
        print(" SENDING IMAGE TO CLIENT....")
        file = open('server.png', 'rb')
        image_data = file.read(2050)
        while image_data:
            client.sendall(image_data)
            image_data = file.read(2050)
        sleep(1)
        image_data = file.read(2050)
        client.sendall(image_data)
        file.close()
        print("IMAGE SENT...")
        print()
        print()
        print(" *** PROCESS TERMINATED AT SERVER SIDE ***")
        quit()

    elif (answer == "EXIT"):
        quit()
