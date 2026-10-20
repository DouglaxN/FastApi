from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine
from sqlalchemy.orm import joinedload


# Cria as tabelas no PostgreSQL (caso não existam)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/estudantes/', response_model=schemas.Estudante)
def criar_estudante(estudante: schemas.EstudanteCreate, db: Session = Depends(get_db)):
    db_estudante = models.Estudante(nome = estudante.nome, email = estudante.email,perfil = models.Perfil(**estudante.perfil.model_dump()))
    db.add(db_estudante)
    db.commit()
    db.refresh(db_estudante)
    return db_estudante

@app.get('/estudantes/', response_model=List[schemas.Estudante])
def listar_estudantes(db: Session = Depends(get_db)):
    estudantes = db.query(models.Estudante).options(joinedload(models.Estudante.perfil)).all()
    return estudantes