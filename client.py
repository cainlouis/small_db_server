import socket
import json
import re

# Print the menu for the client and get their input
def menu():
    print("Python DB Menu \n"
          "1. Find customer \n"
          "2. Add customer \n"
          "3. Delete customer \n"
          "4. Update customer age \n"
          "5. Update customer address \n"
          "6. Update customer phone \n"
          "7. Print report \n"
          "8. exit")
    # Get the input and check if it's valid
    client_input = check_input()
    return client_input


# Ask the client for their choice and check if it is valid
def check_input():
    while True:
        client_input = input("Select: ")
        print('\n')

        # Check if the client entered a digit
        if client_input.isdigit():
            # Check if they entered one of the valid choices
            if 1 <= int(client_input) <= 8:
                # break the loop if they did
                break
            # If they didn't tell the client the problem and continue the loop to ask them again
            else:
                print("Please enter the number of one of the available options")
                # continue
        # If they didn't enter a digit, tell them to do so
        else:
            print("Please enter the number of one of the available options")
    return client_input


# Ask the client for the info of the customer they want to add
def ask_info(ite, fields):
    info = []
    bar = '|'
    # For each infor of the customer prompt the client to enter
    for i in range(ite):
        user_input = input(f"Enter {fields[i]}: ")
        if i == 0:
            user_input = re.sub(r'\s{2,}', '', user_input)
        info.append(user_input)
    # Make it a string
    client_response = bar.join(info)
    print('\n')
    return client_response


# Ask the client for the update they want to do
def update_entry(field, entry):
    entry = entry.split('|')
    client_response = json.dumps({"Name": entry[0], "Field": field[1], "Update": input(f"Enter {entry[0]}'s new {field[1]}: ")})
    print('\n')
    return client_response


# Start the client side and communicate with the server
def start_client():
    # Get the host
    host = socket.gethostname()
    port = 9999
    dformat = 'utf-8'

    # Bind the client to the host and the port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"[NEW CONNECTION] {host} port {port} connected.")

    # Continue to prompt the client until they ask to exit
    while True:
        # Get the client choice and send to server
        client_input = menu()
        client.send(client_input.encode(dformat))

        # If they want to exit break the loop
        if client_input == '8':
            break
        # Communicate with the server until it returns that the action is done
        while True:
            # Receive the server answer and load it as a dictionary
            feedback = client.recv(1024).decode(dformat)
            data = json.loads(feedback)
            msg = data['Response']
            # Depending on the response act accordingly
            if msg == 'Add Customer':  # If the server returns that it is adding a customer as requested
                # Prompt the user for the new customer's info
                client_response = ask_info(data['Iteration'], data['Fields'])
            elif msg == "Update Customer":  # If it returns that it is updating a customer
                # Prompt the user for the update they want to do
                client_response = update_entry(data['Field'], data['Customer'])
            else:  # If it's doing anything else
                # Check if it is done
                if data['Status'] == 'Done':
                    if client_input == '7':  # If it is returning the report, print it with a header
                        print(f"** Database Content ** \n"
                              f"{msg}")
                    else:  # Else print the server response and break the loop
                        print(f"Server Response: {msg}")
                    print('\n')
                    break
                else:  # If it isn't done prompt the user
                    client_response = input(f"{msg}")
            # then send the response to server
            client.send(client_response.encode(dformat))
    # If they exit tell them bye then close the client side connection
    print('Exiting, Good Bye!')
    client.close()


start_client()
