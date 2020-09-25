#! /usr/bin/python3

import os, socket, re

files = {}

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 50001))
serverSocket.listen(1)

connection, address = serverSocket.accept()
while True:
    data = connection.recv(1024).decode()
    if not data: break

    payload = re.split(':', data)
    filename = payload[0]
    content = payload[1:]

    if filename not in files:
        fileDestination = './files/' + filename
        file = open(fileDestination, 'a')
        
        for data in content:
            file.write(data)
        
        file.close()
        connection.send(('%s added to server' %filename).encode())
        files[filename] = True
    else:
        print('%s found in server' %filename)
        connection.send(('%s: duplicate file found' %filename).encode())
    connection.send(b'Ready')

connection.close()