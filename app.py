from flask import Flask, request, render_template, jsonify
from utils.rag_engine import RAGEngine
from dotenv import load_dotenv
import os
import sys

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TEXT_PATH = os.getenv("F:/10 Min School/Gemini_new", "Extracted_text.txt")

app = Flask(__name__)
rag = None 


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/query', methods=['POST'])
def handle_query():
    query = request.get_json().get('query', '')
    if not query:
        return jsonify({'answer': 'Empty query provided'}), 400
    if not rag:
        return jsonify({'answer': 'RAG not initialized'}), 500
    answer = rag.ask(query)
    return jsonify({'answer': answer})


if __name__ == '__main__':
    print("Starting in web mode...")

    if not os.path.exists(TEXT_PATH):
        print(f"File not found: {TEXT_PATH}")
        sys.exit(1)

    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("The context file is empty.")
        sys.exit(1)

    rag = RAGEngine(api_key=GEMINI_API_KEY)
    rag.prepare_document(text)
    print("RAG initialized successfully")

    app.run(debug=True)
