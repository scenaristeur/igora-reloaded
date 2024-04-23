from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class User(BaseModel):
    """format of user's information"""
    u_id: str
    u_chat_id: str
    u_profile: str
    u_platform: str
    u_data: str

