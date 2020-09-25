#! /usr/bin/python3

import os, socket

def fileExists(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print('Error: Could not find file')
        return None, False
    return file, file.read()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1', 50001))
continueConnection = True

while continueConnection:
    fileName = input('File name: ')
    file, data = fileExists(fileName)

    if file:
        if data:
            payload = (fileName + ':' + data)
            clientSocket.send(payload.encode())

            file.close()
            data = clientSocket.recv(1024).decode()
            print(data)
        else:
            print('%s has no data' %fileName)
clientSocket.close()



