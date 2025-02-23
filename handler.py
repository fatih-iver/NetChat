import sys
import os

# "announce" packet format is [name, IP, announce]
# "response" packet format is [name, IP, response]
# "message" packet format is [name, IP, message, 'hello world']

seperator = ","

package = sys.argv[1]

first_seperator_index = package.find(seperator)

name = package[1: first_seperator_index]

second_seperator_index = package.find(seperator, first_seperator_index + 1)

ipv4_address = package[first_seperator_index + 2: second_seperator_index]

third_seperator_index = package.find(seperator, second_seperator_index + 2)

if third_seperator_index == -1:
    command = package[second_seperator_index + 2: -1]

    if command == "announce":
        os.system(f"echo {name}:{ipv4_address} >> online")
        os.system(f"echo [$netchat_username, $netchat_ipv4, response] | ncat {ipv4_address} 12345 2>/dev/null")
    elif command == "response":
        os.system(f"echo {name}:{ipv4_address} >> online")
else:
    command = package[second_seperator_index + 2: third_seperator_index]

    if command == "message":
        message = package[third_seperator_index + 2: -1]
        os.system(f"echo {name}:{message} >> chats")
        print(f"{name}:{message}")
