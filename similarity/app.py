# from typing_extensions import Annotated
import chromadb
import datetime
import uvicorn
from fastapi import FastAPI
from user import User
from operator import attrgetter

app = FastAPI()
chroma_client = chromadb.HttpClient(host="localhost", port=8001)
# collection = chroma_client.get_or_create_collection("testname")

# @app.get("/")
# async def root():

#     heartbeat = chroma_client.heartbeat()
#     count = chroma_client.heartbeat()
#     u_id = user.u_id
#     u_chat_id = user.u_chat_id
#     u_profile = user.u_profile
#     u_platform = user.u_platform
#     u_data = user.u_data
#     return {heartbeat:count}

# @app.get("/peek")
# async def peek():
#     return collection.peek()


# @app.post("/initialise")
# async def initialise():
#     try:
#         collection = chroma_client.get_or_create_collection("testname")

#         data = populate_db()
#         collection.add(
#             documents=data[0],
#             metadatas=data[1],
#             ids=data[2],
#         )

#         return [{"message":"OK"}, collection]
#     except Exception as e:
#         return {"message" : e.args}

# @app.post("/delete")
# async def delete_items():
#     chroma_client.delete_collection(name="testname")
    
#     return {"message": "OK"}

# @app.post("/add")
# async def add(query: RequestData):
#     user = User(query.u_id, query.u_profile,query.u_platform)
#     data = query.data
    
    
#     # collection.add(
#     #     documents=req.documents,
#     #     metadatas=req.metadatas,
#     #     ids= id
#     # )

#     return {"u_id": user, "data": data}

# @app.post("/search")
# async def query_db():
#     results = collection.query(
#     query_texts=["produits de la mer"],
#     n_results=5,
#     # where={"style": "style2"}
#     )

#     return results

@app.post("/add")
async def add_data(user: User):
    u_id ,u_chat_id, u_profile, u_platform, u_data = attrgetter('u_id', 'u_chat_id', 'u_profile', 'u_platform', 'u_data')(user)

    time_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    db_name = u_id + '.' + u_chat_id

    collection = chroma_client.get_or_create_collection(db_name)

    try:
        collection.add(
            documents = u_data,
            metadatas = [{
                "u_chat_id": u_chat_id, 
                "u_profile": u_profile, 
                "u_platform": u_platform, 
                "time": time_now
                }],
            ids = db_name + '.' + time_now
        )
    except Exception as e:
        return {"message": e.args}

    return {"200": "OK"}


@app.post("/search")
async def query_db(user: User):
    u_id ,u_chat_id, u_profile, u_platform, u_data = attrgetter('u_id', 'u_chat_id', 'u_profile', 'u_platform', 'u_data')(user)

    db_name = u_id + '.' + u_chat_id

    collection = chroma_client.get_or_create_collection(db_name)

    try:
        results = collection.query(
        query_texts= u_data,
        n_results=5,
        where={'$and': [{"u_profile": u_profile}, {"u_platform": u_platform}]}
        )
    except Exception as e:
        return {"message": e.args}

    return results

@app.post("/user")
async def send_user(user: User):
    # u_id = user.u_id
    # u_chat_id = user.u_chat_id
    # u_profile = user.u_profile
    # u_platform = user.u_platform
    # u_data = user.u_data

    u_id ,u_chat_id, u_profile, u_platform, u_data = attrgetter('u_id', 'u_chat_id', 'u_profile', 'u_platform', 'u_data')(user)

    message = {
        "id": u_id,
        "metadata": {"user_chat": u_chat_id, "profile": u_profile, "platform": u_platform},
        "data": u_data
    }

    return message


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
