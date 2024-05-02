import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.chains.question_answering import load_qa_chain
# from langchain_community.chat_models import ChatOpenAI
# from langchain_community.vectorstores import Chroma
import chromadb
import dcf

COLLECTION_NAME = "pdf_collection"
HOST = "localhost"
PORT = 8000

chroma_server_client = chromadb.HttpClient(host="localhost", port="8001")


def create_pdf_collection(collection_name: str = COLLECTION_NAME):
    pdf_folder_path = "/home/stag/igora-reload/similarity/fromPDF/documentsPDF"
    documents = []

    for file in os.listdir(pdf_folder_path):

        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200
    )
    chunked_documents = text_splitter.split_documents(documents)

    if chunked_documents:
        id_chunked_docs = [str(x) for x in list(range(len(chunked_documents)))]

        # client = chromadb.Client()
        test_collection = chroma_server_client.get_or_create_collection(collection_name)

        test_collection.add(
            documents=[element.page_content for element in chunked_documents],
            ids=id_chunked_docs,
        )

        print(f"collection: {collection_name}, created")
        dcf.update_list(dcf.get_folder_pdf())
    else:
        print(f"No pdf files in folder: {collection_name} not created")


def delete_pdf_collection(collection_name: str = COLLECTION_NAME):
    # client = chromadb.Client()
    chroma_server_client.delete_collection(name=collection_name)


def query_pdf_collection(
    text: str, result_number: int = 5, collection_name: str = COLLECTION_NAME
):
    # client = chromadb.Client()
    pdf_collection = chroma_server_client.get_or_create_collection(collection_name)

    results = pdf_collection.query(query_texts=text, n_results=result_number)
    return results


def print_results(results, n_query):

    for i in range(n_query):
        print(f"{results['ids'][0][i]}")
        print(f"{results['distances'][0][i]}")
        print(f"{results['metadatas'][0][i]}")
        print(f"{results['documents'][0][i]}")
        print("\n\n")
        i += 1


if __name__ == "__main__":
    create_pdf_collection()
