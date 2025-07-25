import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import LLM
from typing import Optional, List
import re

class BanglaSentenceSplitter:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text):
        sentences = re.split(r'(?<=[।!?])\s+', text.strip())
        chunks, chunk = [], ""
        for sentence in sentences:
            if len(chunk) + len(sentence) <= self.chunk_size:
                chunk += sentence + " "
            else:
                chunks.append(chunk.strip())
                chunk = sentence + " "
        if chunk:
            chunks.append(chunk.strip())
        if self.chunk_overlap > 0 and len(chunks) > 1:
            overlapped = []
            for i in range(len(chunks)):
                prev = chunks[i - 1] if i > 0 else ""
                combined = (prev + " " + chunks[i])[-self.chunk_size:]
                overlapped.append(combined)
            return overlapped
        return chunks

class GeminiLLM(LLM):
    model: any
    model_name: str = "models/gemini-2.5-flash"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

    @property
    def _llm_type(self) -> str:
        return "gemini"

class RAGEngine:
    def __init__(self, api_key):
        print("Initializing RAG engine...")
        try:
            genai.configure(api_key=api_key)
            gemini_model = genai.GenerativeModel("models/gemini-2.5-flash")
            self.llm = GeminiLLM(model=gemini_model)
            self.embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )
            self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            self.vectorstore = None
            self.qa_chain = None
            print("RAG engine initialized.")
        except Exception as e:
            print(f"Failed to initialize RAG engine: {str(e)}")
            raise

    def prepare_document(self, raw_text):
        print("Preparing document for RAG...")
        try:
            chunks = BanglaSentenceSplitter().split_text(raw_text)
            if not chunks:
                raise ValueError("No text chunks created. Ensure input text is valid.")
            self.vectorstore = Chroma.from_texts(chunks, self.embedding_model)
            retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=self.memory
            )
            print(f"Document prepared with {len(chunks)} chunks.")
        except Exception as e:
            print(f"Error preparing document: {str(e)}")
            raise

    def ask(self, question):
        print(f"Processing query: {question}")
        if not self.qa_chain:
            error_msg = "Document not prepared. Please initialize RAG with a document."
            print(error_msg)
            return error_msg
        try:
            answer = self.qa_chain.run(question)
            print("Query processed successfully.")
            return answer
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            print(error_msg)
            return error_msg
