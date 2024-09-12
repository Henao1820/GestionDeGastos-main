from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from models import Base, Usuario, Gasto, Categoria, Transaccion, Pago, Presupuesto, TipoTransaccion, Ingreso
from database import engine, sessionLocal

app = FastAPI()

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Define los esquemas de Pydantic
class UsuarioBase(BaseModel):
    nombre: str
    edad: int
    telefono: str
    correo: str
    contrasena: str
    fechaRegistro: str
    ciudad: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int

# CRUD para Usuario
@app.post("/usuarios/", response_model=UsuarioResponse)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=List[UsuarioResponse])
def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Función para obtener la sesión de la base de datos
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()