import os
import socket
import sys
import threading

print("Welcome to NetChat!")

port = 12345
os.environ["netchat_port"] = str(port)


username = input("Choose a username: ")
os.environ["netchat_username"] = username


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
    print("Host ip address [{host_ip_address}] is not an ipv4 address, NetChat terminated!")
    sys.exit()

host_ipv4_address = host_ip_address

print("HOST_IPV4_ADDRESS", host_ipv4_address)

os.environ["netchat_ipv4"] = host_ipv4_address



def listen():
    os.system("sh listenc")

listening_thread = threading.Thread(target = listen)
listening_thread.start()


def announce():
    host_ipv4_network_address = host_ipv4_address[:host_ipv4_address.rfind(".") + 1]
    subnet_digits = int(host_ipv4_address[host_ipv4_address.rfind(".") + 1:])

    for i in range(254):
        if i != subnet_digits:
            target_ipv4_address = host_ipv4_network_address + str(i)
            os.system(f"echo [$netchat_username, $netchat_ipv4, announce] | ncat {target_ipv4_address} $netchat_port 2>/dev/null")


announcing_thread = threading.Thread(target = announce)
announcing_thread.start()
print("Started announcing")

while True:
    command = input("(message/online/exit):").strip()

    if command == "exit":
        break
    elif command == "online":
        os.system("cat online")
    elif command.startswith("message"):
        first_seperator_index = command.find(" ")
        second_seperator_index = command.find(" ", first_seperator_index + 1)
        target_username = command[first_seperator_index + 1: second_seperator_index]
        message = command[second_seperator_index + 1:]
        for line in open('online'):
            if line.startswith(target_username + ":"):
                target_ipv4 = line[len(target_username)+1:]
                os.system(f"echo [$netchat_username, $netchat_ipv4, message, {message}] | ncat {target_ipv4} $netchat_port 2>/dev/null")
                os.system(f"echo $netchat_username:{message} >> chats")
                break
