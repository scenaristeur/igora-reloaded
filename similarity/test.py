# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# class UserCreate(BaseModel):
#     user_cl: int
#     username: str

# @app.post("/create_user/")
# async def create_user(user_data: UserCreate):
#     user_f = user_data.user_cl
#     username = user_data.username
#     return {
# 		"msg": "we got data succesfully",
# 		"user_id": user_f,
# 		"username": username,
# 	}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="127.0.0.1", port=8000)

import datetime

print(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
      
      
