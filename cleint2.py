import socket
import sys
import datetime
import time

hostnames = open("PROJ2-HNS.txt")
dnstable = []
for dns in hostnames:
    name = dns.split(" ")
    dnstable.append(name[0].strip())
print(dnstable)


lsHost = sys.argv[1]
lsListenPort = int(sys.argv[2])
server_ip = socket.gethostbyname(lsHost)
print(server_ip)
print(lsHost, lsListenPort)

f = open("RESOLVED.txt", "a")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("socket creation failed!")
s.connect((server_ip, lsListenPort))

for host in dnstable:
    try:
        testhost = host
        print("testhost: " + testhost)
        print("attempting to connect using:", testhost, sys.getsizeof(host[0]))
        print("connected to:", server_ip, sys.getsizeof(host))

        s.sendall(testhost)

        data = s.recv(250)
        response = data[:].decode("utf-8")

        print("WRITTEN: " + response)
        f.write(response)
        f.write("\n")
            #time.sleep(7)
            # Look for the response
            #amount_received = 0
            #amount_expected = 250

            #if amount_received < amount_expected:
            #    data = s.recv(250)
            #    amount_received += len(data)
            #    print('received {!r}'.format(data))
            #if ("Error:HOST NOT FOUND" not in data):
            #    f.write(data)
            #    f.write("\n")
    finally:
        print("Hostname Search Concluded\n")

time.sleep(10)
print("closing socket")
s.close()
