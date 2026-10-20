from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Estudante(Base):
    __tablename__ = "estudantes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    perfil = relationship("Perfil", back_populates="estudante", uselist=False, cascade="all, delete-orphan")
    
class Perfil(Base):
    __tablename__ = "perfis"
    
    id = Column(Integer, primary_key=True, index=True)
    idade = Column(Integer)
    endereco = Column(String)
    estudante_id = Column(Integer, ForeignKey("estudantes.id"), unique=True)
    estudante = relationship("Estudante", back_populates="perfil")