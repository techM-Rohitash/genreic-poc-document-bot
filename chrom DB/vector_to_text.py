import os
import chromadb
from PyPDF2 import PdfReader

# Initialize the ChromaDB client
client = chromadb.Client()

# Create a collection (if it doesn't exist)
collection_name = "pdf_collection"
collection = client.get_or_create_collection(collection_name)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def store_in_chromadb(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    
    # Generate a unique ID for the document
    doc_id = os.path.basename(pdf_file).replace(".pdf", "")
    
    collection.add(
        ids=[doc_id],
        documents=[text],
        metadatas=[{"filename": pdf_file}]
    )
    print(f"Text from {pdf_file} has been stored in the ChromaDB collection.")
def fetch_and_store_in_file():
    # Fetch all documents from the collection
    results = collection.get()

    # File to store the fetched data
    output_file = "fetched_data.txt"
    
    with open(output_file, 'w', encoding='utf-8') as file:
        for doc_id, doc_content, metadata in zip(results['ids'], results['documents'], results['metadatas']):
            file.write(f"Document ID: {doc_id}\n")
            file.write(f"Filename: {metadata['filename']}\n")
            file.write("Content:\n")
            file.write(doc_content + "\n")
            file.write("-" * 80 + "\n")
    
    print(f"Fetched data has been stored in {output_file}")


if __name__ == "__main__":
    pdf_file = input("Enter the name of the PDF file (including extension): ")

    # Check if the file exists
    if os.path.exists(pdf_file) and pdf_file.endswith(".pdf"):
        store_in_chromadb(pdf_file)
        fetch_and_store_in_file()

        # Print the location of the vector database
        vector_db_location = os.path.expanduser("~/.cache/chroma")
        print(f"The vector database is stored at: {vector_db_location}")
    else:
        print(f"{pdf_file} does not exist or is not a valid PDF file.")
