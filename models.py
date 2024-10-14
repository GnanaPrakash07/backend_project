from motor import motor_asyncio
from pydantic import BaseModel

client = motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["tasks"]
tasks_collection = db["tasks"]

class TaskSchema(BaseModel):
    title: str
    is_completed: bool = False

class TaskUpdateSchema(BaseModel):
    title: str = None
    is_completed: bool = None
