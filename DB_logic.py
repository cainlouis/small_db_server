import re
from operator import itemgetter


class DAO:
    def __init__(self):
        self.database = self.get_customers()

    def get_customers(self):
        with open('data.txt') as f:
            lines = f.readlines()
            entries = []
            for line in lines:
                entries.append(self.create_dict(re.sub(r'\n', '', line)))
            return entries

    def create_dict(self, customer):
        field_value = re.sub(r'\n | \s{2,}', '', customer)
        clean_customer = field_value.split('|')
        customer = {
            "Name": f"{clean_customer[0]}",
            "Age": f"{clean_customer[1]}",
            "Address": f"{clean_customer[2]}",
            "Phone": f"{clean_customer[3]}"
        }
        return customer

    def get_customer(self, name):
        bar = '|'
        for customer in self.database:
            print(customer)
            if name == customer["Name"]:
                return bar.join(customer.values())
        return f"{name} not found in database"

    def add_customer(self, new_c):
        print(new_c)
        entry = new_c.split('|')
        for customer in self.database:
            print(f"c na {customer['Name']}")
            if entry[0] == customer['Name']:
                return f"Customer {entry[0]} already exist"
        new_c = self.create_dict(new_c)
        self.database.append(new_c)
        return f"{new_c['Name']} added to database"

    def delete_customer(self, name):
        for customer in self.database:
            if name == customer["Name"]:
                self.database.remove(customer)
                return f"Customer {name} has be removed from database"
        return f"Customer {name} does not exist in database"

    def update_customer(self, to_update):
        name = to_update['Name']
        field = to_update['Field']
        for customer in self.database:
            if name == customer['Name']:
                customer[field] = to_update['Update']
                return f"Customer's {name} {field} has be updated"
        return f"Customer {name} could not be found in database"

    def print_report(self):
        records = []
        for customer in self.database:
            bar = '|'
            records.append(bar.join(customer.values()))
        new_line = '\n'
        return new_line.join(records)

