import os
import socket
import sys
import threading
import datetime

os.system("> log")
os.system("> online")
os.system("> chats")

print("Welcome to NetChat!")

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

os.environ["netchat_ipv4"] = host_ipv4_address



def listen():
    os.system("sh listenc &")

def announce():
    host_ipv4_network_address = host_ipv4_address[:host_ipv4_address.rfind(".") + 1]
    subnet_digits = int(host_ipv4_address[host_ipv4_address.rfind(".") + 1:])

    for i in range(10):
        if i != subnet_digits:
            target_ipv4_address = host_ipv4_network_address + str(i)
            print(target_ipv4_address)
            os.system(f"echo [$netchat_username, $netchat_ipv4, announce] | ncat -vvv -w 1 {target_ipv4_address} 12345 &") # 2>/dev/null


last_announcement_time = datetime.datetime.now()
announce()

#announcing_thread = threading.Thread(target = announce)
#announcing_thread.start()

print("message/refresh/online/exit")

while True:
    command = input().strip()

    if command == "exit":
        sys.exit()
    elif command == "announce":
        elapsed_time = datetime.datetime.now() - last_announcement_time
        if elapsed_time > datetime.timedelta(minutes=1):
            last_announcement_time = datetime.datetime.now()
            announce()
            #announcing_thread = threading.Thread(target=announce)
            #announcing_thread.start()
    elif command.startswith("message"):
        first_seperator_index = command.find(" ")
        second_seperator_index = command.find(" ", first_seperator_index + 1)
        target_username = command[first_seperator_index + 1: second_seperator_index]
        message = command[second_seperator_index + 1:]
        for line in open('online'):
            line = line.strip()
            if line.startswith(target_username + ":"):
                target_ipv4 = line[len(target_username)+1:]
                os.system(f"echo [$netchat_username, $netchat_ipv4, message, {message}] | ncat {target_ipv4} 12345 2>/dev/null")
                os.system(f"echo $netchat_username:{message} >> chats")
                break