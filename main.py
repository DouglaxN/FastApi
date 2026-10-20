from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal, engine

# Cria as tabelas no PostgreSQL (caso não existam)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/estudantes/', response_model=schemas.EstudanteResponse)
def create_student(estudante: schemas.EstudanteCreate, db: Session = Depends(get_db)):
    db_estudante = models.Estudante(**estudante.model_dump())
    db.add(db_estudante)
    db.commit()
    db.refresh(db_estudante)
    return db_estudante

@app.get('/estudantes/', response_model=List[schemas.EstudanteResponse])
def read_students(db: Session = Depends(get_db)):
    estudantes = db.query(models.Estudante).all()
    return estudantes