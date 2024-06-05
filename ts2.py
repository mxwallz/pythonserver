import socket
import sys

def dnslookup(data, dnstable):
    print("Data: " + str(data))
    found = 0
    for i in dnstable:
        if(str(data)==i[0]):
            print("Match found")
            print(i)
            found=1
            databack = str(i[0]) + " " + str(i[1])+ " " + str(i[2][0])
            connection.sendall(str.encode(databack))
            print(databack)
    if(found==0):
        hostname = socket.gethostname()
        print("No Host Found\n")
        #databack = str(data) + " - ERROR:HOST NOT FOUND"
        #connection.sendall(databack)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostnames = open("PROJ2-DNSTS2.txt","r")
dnstable = []
for dns in hostnames:
    name = dns.split(" ")
    dnstable.append([name[0],name[1],name[2].rsplit()])

port = int(sys.argv[1])
hostname = socket.gethostname()
# Bind the socket to the port
server_address = (hostname, port)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(50)
            response = data[:].decode("utf-8")
            print('received {!r}'.format(response))
            if response:
                dnslookup(response, dnstable)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        print("Closing current connection\n")
        connection.close()
