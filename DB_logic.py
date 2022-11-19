import re
from operator import itemgetter

# This class handle the database logic
class DAO:
    def __init__(self):
        self.database = self.get_customers()

    # Read the file to get the entries
    def get_customers(self):
        with open('data.txt') as f:
            lines = f.readlines()
            entries = []
            # For each line create a dictionary for customer
            for line in lines:
                entries.append(self.create_dict(re.sub(r'\n', '', line)))
            return entries

    # Create a dictionary for the customer
    def create_dict(self, customer):
        # Get rid of the multiple spaces if there are
        field_value = re.sub(r'\s{2,}', '', customer)
        # Split string by pipeline to get the info
        clean_customer = field_value.split('|')
        # Now create dictionary with the info
        customer = {
            "Name": f"{clean_customer[0]}",
            "Age": f"{clean_customer[1]}",
            "Address": f"{clean_customer[2]}",
            "Phone": f"{clean_customer[3]}"
        }
        return customer

    # Return the entry of a specific customer with the name given by client
    def get_customer(self, name):
        bar = '|'
        # Find the customer by the name given and return the entry as one string
        for customer in self.database:
            if name == customer["Name"]:
                return bar.join(customer.values())
        return f"{name} not found in database"

    # Add a customer to our db list
    def add_customer(self, new_c):
        # Split at pipeline to get each field from string we got from client
        entry = new_c.split('|')
        # Check if a customer with that name already exist
        for customer in self.database:
            if entry[0] == customer['Name']:
                return f"Customer {entry[0]} already exist"
        # If customer doesn't exist add to list
        new_c = self.create_dict(new_c)
        self.database.append(new_c)
        return f"{new_c['Name']} added to database"

    # Delete a customer chosen by the name given by client
    def delete_customer(self, name):
        for customer in self.database:
            if name == customer["Name"]:
                # Remove the customer from our list
                self.database.remove(customer)
                return f"Customer {name} has be removed from database"
        # Return that it couldn't be deleted as the customer doesn't exist
        return f"Customer {name} does not exist in database, could not delete"

    # Update a field of an identified customer
    def update_customer(self, to_update):
        name = to_update['Name']
        field = to_update['Field']
        # Go through all customers in db until we get the one with the matching name
        for customer in self.database:
            if name == customer['Name']:
                # Update the field given by client with the update also given by client
                customer[field] = to_update['Update']
                return f"Customer {name}'s {field} has been updated"
        # If the customer doesn't exist in db return that it couldn't be found
        return f"Customer {name} could not be found in database"

    # Create a string containing all the customers in database
    def print_report(self):
        records = []
        # sort the items in database by name
        sorted_list = sorted(self.database, key=itemgetter('Name'))
        # Create a string separated by | for each of the dictionaries
        for customer in sorted_list:
            bar = '|'
            records.append(bar.join(customer.values()))
        new_line = '\n'
        return new_line.join(records)

