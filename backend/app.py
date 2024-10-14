from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from auth import get_current_user
from database import SessionLocal, engine, Base
import cache

app = FastAPI()

# Modelos de dados
class Task(BaseModel):
    title: str
    status: bool = False

# Criação do banco de dados
Base.metadata.create_all(bind=engine)

# Rota para listar tarefas
@app.get("/tasks/")
def get_tasks(db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    # Cache Redis
    tasks = cache.get_cached_tasks(user)
    if tasks is None:
        tasks = db.query(TaskModel).filter(TaskModel.user == user).all()
        cache.set_cached_tasks(user, tasks)
    return tasks

# Rota para adicionar tarefa
@app.post("/tasks/")
def add_task(task: Task, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    db_task = TaskModel(title=task.title, user=user)
    db.add(db_task)
    db.commit()
    cache.invalidate_cache(user)
    return db_task

# Rota para remover tarefa
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user == user).first()
    if task:
        db.delete(task)
        db.commit()
        cache.invalidate_cache(user)
    else:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
