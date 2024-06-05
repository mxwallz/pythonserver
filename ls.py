import socket
import sys
import datetime


def dnslookup(data, dnstable):
    print("Data: " + str(data))
    found = 0
    TSHostname = ''
    for i in dnstable:
        if("NS" in i[2][0]):
            TSHostname = i[0]
        if(str(data)==i[0]):
            print("Match found")
            found=1
            databack = str(i[0]) + " " + str(i[1])+ " " + str(i[2][0])
            connection.sendall(databack)
            print(databack)
    if(found==0):
        print("No match found, asking TS")
        databack = str(TSHostname) + " - NS"
        connection.sendall(databack)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#following is for client to read
#hostnames = open("PROJ2-HNS.txt", "r")
#dnstable = []
#for dns in hostnames:
#    name = dns.split(" ")
#    print("name is ",name)
#    #get indexError with following line: remz
#    dnstable.append([name[0],name[1],name[2].rsplit()])

#lsListen will connect w client
dnstable = []

lsListenPort = int(sys.argv[1])
ts1Hostname = sys.argv[2]
ts1ListenPort = int(sys.argv[3])
ts2Hostname = sys.argv[4]
ts2ListenPort = int(sys.argv[5])

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print("host name is:", hostname)
print(ip)
#hostNamee = socket.gethostname(localhost)
#print(hostNamee)

# Bind the socket ls from client to the port
server_address = (hostname, lsListenPort)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(3)
print(dnstable)
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    print('connection from', client_address)

    try:
        print('connection from', client_address)
        print('time of connection:',datetime.datetime.now())

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print('received {!r}'.format(data))
            if data:
                #send search to ts1 and ts2 *** split into multi synch
                dnslookup(data, dnstable)
                print('sending data back to the client')
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        print("Closing current connection")
        connection.close()
