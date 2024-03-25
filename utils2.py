# In one invoice number have multiple product descriptions
import csv
from collections import defaultdict
import json
 
def retrieve_the_multiple_products_in_one_invoice_list(csv_file):
    seen_rows = defaultdict(list)
    duplicate_rows = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = (row['customer_name'], row['invoice_no'], row['invoice_date'], row['total_value'])
            seen_rows[key].append((row['customer_name'], row['invoice_no'], row['invoice_date'], row['total_value']))

        for key, rows in seen_rows.items():
            if len(rows) > 1:  # If there are duplicates
                duplicate_rows.extend(rows)

    # Remove empty dictionaries
    duplicate_rows = [row for row in duplicate_rows if any(row)]

    return json.dumps(duplicate_rows)

csv_file = "erp100.csv" 
result = retrieve_the_multiple_products_in_one_invoice_list(csv_file)
# print("oii",result) 




