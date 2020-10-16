#! /usr/bin/python3
import os, socket, sys, re, time
sys.path.append('../lib')
import params
from framedSock import framedReceive, framedSend

# params
switchesVarDefaults = (
    (('-s', '--server'), 'server', '127.0.0.1:50001'),
    (('-lf', '--localfilename'), 'local', 'filename'),
    (('-rf', '--remotefilename'), 'remote', 'filename'),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
)

paramMap = params.parseParams(switchesVarDefaults)
server, proxy, localFilename, remoteFilename, usage = paramMap['server'], paramMap['proxy'], paramMap['local'], paramMap['remote'], paramMap['usage']

# params usage
if usage:
    params.usage()

if proxy:
    server = '127.0.0.1:50000'

try:
    serverHost, serverPort = re.split(':', server)
    serverPort = int(serverPort)
except:
    print('ERROR: Can\'t parse server:port from %s' %server)
    sys.exit(1)


# check if the file exists
def fileExists(filename):
    try:
        fileSource = './files/' + filename
        file = open(fileSource, 'rb')
    except FileNotFoundError:
        print('Error: Could not find %s' %filename)
        return None, False
    except PermissionError:
        print('Error: Invalid Address')
        return None, False
    return file, file.readlines()

# create payloads to send
def createPayload(key, filename, data):
    for i in range(len(data)):
        description = (key + ':' + filename + ':').encode()
        data[i] = description + data[i]
    return data

# Connect to client
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

try:
    key = framedReceive(clientSocket, False).decode()
    print('Server File Key: %s' %key)
except:
    print('Error: Lost Connection to server')
    sys.exit(1)

file, data = fileExists(localFilename)
if remoteFilename == 'filename':
    remoteFilename = localFilename
data = createPayload(key, remoteFilename, data) if file else False

if file and data:
    for payload in data:
        framedSend(clientSocket, payload, False)
        serverMessage = framedReceive(clientSocket, False).decode()
        if serverMessage == "Error":
            framedSend(clientSocket, key.encode(), False)
            print('Error: Server cannot re-write file. Pick another name')
            sys.exit(1)
    file.close()
    key = str(int(key) + 1)
    framedSend(clientSocket, key.encode(), False)
elif file and not data:
    print('%s has not data' %localFilename)
    framedSend(clientSocket, key.encode(), False)
else:
    framedSend(clientSocket, key.encode(), False)

clientSocket.close()



