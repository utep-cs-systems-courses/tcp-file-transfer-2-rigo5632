#! /usr/bin/python3

import os, socket

def fileExists(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print('Error: Could not find file')
        return None, []
    return file, file.readlines()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1', 50001))
continueConnection = True

while continueConnection:
    fileName = str(input('File name: '))
    file, data = fileExists(fileName)
    print(data)
    if file and data:
        for payload in data:
            payload = (fileName + ':' + payload).encode()
            clientSocket.send(payload)
    else:
        print('Error: File has no content')
            

clientSocket.close()



