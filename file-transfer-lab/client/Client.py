#! /usr/bin/python3

import os, socket

def fileExists(fileName):
    try:
        fileSource = './files/' + fileName
        file = open(fileSource, 'r')
    except FileNotFoundError:
        print('Error: Could not find file')
        return None, False
    except PermissionError:
        print('Error: Invalid Address')
        return None, False
    return file, file.readlines()

def createPayload(key, filename, data):
    for i in range(len(data)):
        data[i] = key + ':' + filename + ':' + data[i]
    return data

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1', 50001))
continueConnection = True
print('Enter exit to quit program')

while continueConnection:
    try:
        key = clientSocket.recv(1024).decode()
    except ConnectionResetError:
        print('Error: Lost Connection to Server')
        break
    fileName = input('File name: ')
    if fileName == 'exit': 
        clientSocket.send(fileName.encode())
        break
    file, data = fileExists(fileName)

    data = createPayload(key, fileName, data) if file else False

    if file:
        if data:
            for payload in data:
                print('Sending: %s' %payload)
                clientSocket.send(payload.encode())
            file.close()
            key = str(int(key) + 1)
            clientSocket.send(key.encode())
        else:
            print('%s has no data' %fileName)
            clientSocket.send(key.encode())
    
    if not data: key = clientSocket.send(key.encode())
clientSocket.close()



