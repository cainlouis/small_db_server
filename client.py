import socket
import json

def menu():
    print("Python DB Menu")
    print("1. Find customer \n"
          "2. Add customer \n"
          "3. Delete customer \n"
          "4. Update customer age \n"
          "5. Update customer address \n"
          "6. Update customer phone \n"
          "7. Print report \n"
          "8. exit")

    client_input = check_input()
    return client_input


def check_input():
    while True:
        client_input = input("Select: ")
        print('\n')

        if client_input.isdigit():
            if 1 <= int(client_input) <= 8:
                break
            else:
                print("Please enter the number of one of the available options")
                # continue
        else:
            print("Please enter the number of one of the available options")
    return client_input


def ask_info(ite, fields):
    info = []
    bar = '|'
    for i in range(ite):
        info.append(input(f"Enter {fields[i]}: "))
    client_response = bar.join(info)
    print('\n')
    return client_response

def update_entry(field, entry):
    entry = entry.split('|')
    client_response = json.dumps({"Name": entry[0], "Field": field[1], "Update": input(f"Enter {entry[0]}'s new {field[1]}: ")})
    print('\n')
    return client_response

def start_client():
    host = socket.gethostname()
    port = 9999
    dformat = 'utf-8'

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"[NEW CONNECTION] {host} port {port} connected.")

    while True:
        client_input = menu()
        client.send(client_input.encode(dformat))

        if client_input == '8':
            break
        count = 0
        while True:
            feedback = client.recv(1024).decode(dformat)
            data = json.loads(feedback)
            msg = data['Response']
            if msg == 'Add Customer':
                client_response = ask_info(data['Iteration'], data['Fields'])
            elif msg == "Update Customer":
                client_response = update_entry(data['Field'], data['Customer'])
            else:
                if data['Status'] == 'Done':
                    if client_input == '7':
                        print(f"** Database Content ** \n"
                              f"{msg}")
                    else:
                        print(f"Server Response: {msg}")
                    print('\n')
                    break
                else:
                    client_response = input(f"{msg}")
            client.send(client_response.encode(dformat))

    client.close()


start_client()
