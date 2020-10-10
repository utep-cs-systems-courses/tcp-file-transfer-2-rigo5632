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
        file = open(fileSource, 'rb')
    except FileNotFoundError:
        print('Error: Could not find file')
        return None, False
    except PermissionError:
        print('Error: Invalid Address')
        return None, False
    return file, file.readlines()

def createPayload(key, filename, data):
    for i in range(len(data)):
        description = (key + ':' + filename + ':').encode()
        data[i] = description + data[i]
    return data

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))
while True:
    try:
        key = framedReceive(clientSocket, False).decode()
        print('Server File Key: %s' %key)
    except ConnectionResetError:
        print('Error: Lost Connection to Server')
        break
    
    userInput = str(input('> '))
    tokens = re.split(' +', userInput)

    if len(tokens) == 3:
        command = tokens[0]
        localFileName = tokens[1]
        remoteFileName = tokens[2]
    elif len(tokens) == 2:
        command = tokens[0]
        localFileName = tokens[1]
        remoteFileName = localFileName
    elif len(tokens) == 1 and tokens[0] == 'exit':
        framedSend(clientSocket, tokens[0].encode(), False)
        break
    else:
        command = None
        localFileName = None
        remoteFileName = None
    
    if len(tokens) >= 2 and command == 'put':
        file, data = fileExists(localFileName)

        data = createPayload(key, remoteFileName, data) if file else False

        if file and data:
            for payload in data:
                print('Sending: %s' %payload, end = ' ')
                framedSend(clientSocket, payload, False)
                #time.sleep(.3)
            file.close()
            key = str(int(key) + 1)
            framedSend(clientSocket, key.encode(), False)
        elif file and not data:
            print('%s has no data' %localFileName)
            framedSend(clientSocket, key.encode(), False)
        else:
            framedSend(clientSocket, key.encode(), False)
    else:
        print('Invalid Syntax!')
        print('put <local-file-name> <remote-file-name>')
        framedSend(clientSocket, key.encode(), False)
clientSocket.close()



