import os
import socket
import sys
import threading
import time
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
    os.system("sh listenc")

listening_thread = threading.Thread(target = listen)
listening_thread.start()


def announce():
    host_ipv4_network_address = host_ipv4_address[:host_ipv4_address.rfind(".") + 1]
    subnet_digits = int(host_ipv4_address[host_ipv4_address.rfind(".") + 1:])

    for i in range(254):
        if i != subnet_digits:
            target_ipv4_address = host_ipv4_network_address + str(i)
            os.system(f"echo [$netchat_username, $netchat_ipv4, announce] | ncat -w 0.01 {target_ipv4_address} 12345 2>/dev/null")



announcing_thread = threading.Thread(target = announce)
last_announcement_time = datetime.datetime.now()
announcing_thread.start()
print("Announcing! Wait.", end="")
time.sleep(1)
print(".", end="")
time.sleep(1)
print(".", end="")
time.sleep(1)
print("Announcing finished!")

print("message/refresh/online/exit")

while True:
    command = input().strip()

    if command == "exit":
        sys.exit()
    elif command == "announce":
        current_time = datetime.datetime.now()
        elapsed_time = current_time - last_announcement_time
        if elapsed_time > datetime.timedelta(minutes=1):
            announcing_thread = threading.Thread(target=announce)
            last_announcement_time = datetime.datetime.now()
            announcing_thread.start()
            print("Announcing! Wait.", end = "")
            time.sleep(1)
            print(".", end = "")
            time.sleep(1)
            print(".", end = "")
            time.sleep(1)
            print("Announcing finished!")
        else:
            print("Cannot announce!")
    elif command == "online":
        os.system("cat online")
    elif command.startswith("message"):
        first_seperator_index = command.find(" ")
        second_seperator_index = command.find(" ", first_seperator_index + 1)
        target_username = command[first_seperator_index + 1: second_seperator_index]
        message = command[second_seperator_index + 1:]
        username_to_ipv4 = {}
        for line in open('online'):
            username_to_ipv4[line.strip().split(":")[0]] = line.strip().split(":")[1]
        if target_username in username_to_ipv4:
            target_ipv4 = username_to_ipv4[target_username]
            os.system(f"echo [$netchat_username, $netchat_ipv4, message, {message}] | ncat {target_ipv4} 12345 2>/dev/null")
            os.system(f"echo $netchat_username:{message} >> chats")
            break
        else:
            print("No such user exist!")
