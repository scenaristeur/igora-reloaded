import os
import datetime
import chromadb
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()


def has_key(my_data: list[dict], key_to_find: str) -> bool:
    
    for element in my_data:
        if key_to_find in element.keys():
            return True

    return False


def value_of_key(my_data: list[dict], key_to_find: str) -> str:
    for element in my_data:
        if key_to_find in element.keys():
            return element[key_to_find]

    return ""


def convert_list_to_dict(my_data: list[dict]) -> dict:
    new_dict = {}

    for dictionary in my_data:
        for key, value in dictionary.items():
            new_dict[key] = value

    return new_dict


def split_pdfs(pdf_folder: str):
    
    documents = []
    for file in os.listdir(pdf_folder):

        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200
    )
    chunked_documents = text_splitter.split_documents(documents)
    return chunked_documents


async def add_data(user_id: str, my_metadata: list[dict], my_data: str, chroma_client: chromadb.HttpClient) -> dict:

    if len(my_metadata) < 2:
        return {"400" : "metadata: expected at least 2 elements"}

    if not has_key(my_metadata, "u_chat_id"):
        return {"400" : "metadata: expected u_chat_id"}

    time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = ".".join([user_id, value_of_key(my_metadata, "u_chat_id"), time_now])

    collection = chroma_client.get_or_create_collection(user_id)

    metadata_dict = convert_list_to_dict(my_metadata)

    try:
        collection.add(
            documents = my_data,
            metadatas = [metadata_dict],
            ids = unique_id,
        )
    except Exception as e:
        return {"message": e.args}

    return {"200": "OK"}


async def chroma_query(
    user_id: str, my_metadata: list[dict], search_data: str, number_results: int, chroma_client: chromadb.HttpClient
):

    collection = chroma_client.get_or_create_collection(user_id)
    try:
        if len(my_metadata) >= 2:
            results = collection.query(
                query_texts = search_data,
                n_results = number_results,
                where = {
                    "$and": 
                        my_metadata

                },
            )
        elif len(my_metadata) == 1:
            results = collection.query(
                query_texts = search_data,
                n_results = number_results,
                where = {my_metadata},
            )
        else:
            results = collection.query(
                query_texts = search_data,
                n_results = number_results,
            )
    except Exception as e:
        return {"message": e.args}

    return results


async def pdf_query(search_data: str, number_results: int, collection_name: str, chroma_client: chromadb.HttpClient):

    collection = chroma_client.get_collection(collection_name)
    try:
        results = collection.query(
                query_texts = search_data,
                n_results = number_results,
            )
    except Exception as e:
        return {"message": e.args}

    return results


async def create_pdf_collection(pdf_folder: str , collection_name: str, chroma_client: chromadb.HttpClient):

    print(f'pdf path: {pdf_folder}')
    print(f'pdf collection: {collection_name}')

    chunked_documents = split_pdfs(pdf_folder)
    print('chunked documents done')
    if chunked_documents:
        id_chunked_docs = [str(x) for x in list(range(len(chunked_documents)))]

        test_collection = chroma_client.get_or_create_collection(collection_name)

        print(type(chunked_documents))
        print(type(id_chunked_docs))
        print (chunked_documents[0])
        print(type(chunked_documents[0]))
        print('\n\n')
        print (chunked_documents[1].page_content)
        print (chunked_documents[1].metadata)
        print('\n\n')
        print (chunked_documents[2].page_content)
        print (chunked_documents[2].metadata)
        print('\n\n')
        print (chunked_documents[3].page_content)
        print (chunked_documents[3].metadata)

        test_collection.add(
            documents = [element.page_content for element in chunked_documents],
            metadatas = [element.metadata for element in chunked_documents],
            ids = id_chunked_docs,
        )
        return {"200": f"Collection {collection_name}: added"}
    else:
        return {"404": f"No pdf files in {pdf_folder} not created"}
