import os
import socket
import sys
import threading

PORT = 12345

print("Welcome to NetChat!")

#username = input("Choose a username: ")
username = "fiver"

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
    print("Host ip address [", host_ip_address, "] is not an ipv4 address, NetChat terminated!")
    sys.exit()

host_ipv4_address = host_ip_address

print("HOST_IPV4_ADDRESS", host_ip_address)


def listen(host_ipv4_address):
    os.system(f"ncat -kl --recv-only  {host_ipv4_address} {PORT}")


#listening_thread = threading.Thread(target = listen, args = (host_ipv4_address,))


#listening_thread.start()
#print("Started listening")


def announce(host_ipv4_address):
    host_ipv4_network_address = host_ip_address[:host_ip_address.rfind(".") + 1]
    print("HOST_IPV4_NETWORK_ADDRESS", host_ipv4_network_address)

    for i in range(255):
        target_ipv4_address = host_ipv4_network_address + str(i)
        os.system(f"echo [{username}, {host_ipv4_address}, announce] | ncat --send-only {target_ipv4_address} 12345 2>/dev/null")


announcing_thread = threading.Thread(target = announce, args = (host_ipv4_address,))

announcing_thread.start()
print("Started announcing")

