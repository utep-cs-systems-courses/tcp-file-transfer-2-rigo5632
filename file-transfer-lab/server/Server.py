#! /usr/bin/python3

import os, socket, re, random

files = {}
key = '0'
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 50001))
serverSocket.listen(1)

connection, address = serverSocket.accept()
connection.send(key.encode())
while True:
    data = connection.recv(1024).decode()
    filename = ''
    content = ''
    if not data: break
    if data == 'exit': break

    payload = re.split(':', data)
    if len(payload) == 1:
        key = payload[0]
        files[filename] = -1
        filename = None
        content = None
        connection.send(key.encode())
    else:
        key = payload[0]
        filename = payload[1]
        content = payload[2]

    if filename not in files and filename is not None:
        fileDestination = './files/' + filename
        file = open(fileDestination, 'a')
        file.write(content)
        file.close()
    else:
        if filename:
            print('%s found in server' %filename)

connection.close()