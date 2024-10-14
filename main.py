from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from models import Task, engine

app = FastAPI()

Session = sessionmaker(bind=engine)
session = Session()

class TaskSchema(BaseModel):
    title: str
    is_completed: bool = False

class TaskUpdateSchema(BaseModel):
    title: str = None
    is_completed: bool = None

@app.post("/v1/tasks", status_code=201)
async def create_task(task: TaskSchema):
    new_task = Task(title=task.title, is_completed=task.is_completed)
    session.add(new_task)
    session.commit()
    return {"id": new_task.id}

@app.get("/v1/tasks", status_code=200)
async def list_all_tasks():
    tasks = session.query(Task).all()
    return {"tasks": [{"id": task.id, "title": task.title, "is_completed": task.is_completed} for task in tasks]}

@app.get("/v1/tasks/{id}", status_code=200)
async def get_task(id: int):
    task = session.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="There is no task at that id")
    return {"id": task.id, "title": task.title, "is_completed": task.is_completed}

@app.delete("/v1/tasks/{id}", status_code=204)
async def delete_task(id: int):
    task = session.query(Task).filter(Task.id == id).first()
    if task is not None:
        session.delete(task)
        session.commit()
    return None

@app.put("/v1/tasks/{id}", status_code=204)
async def update_task(id: int, task: TaskUpdateSchema):
    task_obj = session.query(Task).filter(Task.id == id).first()
    if task_obj is None:
        raise HTTPException(status_code=404, detail="There is no task at that id")
    if task.title is not None:
        task_obj.title = task.title
    if task.is_completed is not None:
        task_obj.is_completed = task.is_completed
    session.commit()
    return None

@app.post("/v1/tasks/bulk", status_code=201)
async def bulk_create_tasks(tasks: list[TaskSchema]):
    new_tasks = [Task(title=task.title, is_completed=task.is_completed) for task in tasks]
    session.add_all(new_tasks)
    session.commit()
    return {"tasks": [{"id": task.id} for task in new_tasks]}

@app.delete("/v1/tasks/bulk", status_code=204)
async def bulk_delete_tasks(tasks: list[int]):
    for id in tasks:
        task = session.query(Task).filter(Task.id == id).first()
        if task is not None:
            session.delete(task)
    session.commit()
    return None
