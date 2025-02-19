from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.llms import Cohere   
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is missing. Please check your .env file.")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY is missing. Please check your .env file.")

# Download embeddings
embeddings = download_hugging_face_embeddings()

# Define Pinecone index
index_name = "medicalbot"

# Initialize Pinecone vector store
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# 🔹 Increased retrieval count (k=15 for better recall)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 15})

# Initialize LLM
llm = Cohere(temperature=0.3, max_tokens=800)  # Lower temperature for factual accuracy

# 🔹 Stronger system prompt formatting
system_prompt = """You are a medical assistant. Use ONLY the provided context for your answer.

If the information is not in the context, respond: "I do not have enough information on this topic."

Context:
{context}

User's Question: {input}"""

# Modify the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# 🔹 Structured answer extraction
question_answer_chain = create_stuff_documents_chain(llm, prompt, document_variable_name="context")
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg")
    if not msg:
        return "Please enter a message."

    print(f"User message: {msg}")

    try:
        # 🔹 Retrieve relevant documents
        retrieved_docs = retriever.get_relevant_documents(msg)

        if retrieved_docs:
            retrieved_texts = "\n".join([doc.page_content for doc in retrieved_docs])
            retrieved_titles = [doc.metadata.get("title", "Unknown Title") for doc in retrieved_docs]
            print(f"Retrieved Documents Titles: {retrieved_titles}")
            print(f"Retrieved Texts:\n{retrieved_texts}")
        else:
            print("No relevant documents found.")

        # 🔹 If no relevant documents, return a clear message
        if not retrieved_docs:
            return "I do not have enough information on this topic."

        # 🔹 Ensure LLM gets structured context
        response = rag_chain.invoke({"input": msg, "context": retrieved_texts})

        # 🔹 Debug response
        print(f"RAG Output: {response}")

        # Extract answer safely
        answer = response.get("answer", "I do not have enough information.")

        print(f"Bot's response: {answer}")
        return answer
    except Exception as e:
        print(f"Error processing message: {e}")
        return "An error occurred. Please try again."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
