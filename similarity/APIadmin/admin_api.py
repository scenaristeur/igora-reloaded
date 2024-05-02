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
# NUMBER_RESULTS = int(os.getenv("RESULT_NUMBER"))
PDF_COLLECTION_NAME = os.getenv("PDF_COLLECTION_NAME")
PDF_FOLDER_PATH = os.getenv("PDF_FOLDER_PATH")

router = APIRouter()
chroma_client = chromadb.HttpClient(host=CHROMA_DB_HOST, port=CHROMA_DB_PORT)


def is_admin(username: str, password: str) -> bool:
    """Method to verify user is admin"""

    return True


@router.post("/admin/create_pdf_collection")
async def create_collection(user: datas.User):

    username, password = attrgetter("username", "password")(user)

    if is_admin(username, password):

        result = await chroma_methods.create_pdf_collection(
            PDF_FOLDER_PATH, PDF_COLLECTION_NAME, chroma_client
        )
        return result

    return {"403": f"{user} has no admin rights"}


@router.post("/admin/delete_pdf_collection")
async def delete_collection(user: datas.User):

    username, password = attrgetter("username", "password")(user)

    if is_admin(username, password):

        chroma_client.delete_collection(name=PDF_COLLECTION_NAME)
        return {"200": f"Collection {PDF_COLLECTION_NAME}: deleted"}

    return {"403": f"{user} has no admin rights"}
