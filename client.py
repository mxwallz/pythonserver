import socket
import sys

# Connect the socket to the port where the server is listening
hostnames = open("PROJ2-HNS.txt")
dnstable = []
for dns in hostnames:
    name = dns.split(" ")
    dnstable.append(name)

print(dnstable)



lsHost = sys.argv[1]
lsListenPort = int(sys.argv[2])

f = open("RESOLVED.txt", "a")

for host in dnstable:

    try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = (rsHost, rsListenPort)
		print('connecting to {} port {}'.format(*server_address))
		sock.connect((server_address))
        # Send data
		message = host
		print('sending {!r}'.format(message))
		sock.sendall(message)

        # Look for the response
		amount_received = 0
		amount_expected = len(message)

		if amount_received < amount_expected:
			data = sock.recv(250)
			amount_received += len(data)
			print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()

    if("NS" in data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("No Match Found, asking TS")
        databack = data.split(" ")
        TSHostname = databack[0]
        print(TSHostname)
        server_address = (TSHostname, tsListenPort)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)
        try:
            message = host
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # Look for the response
            amount_received = 0
            amount_expected = len(message)

            if amount_received < amount_expected:
                data = sock.recv(50)
                amount_received += len(data)
                print('received {!r}'.format(data))

        finally:
            print('closing socket')
            sock.close()

    if("NS" not in data):
        if("Error" not in data):
            print("WRITTEN")
            f.write(data)
            f.write("\n")
