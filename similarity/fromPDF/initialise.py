import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.embeddings import OpenAIEmbeddings
# from langchain.chains.question_answering import load_qa_chain
# from langchain_community.chat_models import ChatOpenAI
# from langchain_community.vectorstores import Chroma
import chromadb

def load_chunk_persist_pdf():
    pdf_folder_path = "/home/stag/igora-reload/similarity/fromPDF/documentsPDF"
    documents = []

    for file in os.listdir(pdf_folder_path):

        if file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)

    id_chunked_docs = [str(x) for x in list(range(len(chunked_documents)))]

    client = chromadb.Client()
    test_collection = client.get_or_create_collection("pdf_collection")

    test_collection.add(
        documents = [element.page_content for element in chunked_documents],
        ids = id_chunked_docs
    )


    results = test_collection.query(
        query_texts="e locaux à fort enjeu \xa0dans le cadre des restructurations de services des tribunaux judiciaires de \nNanterre et Versailles ainsi que, plus globalement, la couverture de durées d'engagement plus longues des baux \nnégociés par les services des domaines ;\n•l'engagement des marchés de maintenance pris dans le cadre des marchés globaux de performance pour la \nconstruction ou la réhabilitation des palais de justice de Cayenne, de Saint-Laurent-du-Maroni (Guyane) et Saint-\nMartin (Antilles françaises) ;\n•le réengagement des marchés interministériels d'électricité et de gaz pour la période d'approvisionnement 2022-\n2023.\nLes crédits de paiement sont préservés par rapport à une dépense",
        n_results=2
    )


    return results


def print_results(results, n_query):

    for i in range(n_query):
        print(f"{results['ids'][0][i]}")
        print(f"{results['distances'][0][i]}")
        print(f"{results['metadatas'][0][i]}")
        print(f"{results['documents'][0][i]}")
        print('\n\n')
        i+=1

if __name__ == "__main__":

    test_var = load_chunk_persist_pdf()
    print_results(test_var, 2)
