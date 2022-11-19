import json
import socket
import DB_logic
import re

db = DB_logic.DAO()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    dformat = 'utf-8'

    while True:
        data = conn.recv(1024).decode(dformat)
        get_action(data, conn, dformat)
        if data == '8':
            break
    conn.close() # never goes there because of while loop


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


def get_customer(option, conn, dformat):
    send_to_client(conn, dformat, {"Response": "Customer Name: ", "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    check = re.fullmatch(r'\s+', response)
    if not check:
        send_to_client(conn, dformat, {"Response": db.get_customer(response), "Status": "Done"})
    else:
        send_to_client(conn, dformat,
                       {"Response": "Could not perform action, empty string or string of only space are not accepted for names",
                        "Status": "Done"})


def add_customer(option, conn, dformat):
    send_to_client(conn, dformat,
                   {"Response": "Add Customer", "Iteration": 4, "Fields": ["Name", "Age", "Address", "Phone"],
                    "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    check = re.match(r'[:alpha:]', response)
    if not check:
        send_to_client(conn, dformat, {"Response": db.add_customer(response), "Status": "Done"})
    else:
        send_to_client(conn, dformat,
                       {"Response": "Could not perform action, empty string, string of only space, or numbers are not accepted for names",
                        "Status": "Done"})


def delete_customer(option, conn, dformat):
    send_to_client(conn, dformat, {"Response": "Customer Name: ", "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    check = re.fullmatch(r'\s+', response)
    if not check:
        send_to_client(conn, dformat, {"Response": db.delete_customer(response), "Status": "Done"})
    else:
        send_to_client(conn, dformat,
                       {"Response": "Could not perform action, empty string or string of only space are not accepted for names",
                        "Status": "Done"})


def update_customer(option, conn, dformat):
    send_to_client(conn, dformat, {"Response": "Customer Name: ", "Status": "In progress"})
    response = conn.recv(1024).decode(dformat)
    check = re.fullmatch(r'\s+', response)
    if not check:
        if option == '6':
            field = [3, 'Phone']
        elif option == '5':
            field = [2, 'Address']
        else:
            field = [1, 'Age']
        customer = db.get_customer(response)
        if 'not found in database' not in customer:
            send_to_client(conn, dformat, {"Response": "Update Customer", "Status": "In progress", "Field": field,
                                           "Customer": db.get_customer(response)})
            response = conn.recv(1024).decode(dformat)
            check = re.fullmatch(r'[0-9]+', response)
            if not check:
                send_to_client(conn, dformat, {"Response": db.update_customer(json.loads(response)), "Status": "Done"})
        else:
            send_to_client(conn, dformat, {"Response": db.get_customer(response), "Status": "Done"})
    else:
        send_to_client(conn, dformat,
            {"Response": "Could not perform action, empty string or string of only space are not accepted for names",
             "Status": "Done"})


def send_to_client(conn, dformat, response):
    to_client = json.dumps(response)
    conn.send(to_client.encode(dformat))


def start():
    host = socket.gethostbyname(socket.gethostname())
    port = 9999

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"[LISTENING] Server is listening on {host} port {port}")

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)


print("[STARTING] server is starting...")
start()

