#! /usr/bin/env python3
# Echo Client
"""
Programming language and version: Python 3.8.1
Testing Environment:
    OS: Windows
    IDE with entrance file: N/A
    Command Lines:
        python dnsclient.py 127.0.0.1 12000 host99.student.test
"""

import sys, socket, time, struct, random

# Get the IP address of server, port, hostname as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostName = sys.argv[3]

# message type (1) since it will be the request
messageType = 1

# return code on request set to 0
returnCode = 0

# no answer yet, so length is 0
answerLength = 0

# this will be the message identifier that will be send, it will increment by 1 in each loop
messageIdentifier = random.randint(1, 100)

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# add A IN to hostname
questionString = hostName + ' A IN'

# converting string into bytes
questionStringEncode = questionString.encode()

# getting the length of the questionString
questionLength = len(questionString)

# counter for timeout printing
counter = 1


print("Sending Request to " + str(host) + " " + str(port) + ":")
print('Message ID: ', messageIdentifier)
print('Question Length: ' + str(questionLength) + " bytes")
print('Answer Length: ' + str(answerLength) + " bytes")
print('Question: ' + str(questionString) + '\n')


for i in range(3):
    # packing the data that will be send
    data = struct.pack('!HHIHH', messageType, returnCode, messageIdentifier, questionLength, answerLength)\
           + questionStringEncode

    # sending the data
    clientsocket.sendto(data, (host, port))

    try:
        # set up how long the client has to wait for a response
        clientsocket.settimeout(1)

        # sleep to simulate delay in response
        time.sleep(2)

        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(1024)

        # unpacking up to 12 bytes since I don't know the size for the question
        receivedEcho = struct.unpack('!HHIHH', dataEcho[:12])

        # length of the question and length of the answer
        questionLengthFromEcho = receivedEcho[3]
        answerLengthFromEcho = receivedEcho[4]

        # Since I know the length of the question and answer I can unpack
        receivedEcho = struct.unpack('!HHIHH{}s{}s'.format(questionLengthFromEcho, answerLengthFromEcho), dataEcho)

        # Get the return code, message ID, question, and answer from the server's echo
        returnCodeFromEcho = receivedEcho[1]
        messageIdentifierFromEcho = receivedEcho[2]
        questionStringFromEcho = receivedEcho[5]
        answerSectionFromEcho = receivedEcho[6]

        # decode the question and the answer
        questionStringEchoDecoded = questionStringFromEcho.decode()
        answerSectionFromEchoDecoded = answerSectionFromEcho.decode()


        print("Received Response from " + str(host) + ", " + str(port) + ":")

        if returnCodeFromEcho == 0:
            print("Return Code: 0 (No errors)")
        else:
            print("Return Code: 1 (Name does not exist)")

        print("Message ID: ", messageIdentifierFromEcho)
        print("Question Length: " + str(questionLengthFromEcho) + ' bytes')
        print("Answer Length: " + str(answerLengthFromEcho) + ' bytes')
        print("Question: ", questionStringEchoDecoded)

        if returnCodeFromEcho == 0:
            print("Answer: ", answerSectionFromEchoDecoded)

        break

    except socket.timeout:
        if counter < 3:
            print("Request timed out ...")
            print("Sending Request to " + str(host) + " " + str(port) + ":")

        else:
            print("Request timed out ... Exiting Program.")

        counter += 1

# Close the client socket
clientsocket.close()