#! /usr/bin/python3
import os, socket, re, sys, time
sys.path.append('../lib')
import params
from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', '127.0.0.1:50001'),
    (('-lf', '--localfilename'), 'localFileName', 'filename'),
    (('-rf', '--remotefilename'), 'remoteFileName', 'filename'),
    (('-p', '--proxy'), 'proxy', False),
    (('-?', '--usage'), 'usage', False)
)

paramMap = params.parseParams(switchesVarDefaults)
server, proxy, localFileName, remoteFileName, usage = paramMap['server'], paramMap['proxy'], paramMap['localFileName'], paramMap['remoteFileName'], paramMap['usage']

if usage: params.usage()

try:
    serverHost, serverPort = re.split(':', server)
    serverPort = int(serverPort)
except:
    print('ERROR: Can\'t parse server:port from %s' %server)
    sys.exit(1)


def fileExists(filename):
    filename = './files/' + filename
    if not os.path.exists(filename):
        print('%s does not exist' %(filename))
        return None, False
    file = open(filename, 'rb')
    return file, file.readlines()

def createPayload(key, filename, data):
    for i in range(len(data)):
        description = (key + ':' + filename + ':').encode()
        data[i] = description + data[i]
    return data

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))
framedSocket = EncapFramedSock((clientSocket, (serverHost, serverPort)))


try:
    key = framedSocket.receive(False).decode()
    print('Server File Key: %s' %key)
except ConnectionResetError:
    print('Error: Lost Connection to Server')
    sys.exit(1)
    
file, data = fileExists(localFileName)
if remoteFileName == 'filename': remoteFileName = localFileName
data = createPayload(key, remoteFileName, data) if file else False

if file and data:
    for payload in data:
        print('Sending: %s' %payload, end = ' ')
        framedSocket.send(payload, False)
    file.close()
    key = str(int(key) + 1)
    framedSocket.send(key.encode(), False)
elif file and not data:
    print('%s has no data' %localFileName)
    framedSocket.send(key.encode(), False)
else:
    framedSocket.send(key.encode(), False)
clientSocket.close()



