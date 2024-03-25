import csv
import json
import spacy

nlp = spacy.load("en_core_web_sm")

def calculate_total_value(csv_file, customer_name):
    total_value = 0
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['customer_name'] == customer_name:
                total_value += float(row['total_value'])
    return total_value

def generate_qa_pairs(csv_file):
    qa_pairs = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_name = row['customer_name']
            total_value = str(calculate_total_value(csv_file, customer_name))
            qa_pairs.append({
                "question": f"What is the Total value or Net value for {customer_name}?",
                "answer": total_value
            })
            qa_pairs.append({
                "question": f"What is the product code for {row['product_description']}?",
                "answer": row['product_code']
            })
            qa_pairs.append({
                "question": f"Who is the customer for the product {row['product_description']}?",
                "answer": row['customer_name']
            })
            qa_pairs.append({
                "question": f"Who is the customer for the product code {row['product_code']}?",
                "answer": row['customer_name']
            })
            qa_pairs.append({
                "question": f"What is the product description for this product code {row['product_code']}?",
                "answer": row['product_description']
            })
            qa_pairs.append({
                "question": f"What is the total value for this product code {row['product_code']}?",
                "answer": row['total_value']
            })
            qa_pairs.append({
                "question": f"What is the invoice number for this product code {row['product_code']}?",
                "answer": row['invoice_no']
            })
            qa_pairs.append({
                "question": f"What is the invoice date for this product code {row['product_code']}?",
                "answer": row['invoice_date']
            })
            qa_pairs.append({
                "question": f"What is the ordered quantity for this product code {row['product_code']}?",
                "answer": row['order_qty']
            })
            qa_pairs.append({
                "question": f"What is the MRP for this product code {row['product_code']}?",
                "answer": row['item_mrp']
            })
            qa_pairs.append({
                "question": f"Who is the customer for this invoice number {row['invoice_no']}?",
                "answer": row['customer_name']
            })
            qa_pairs.append({
                "question": f"What is the date of for this invoice number {row['invoice_no']}?",
                "answer": row['invoice_date']
            })
            qa_pairs.append({
                "question": f"When was the invoice for {row['product_description']} issued to {row['customer_name']}?",
                "answer": row['invoice_date']
            })
            qa_pairs.append({
                "question": f"What is the total value of the order for {row['product_description']} for {row['customer_name']}?",
                "answer": row['total_value']
            })
            qa_pairs.append({
                "question": f"How many items were ordered for the product {row['product_description']} by {row['customer_name']}?",
                "answer": row['order_qty']
            })
            qa_pairs.append({
                "question": f"What is the invoice number for the product {row['product_description']} ordered by {row['customer_name']}?",
                "answer": row['invoice_no']
            })
            qa_pairs.append({
                "question": f"What is the item MRP for the product {row['product_description']}?",
                "answer": row['item_mrp']
            })
    return qa_pairs

def dataset():
    csv_file = "erp100.csv"
    qa_pairs = generate_qa_pairs(csv_file)
    return qa_pairs

data = dataset()

def remove_duplicate_pairs(qa_pairs):
    unique_pairs = set()
    unique_qa_pairs = []

    for pair in qa_pairs:
        pair_tuple = (pair['question'], pair['answer'])
        if pair_tuple not in unique_pairs:
            unique_pairs.add(pair_tuple)
            unique_qa_pairs.append(pair)
    return unique_qa_pairs

def CleanedDataSet():
    data = dataset()
    cleaned_data = remove_duplicate_pairs(data)
    return cleaned_data

# In one invoice number have multiple product descriptions
input_text = "Net value"

# def total_value_qapairs_questions(input_text , exi_qa_pairs):
#     for total_value_qapairs in exi_qa_pairs["qa_pairs"]:
#         if input_text.lower() in exi_qa_pairs["question"].lower():
#             questions = [qa_pair["question"] for qa_pair in total_value_qapairs["qa_pairs"]]
#             return questions
#         # ["question": "What is the Total value or Net value for Amman Auto Agency?]"
#     return None

def total_value_qapairs_questions(input_text, exi_qa_pairs):
    questions = []
    for qa_pair in exi_qa_pairs:
        if input_text.lower() in qa_pair["question"].lower():
            questions.append(qa_pair["question"])
    if questions:
        # ["question": "What is the Total value or Net value for Amman Auto Agency?]"
        return json.dumps(questions)
    else:
        return None
    
def total_value_qapairs_answers(input_text, exi_qa_pairs):
    answers = []
    for qa_pair in exi_qa_pairs:
        if input_text.lower() in qa_pair["question"].lower():
            answers.append(qa_pair["answer"])
    if answers:
        return answers
        # 7480.0
    else:
        return None


exi_qa_pairs = CleanedDataSet()
question = total_value_qapairs_questions(input_text, exi_qa_pairs)

def extract_organization_entities(question):
    doc = nlp(question)
    organizations = []
    for entity in doc.ents:
        if entity.label_ == "ORG":
            organizations.append(entity.text)
            # Amman Auto Agency
    return json.dumps(organizations)

def total_value_and_customer_names(question, input_text, exi_qa_pairs):
    customer_name = extract_organization_entities(question)
    total_value = total_value_qapairs_answers(input_text, exi_qa_pairs)
    pairs = {
        "customer_name": customer_name,
        "total_value": total_value
    }
    unclean_result = json.dumps(pairs)
    parsed_result = json.loads(unclean_result)
    
    # Extracting customer names as a list from the JSON string
    customer_names = json.loads(parsed_result['customer_name'])
    
    # Converting total values to floats
    total_values = [float(val) for val in parsed_result['total_value']]
    
    # Pairing customer names with total values
    result = [{'customer_name': name, 'total_value': value} for name, value in zip(customer_names, total_values)]
    
    return result


def migrate_total_value_and_customer_names():
    result = total_value_and_customer_names(question, input_text, exi_qa_pairs)
    return json.dumps(result)

def save_qa_pairs_as_json(qa_pairs, json_file):
    with open(json_file, 'w') as file:
        json.dump(qa_pairs, file, indent=4)


 
cleaned_data = remove_duplicate_pairs(data)


if __name__ == "__main__":
    csv_file = "erp100.csv"
    json_file = "qa_pairs.json"

    qa_pairs = generate_qa_pairs(csv_file)
    save_qa_pairs_as_json(cleaned_data, json_file)

# https://chat.openai.com/c/a28d39c4-c001-453c-9a89-c75af44c803e

