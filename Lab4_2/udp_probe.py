# udp_probe.py (simple)
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(2.0)
host = "1.1.1.1" #cloudfare dns try using 8.8.8.8 Google dns and also scanme.nmap.org
port = 53
s.sendto(b"\x00", (host, port))
try:
    data, addr = s.recvfrom(512)
    print("Received reply, service likely up")
except socket.timeout:
    print("No reply (could be closed/filtered or service not responding)")