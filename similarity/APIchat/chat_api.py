import os
import sys

sys.path.append(os.path.join(os.getcwd(), os.pardir))

import chromadb


from fastapi import APIRouter
from operator import attrgetter
from dotenv import load_dotenv

import data_structure.data as datas
import database_query_methods.chroma_methods as chroma_methods


load_dotenv()
CHROMA_DB_HOST = os.getenv("CHROMA_DB_HOST")
CHROMA_DB_PORT = os.getenv("CHROMA_DB_PORT")
NUMBER_RESULTS = int(os.getenv("RESULT_NUMBER"))

router = APIRouter()
chroma_client = chromadb.HttpClient(host=CHROMA_DB_HOST, port=CHROMA_DB_PORT)


@router.post("/add")
async def add_data(user_request: datas.Data) -> dict:
    user_id, metadata, data_to_add = attrgetter("user_id", "metadata", "data")(
        user_request
    )

    return_message = await chroma_methods.add_data(
        user_id, metadata, data_to_add, chroma_client
    )
    return return_message


@router.post("/search")
async def query_db(user_request: datas.Data):
    user_id, metadata, query_data = attrgetter("user_id", "metadata", "data")(
        user_request
    )

    results = await chroma_methods.chroma_query(
        user_id, metadata, query_data, NUMBER_RESULTS, chroma_client
    )
    print(f"resultats: {results}")
    return results


