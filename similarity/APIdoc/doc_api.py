import os
from dotenv import load_dotenv

import chromadb
import similarity.data_structure.data as query
import database_query_methods.chroma_methods as chroma_methods

from fastapi import APIRouter
from operator import attrgetter

load_dotenv()
CHROMA_DB_HOST = os.getenv("CHROMA_DB_HOST")
CHROMA_DB_PORT = os.getenv("CHROMA_DB_PORT")
NUMBER_RESULTS = int(os.getenv("RESULT_NUMBER"))
PDF_COLLECTION_NAME = os.getenv("PDF_COLLECTION_NAME")

router = APIRouter()
chroma_server_client = chromadb.HttpClient(host=CHROMA_DB_HOST, port=CHROMA_DB_PORT)


@router.post("/pdfsearch")
async def query_pdf_collection(data: query.PDFQuery):

    text_query = attrgetter("data")(data)
    results = await chroma_methods.pdf_query(
        text_query, NUMBER_RESULTS, PDF_COLLECTION_NAME, chroma_server_client
    )

    return results
