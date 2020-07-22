#! /usr/bin/env python3
# Echo Server
"""
Programming language and version: Python 3.8.1
Testing Environment:
    OS: Windows
    IDE with entrance file: N/A
    Command Lines:
        python dnsserver.py 127.0.0.1 12000
"""

import sys, socket, struct, pathlib

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# return code informs client if the hostname was found or not
# 0 -> not found
# 1 -> found
returnCode = 0

# looking for the file in current directory
path = pathlib.Path.cwd() / 'dns-master.txt'

# opening file to read contents, split it in lines
text = path.read_text()
text = text.splitlines()

# type of message (2) since it will be the response
messageType = 2

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort))

# loop forever listening for incoming UDP messages
while True:
    data, address = serverSocket.recvfrom(1024)

    # unpacking the data received from the socket, only 12 bytes since I don't know the length of the question
    received = struct.unpack('!HHIHH', data[:12])

    # get the length of the question
    questionLength = received[3]

    # unpack with the length of the question
    received = struct.unpack('!HHIHH{}s'.format(questionLength), data)

    # selecting the message ID I received from the socket
    messageIdentifier = received[2]

    # getting the question, and decoding the question
    questionString = received[5]
    questionStringDecoded = questionString.decode()

    # initialize an answer
    answerSection = ''

    for line in text:
        if questionStringDecoded in line:
            answerSection = line
            returnCode = 0
            break
        else:
            returnCode = 1

    # length of the answerSection
    answerLength = len(answerSection)

    # encode the answer question
    answerSectionEncoded = answerSection.encode()

    # packing to respond the client
    toSend = struct.pack('!HHIHH', messageType, returnCode, messageIdentifier, questionLength, answerLength) \
             + questionString + answerSectionEncoded

    # Echo back to client
    # serverSocket.sendto(toSend, address)
