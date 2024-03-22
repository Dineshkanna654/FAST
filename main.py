from fastapi import FastAPI, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from qapairs import CleanedDataSet
from chatbot import preprocess_data, get_answer
from transformers import GPT2Tokenizer, GPT2LMHeadModel

app = FastAPI()

# Load QA pairs and preprocess data only once
qa_pairs = CleanedDataSet()
corpus, questions, answers = preprocess_data(qa_pairs)

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

@app.post("/getQA")
async def get_qa_pairs():
    print('length',len(qa_pairs))
    return {"qa_pairs": qa_pairs} 

@app.post("/getAnswer")
async def get_answer_for_question(question: str):
    response = get_answer(question, vectorizer, tfidf_matrix, questions, answers)
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
     # Define the prompt
    print("question: ", question)
    print("response: ",response)

    if response:
        return {"answer": response}
    else:
        raise HTTPException(status_code=404, detail="Answer not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
