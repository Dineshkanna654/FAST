import spacy

nlp = spacy.load("en_core_web_sm")
input_text = "Net value"

def total_value(input_text , exi_qa_pairs):
    for total_value_qapairs in exi_qa_pairs["qa_pairs"]:
        if input_text.lower() in exi_qa_pairs["question"].lower():
            return total_value_qapairs
        # {
        # "question": "What is the Total value or Net value for Amman Auto Agency?",
        # "answer": "7480.0"
        # }
    return None

def extract_organization_entities(question):
    doc = nlp(question)
    organizations = []
    for entity in doc.ents:
        if entity.label_ == "ORG":
            organizations.append(entity.text)
    return organizations
