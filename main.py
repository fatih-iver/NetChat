import os
import socket
import sys
print("Welcome to NetChat!")

# HOST_IPV4_ADDRESS = socket.gethostbyname(socket.gethostname())


def get_host_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


host_ip_address = get_host_ip_address()


def ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except socket.error:
        return False
    return True


if not ipv4_address(host_ip_address):
    print("Host ip address [", host_ip_address, "] is not an ipv4 address, program terminated!")
    sys.exit()

host_ipv4_address = host_ip_address

print("HOST_IPV4_ADDRESS", host_ip_address)

host_ipv4_network_address = host_ip_address[:host_ip_address.rfind(".")+1]

print("HOST_IPV4_NETWORK_ADDRESS", host_ipv4_network_address)

#os.system("ncat -l 127.0.0.1 12345")
