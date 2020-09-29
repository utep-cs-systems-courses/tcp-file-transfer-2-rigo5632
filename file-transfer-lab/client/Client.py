#! /usr/bin/python3
import os, socket, sys, re, time
sys.path.append('../../lib')
import params
sys.path.append('../../framed-echo')
from framedSock import framedReceive, framedSend

switchesVarDefaults = (
    (('-s', '--server'), 'server', '127.0.0.1:50001'),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
)

paramMap = params.parseParams(switchesVarDefaults)
server, proxy, usage = paramMap['server'], paramMap['proxy'], paramMap['usage']

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(':', server)
    serverPort = int(serverPort)
except:
    print('ERROR: Can\'t parse server:port from %s' %server)
    sys.exit(1)


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
clientSocket.connect((serverHost, serverPort))
while True:
    try:
        key = clientSocket.recv(1024).decode() if not proxy else framedReceive(clientSocket, False).decode()
        print('Server File Key: %s' %key)
    except ConnectionResetError:
        print('Error: Lost Connection to Server')
        break

    print('put <local-name> <remote-name>')
    fileName = input('> ')
    if fileName == 'exit': 
        clientSocket.send(fileName.encode()) if not proxy else framedSend(clientSocket, fileName.encode(), False)
        break
    file, data = fileExists(fileName)

    data = createPayload(key, fileName, data) if file else False

    if file:
        if data:
            for payload in data:
                print('Transfering: %s' %payload, end='')
                clientSocket.send(payload.encode()) if not proxy else framedSend(clientSocket, payload.encode(), False)
                time.sleep(.1)
            file.close()
            key = str(int(key) + 1)
            clientSocket.send(key.encode()) if not proxy else framedSend(clientSocket, key.encode(), False)
        else:
            print('%s has no data' %fileName)
            clientSocket.send(key.encode()) if not proxy else framedSend(clientSocket, key.encode(), False)
    
    if not data: key = clientSocket.send(key.encode()) if not proxy else framedSend(clientSocket, key.encode(), False)
clientSocket.close()



