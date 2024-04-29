#! /usr/bin/env python3
import sys
import os

sys.path.append(os.path.join(os.getcwd(), os.pardir))

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

# import similarity.chatAPI.app as chat_app
from APIchat import chat_api as chat_app
from APIdoc import doc_api as doc_app
from APIadmin import admin_api as admin_app

load_dotenv()
API_HOST = os.getenv("API_HOST")
API_PORT = int(os.getenv("API_PORT"))

app = FastAPI()
app.include_router(chat_app.router)
app.include_router(doc_app.router)
app.include_router(admin_app.router)


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
