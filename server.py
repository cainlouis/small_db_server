import json
import socket
import DB_logic
import re

db = DB_logic.DAO()


# This class handles the request from the client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    dformat = 'utf-8'
    # Get the request from client act according to the input
    while True:
        data = conn.recv(1024).decode(dformat)
        get_action(data, conn, dformat)
        # break the loop to wait for a new connection if the client exit
        if data == '8':
            break
    conn.close() # never goes there because of while loop


# Act according to the option selected by client
def get_action(option, conn, dformat):
    match option:
        case '1':
            get_customer(option, conn, dformat)
        case '2':
            add_customer(option, conn, dformat)
        case '3':
            delete_customer(option, conn, dformat)
        case '4' | '5' | '6':
            update_customer(option, conn, dformat)
        case '7':
            send_to_client(conn, dformat, {"Response": db.print_report(), "Status": "Done"})


# Return the info of a specific customer to client
def get_customer(option, conn, dformat):
    # First prompt the client for a name
    send_to_client(conn, dformat, {"Response": "Customer Name: ", "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    # Check if the name is only a space character
    check = re.fullmatch(r'\s+', response)
    # If not return the info to the client
    if not check:
        send_to_client(conn, dformat, {"Response": db.get_customer(response), "Status": "Done"})
    # Else tell the client that the name is not valid
    else:
        send_to_client(conn, dformat,
                       {"Response": "Could not perform action, empty string or string of only space are not accepted for names",
                        "Status": "Done"})


# Add a customer to the db
def add_customer(option, conn, dformat):
    # Prompt the client to enter the new customer's info
    send_to_client(conn, dformat,
                   {"Response": "Add Customer", "Iteration": 4, "Fields": ["Name", "Age", "Address", "Phone"],
                    "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    # Check that the name of the new customer is valid
    check = re.match(r'[:alpha:]', response)
    # If it is, add the customer to db
    if not check:
        send_to_client(conn, dformat, {"Response": db.add_customer(response), "Status": "Done"})
    # If not tell client it is not valid
    else:
        send_to_client(conn, dformat,
                       {"Response": "Could not perform action, empty string, string of only space, or numbers are not accepted for names",
                        "Status": "Done"})


# Delete a specific customer from db
def delete_customer(option, conn, dformat):
    # Prompt the client for a name
    send_to_client(conn, dformat, {"Response": "Customer Name: ", "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    # Check if they entered only spaces
    check = re.fullmatch(r'\s+', response)
    # If they didn't delete customer from db
    if not check:
        send_to_client(conn, dformat, {"Response": db.delete_customer(response), "Status": "Done"})
    # Else tell them the name was not valid
    else:
        send_to_client(conn, dformat,
                       {"Response": "Could not perform action, empty string or string of only space are not accepted for names",
                        "Status": "Done"})


# Update a specific customer info
def update_customer(option, conn, dformat):
    # Prompt the client for a name
    send_to_client(conn, dformat, {"Response": "Customer Name: ", "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    # check if they didn't enter only spaces
    check = re.fullmatch(r'\s+', response)
    # If they didn't update the field they wanted to update
    if not check:
        # Assign the field to the option the client chose
        if option == '6':
            field = [3, 'Phone']
        elif option == '5':
            field = [2, 'Address']
        else:
            field = [1, 'Age']
        # Get the customer from db
        customer = db.get_customer(response)
        # If the customer exist in db prompt the client for the update they want
        if 'not found in database' not in customer:
            send_to_client(conn, dformat, {"Response": "Update Customer", "Status": "In progress", "Field": field,
                                           "Customer": db.get_customer(response)})
            response = conn.recv(1024).decode(dformat)
            send_to_client(conn, dformat, {"Response": db.update_customer(json.loads(response)), "Status": "Done"})
        # If the customer doesn't exist simply send the customer the answer of the db
        else:
            send_to_client(conn, dformat, {"Response": db.get_customer(response), "Status": "Done"})
    # If they did, tell them that the name is not valid
    else:
        send_to_client(conn, dformat,
            {"Response": "Could not perform action, empty string or string of only space are not accepted for names",
             "Status": "Done"})


# Create a string from the db response and send to db
def send_to_client(conn, dformat, response):
    to_client = json.dumps(response)
    conn.send(to_client.encode(dformat))


# Start the server to listen on the port for the client
def start():
    # Get the host
    host = socket.gethostbyname(socket.gethostname())
    port = 9999

    # Bind the server to the host and port to listen
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"[LISTENING] Server is listening on {host} port {port}")

    # Accept the connection and call handle_client to handle the client requests
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)


print("[STARTING] server is starting...")
start()

