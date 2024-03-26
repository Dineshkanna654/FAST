import csv
import json

csv_file = "erp100.csv"

def get_customer_names(csv_file):
    customer_names = []

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_name = row['customer_name'].strip()
            if customer_name:
                customer_names.append(customer_name)

    return customer_names

def calculate_total_value(csv_file, customer_name):
    total_value = 0
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['customer_name'] == customer_name:
                total_value += float(row['total_value'])
    return total_value


# Store the total value with customer name in json
def calculate_customer_totals(csv_file_path):
    # Define a dictionary to store total values for each customer
    customer_totals = {}

    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Extract customer name and total value from the row
            customer_name = row['customer_name']  # Ensure column name matches the one in your CSV
            total_value_str = row['total_value']  # Ensure column name matches the one in your CSV
            
            # Check if total_value_str is not empty
            if total_value_str:
                total_value = float(total_value_str)
            else:
                total_value = 0.0  # Or any other default value you prefer
            
            # Update the total value for the customer in the dictionary
            if customer_name in customer_totals:
                customer_totals[customer_name] += total_value
            else:
                customer_totals[customer_name] = total_value

    # Create a list to store customer totals in JSON format
    customer_totals_json = []

    # Convert the customer_totals dictionary to JSON format
    for customer, total in customer_totals.items():
        customer_total_json = {
            "customer_name": customer,
            "total_value": total
        }
        customer_totals_json.append(customer_total_json)

    # Filter out entries with an empty customer_name
    customer_totals_json_filtered = [entry for entry in customer_totals_json if entry['customer_name']]

    # Convert the filtered list to a JSON-formatted string
    json_string = json.dumps(customer_totals_json_filtered, indent=2)
    
    return json_string



def get_top_customers(customer_totals_json, top=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
    # Sort the list of customer totals based on the total_value in descending order
    sorted_customer_totals = sorted(customer_totals_json, key=lambda x: x['total_value'], reverse=True)
    # Get the top N customers
    top_customers = sorted_customer_totals[:top]
    return top_customers


