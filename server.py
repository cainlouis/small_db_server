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
            to_client = json.dumps({"Response": "Customer Name: ", "Status": "In progress"})
            conn.send(to_client.encode(dformat))
            response = conn.recv(1024).decode(dformat)
            print(f"res {response}")
            check = re.fullmatch(r'\s+', response)
            if not check:
                db_res = {"Response": db.get_customer(response), "Status": "Done"}
                to_client = json.dumps(db_res)
                conn.send(to_client.encode(dformat))
        case '2':
            to_client = json.dumps({"Response": "Add Customer", "Iteration": 4, "Fields": ["Name", "Age", "Address", "Phone"], "Status": "In progress"})
            conn.send(to_client.encode(dformat))
            response = conn.recv(1024).decode(dformat)
            print(f"res {type(response)}")
            check = re.match(r'[:alpha:]', response)
            print(f"Check is {check}")
            if not check:
                db_res = {"Response": db.add_customer(response), "Status": "Done"}
                to_client = json.dumps(db_res)
                conn.send(to_client.encode(dformat))

        case '3':
            to_client = json.dumps({"Response": "Customer Name: ", "Status": "In progress"})
            conn.send(to_client.encode(dformat))
            response = conn.recv(1024).decode(dformat)
            print(f"res {response}")
            check = re.fullmatch(r'\s+', response)
            if not check:
                db_res = {"Response": db.delete_customer(response), "Status": "Done"}
                to_client = json.dumps(db_res)
                conn.send(to_client.encode(dformat))
        case '4' | '5' | '6':
            to_client = json.dumps({"Response": "Customer Name: ", "Status": "In progress"})
            conn.send(to_client.encode(dformat))
            response = conn.recv(1024).decode(dformat)
            print(f"res {response}")
            check = re.fullmatch(r'\s+', response)
            if not check:
                field = []
                if option == '6':
                    field = [3, 'Phone']
                elif option == '5':
                    field = [2, 'Address']
                else:
                    field = [1, 'Age']
                db_res = {"Response": "Update Customer", "Status": "In progress", "Field": field, "Customer": db.get_customer(response)}
                to_client = json.dumps(db_res)
                conn.send(to_client.encode(dformat))
                response = conn.recv(1024).decode(dformat)
                check = re.fullmatch(r'[0-9]+', response)
                if not check:
                    db_res = {"Response": db.update_customer(json.loads(response)), "Status": "Done"}
                    to_client = json.dumps(db_res)
                    conn.send(to_client.encode(dformat))
        case '7':
            to_client = json.dumps({"Response": db.print_report(), "Status": "Done"})
            conn.send(to_client.encode(dformat))
            # response = conn.recv(1024).decode(dformat)
            # conn.send()


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

