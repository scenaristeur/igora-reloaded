from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Data(BaseModel):
    """format of chat's POST query"""

    user_id: str
    metadata: list[dict]
    data: str


class PDFQuery(BaseModel):
    """format of pdf's POST query"""

    data: str


class User(BaseModel):
    """Format of user"""

    username: str
    password: str
