# Project Setup and Implementation Details
# Setup Guide
pip install -r requirements.txt

Clone the GitHub Repository ||
Open VS Code with the folder ||
Open terminal and ||
    type: python app.py ||
Click on the " Running on http://127.0.0.1:5000 " ||
Now, you will see a box having placeholder written “আপনার প্রশ্ন লিখুন”? ||
Write your question ||
Click the “জিজ্ঞাসা করুন” button ||
Here We Go!! 🚨 ||

# Used Tools, Libraries, and Packages
Flask: Lightweight web framework for serving HTML UI

EasyOCR: For extracting text from images

```pdf2image```: Converts PDF pages to images

```google-generativeai```: To access Gemini 2.5 Flash for LLM inference

```langchain```: Framework for chaining LLMs with tools (retrieval, memory, etc.)

```tiktoken```: For tokenization

```chromadb```: Local vector store for embeddings

```sentence-transformers```: Generates dense semantic embeddings

```transformers```: For advanced NLP models

```python-dotenv```: Loads environment variables like GEMINI_API_KEY

```langchain_community```: Integrates with ChromaDB and Hugging Face embeddings

```langchain-core```: Core LangChain functionalities

```re``` (regex): Custom sentence splitting (handles Bangla punctuation like |)

```os/sys```: File path access and CLI handling

```flask.request, flask.jsonify, flask.render_template```: Accepting queries, returning answers, and rendering templates

# Sample Queries and Outputs
User Question: কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?Expected Answer: মামাকে  

User Question: বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?Expected Answer: ১৫ বছর  

User Question: রবীন্দ্রনাথ ঠাকুর এর জন্ম কোথায়?Expected Answer: জোড়াসাঁকো কলকাতা, ভারত

# Implementation Details
Text Extraction Method and Challenges

Method/Library: Used easyOCR with pdf2image to extract text from PDFs.  

Reason: pdf2image converts PDF pages to images, and easyOCR performs OCR to extract text, which is effective for scanned or image-based PDFs.  

Challenges:  

Formatting issues with Bangla text, especially with complex scripts and punctuation (e.g., |).  

Inconsistent font rendering in PDFs can lead to OCR errors.  

Structured content like tables or lists (e.g., “কবি পরিচিতি”) often loses formatting, impacting retrieval accuracy.

# Chunking Strategy

Strategy: Custom Bangla sentence-based chunking with a character limit of ~500 characters and an optional 50-character overlap.  

Details:  

Preserves sentence boundaries in Bangla (|, ?, !).  

Ensures semantic cohesion within each chunk.  

Overlapping retains context across adjacent chunks, improving retrieval relevance.

Why it Works: Sentence-based chunking aligns with the narrative style of the content, and overlaps maintain contextual continuity, enhancing semantic retrieval.

# Embedding Model

Model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 from HuggingFace.  

Reason:  

Multilingual support, effective for Bangla.  

Lightweight yet powerful for semantic embeddings.  

Widely used in production-grade RAG systems.


How it Captures Meaning: Generates dense vector representations where semantically similar texts are close in vector space. Trained on sentence-level paraphrasing tasks, it excels at capturing meaning for retrieval.

# Query and Chunk Comparison

Storage: ChromaDB as the vector store.  

Similarity Method: Cosine similarity between query and chunk embeddings.  

Reason:  

ChromaDB is lightweight, fast, and integrates seamlessly with LangChain.  

Cosine similarity is efficient for high-dimensional embeddings and widely used.

Ensuring Meaningful Comparison:  

Query and chunks are embedded using the same model, ensuring they lie in the same vector space.  

Carefully tuned chunk size preserves contextual meaning.


Handling Vague Queries:  

Vague or contextless queries may retrieve less relevant chunks due to poor semantic alignment.  

Mitigation: Improve chunking with NLP-based sentence boundary detection or use larger documents for richer context.



# Result Relevance and Improvements

Relevance: Results are generally relevant for fact-based or direct questions.  

Challenges: Structured sections (e.g., tables or lists like “কবি পরিচিতি”) are poorly chunked, leading to retrieval issues.  

Potential Improvements:  

Improved Chunking: Use NLP tools or language-specific tokenizers for accurate sentence boundary detection.  

Larger Document Input: More context improves retrieval performance.  

Advanced Embeddings: Transformer-based models with attention mechanisms could better capture semantic structure, though at higher computational cost.  

Preprocessing Structured Content: Manually preprocess or differently chunk structured sections like tables or lists.




