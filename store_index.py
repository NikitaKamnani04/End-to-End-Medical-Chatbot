
from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import Pinecone, ServerlessSpec, PineconeApiException
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


extracted_data = load_pdf_file(data='Data/')
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)
# Define the index name
index_name = "medicalbot"

# List existing indexes
existing_indexes = pc.list_indexes()

# Check if the index already exists
if index_name in existing_indexes:
    print(f"Index '{index_name}' already exists. Skipping creation.")
else:
    try:
        print(f"Creating index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=384,  # Replace with your model dimensions
            metric="cosine",  # Replace with your model metric
            spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Specify your cloud and region
        )
        print(f"Index '{index_name}' created successfully.")
    except PineconeApiException as e:
        print(f"Error creating index: {e}")

    #Embed each chunk and upsert the embeddings into your Pinecone Index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)