import chromadb
import datetime
import uvicorn
from fastapi import FastAPI
from user.user import User
from operator import attrgetter

app = FastAPI()
chroma_client = chromadb.HttpClient(host="localhost", port=8001)


@app.post("/add")
async def add_data(user: User):
    u_id ,u_chat_id, u_profile, u_platform, u_data = attrgetter('u_id', 'u_chat_id', 'u_profile', 'u_platform', 'u_data')(user)

    time_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = '.'.join([u_id, u_chat_id, time_now])

    collection = chroma_client.get_or_create_collection(u_id)
    try:
        collection.add(
            documents = u_data,
            metadatas = [{
                "u_chat_id": u_chat_id, 
                "u_profile": u_profile, 
                "u_platform": u_platform, 
                "time": time_now
                }],
            ids = unique_id
        )
    except Exception as e:
        return {"message": e.args}

    return {"200": "OK"}


@app.post("/search")
async def query_db(user: User):
    u_id ,u_chat_id, u_profile, u_platform, u_data = attrgetter('u_id', 'u_chat_id', 'u_profile', 'u_platform', 'u_data')(user)

    collection = chroma_client.get_or_create_collection(u_id)

    try:
        results = collection.query(
        query_texts= u_data,
        n_results = 5,
        where = {'$and': [
            {"u_chat_id": u_chat_id},
            {"u_profile": u_profile},
            {"u_platform": u_platform}
            ]}
        )
    except Exception as e:
        return {"message": e.args}

    return results

@app.post("/user")
async def send_user(user: User):
    u_id ,u_chat_id, u_profile, u_platform, u_data = attrgetter('u_id', 'u_chat_id', 'u_profile', 'u_platform', 'u_data')(user)

    message = {
        "id": u_id,
        "metadata": {"user_chat": u_chat_id, "profile": u_profile, "platform": u_platform},
        "data": u_data
    }

    return message


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
