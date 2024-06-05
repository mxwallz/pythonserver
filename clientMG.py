import socket
import sys
import datetime

hostnames = open("PROJ2-HNS.txt")
dnstable = []
for dns in hostnames:
    name = dns.split(" ")
    dnstable.append(name)
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

#while true: not necessary
for host in dnstable:
    try:
        print("attempting to connect using:", host[0])
        s.connect((server_ip, lsListenPort))
        s.sendall(host[0])

        data = s.recv(250)
        if !("Error:HOST NOT FOUND" in data):
            f.write(data)
            f.write("\n")

    finally:
        print("closing socket")
        s.close()
