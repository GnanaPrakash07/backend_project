from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import TaskSchema, TaskUpdateSchema, tasks_collection

app = FastAPI()

@app.post("/v1/tasks", status_code=201)
async def create_task(task: TaskSchema):
    new_task = await tasks_collection.insert_one({"title": task.title, "is_completed": task.is_completed})
    return {"id": new_task.inserted_id}

@app.get("/v1/tasks", status_code=200)
async def list_all_tasks():
    tasks = await tasks_collection.find().to_list(length=100)
    return {"tasks": [{"id": task["_id"], "title": task["title"], "is_completed": task["is_completed"]} for task in tasks]}

@app.get("/v1/tasks/{id}", status_code=200)
async def get_task(id: str):
    task = await tasks_collection.find_one({"_id": id})
    if task is None:
        raise HTTPException(status_code=404, detail="There is no task at that id")
    return {"id": task["_id"], "title": task["title"], "is_completed": task["is_completed"]}

@app.delete("/v1/tasks/{id}", status_code=204)
async def delete_task(id: str):
    await tasks_collection.delete_one({"_id": id})
    return None

@app.put("/v1/tasks/{id}", status_code=204)
async def update_task(id: str, task: TaskUpdateSchema):
    task_obj = await tasks_collection.find_one({"_id": id})
    if task_obj is None:
        raise HTTPException(status_code=404, detail="There is no task at that id")
    update_data = {}
    if task.title is not None:
        update_data["title"] = task.title
    if task.is_completed is not None:
        update_data["is_completed"] = task.is_completed
    await tasks_collection.update_one({"_id": id}, {"$set": update_data})
    return None

@app.post("/v1/tasks/bulk", status_code=201)
async def bulk_create_tasks(tasks: list[TaskSchema]):
    new_tasks = [{"title": task.title, "is_completed": task.is_completed} for task in tasks]
    result = await tasks_collection.insert_many(new_tasks)
    return {"tasks": [{"id": id} for id in result.inserted_ids]}

@app.delete("/v1/tasks/bulk", status_code=204)
async def bulk_delete_tasks(tasks: list[str]):
    await tasks_collection.delete_many({"_id": {"$in": tasks}})
    return None
