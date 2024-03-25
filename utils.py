import csv

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

def retrieve_unique_column_values(csv_file, column_name):
    unique_values = set()

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract the value from the specified column
            value = row[column_name]
            unique_values.add(value)

    return unique_values

column_name = 'customer_name'
customer_list = retrieve_unique_column_values(csv_file, column_name)
# print('customer_list', customer_list)

# Store the total value with customer name in json
def customer_total_value(csv_file):
    total_values = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_name = row['customer_name']
            total_value = calculate_total_value(csv_file, customer_name)
            if customer_name in total_values:
                total_values[customer_name] += total_value
            else:
                total_values[customer_name] = total_value
    
    # Convert dictionary to list of dictionaries for JSON output
    output = [{'Customer_name': customer, 'Total_value': str(total_values[customer])} for customer in total_values]
    return output




# def top_most_customer_on_sales(customer_list, top_range):
#     total_sales = {}
#     for customer in customer_list:
#         total_sales[customer] = calculate_total_value(csv_file, customer)
#     sorted_customers = sorted(total_sales.items(), key=lambda x: x[1], reverse=True)
#     return sorted_customers[:top_range]


