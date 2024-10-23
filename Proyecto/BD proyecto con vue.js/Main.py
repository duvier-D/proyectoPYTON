import bcrypt
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Conexion import create, get_db
from Modelo import *
from Schemes import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # añadir más orígenes si es necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

base.metadata.create_all(bind=create)

# ----------------------------- Registro Pesos -----------------------------

@app.post("/insertarpesos", response_model=RegistroPesosBase)
async def crear_registro(registro: RegistroPesosBase, db: Session = Depends(get_db)):
    nuevo_registro = RegistroPesos(**registro.dict())
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return nuevo_registro

@app.get("/consultarpesos", response_model=list[RegistroPesosBase])
async def obtener_registros(db: Session = Depends(get_db)):
    registros = db.query(RegistroPesos).all()
    return registros

@app.get("/consultarpesos/{empleado_documento}", response_model=RegistroPesosBase)
async def obtener_registro_por_documento(empleado_documento: int, db: Session = Depends(get_db)):
    registro = db.query(RegistroPesos).filter(RegistroPesos.empleado_documento == empleado_documento).first()
    if registro is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

# ----------------------------- Entrega EPP -----------------------------

@app.post("/insertarepp", response_model=EntregaEPPBase)
async def crear_entrega(entrega: EntregaEPPBase, db: Session = Depends(get_db)):
    nueva_entrega = EntregaEPP(**entrega.dict())
    db.add(nueva_entrega)
    db.commit()
    db.refresh(nueva_entrega)
    return nueva_entrega

@app.get("/consultarepp", response_model=list[EntregaEPPBase])
async def obtener_entregas(db: Session = Depends(get_db)):
    entregas = db.query(EntregaEPP).all()
    return entregas

@app.get("/consultarepp/{empleado_documento}", response_model=EntregaEPPBase)
async def obtener_entrega_por_documento(empleado_documento: int, db: Session = Depends(get_db)):
    entrega = db.query(EntregaEPP).filter(EntregaEPP.empleado_documento == empleado_documento).first()
    if entrega is None:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return entrega

# ----------------------------- Usuarios -----------------------------

@app.post("/insertarusuario", response_model=UsuarioBase)
async def crear_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/consultarusuarios", response_model=list[UsuarioBase])
async def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

@app.put("/modificarusuario/{documento}", response_model=UsuarioBase)
async def modificar_usuario(documento: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.documento == documento).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar los campos del usuario
    for key, value in usuario.dict().items():
        setattr(usuario_existente, key, value)

    db.commit()
    db.refresh(usuario_existente)
    return usuario_existente

@app.delete("/eliminarusuario/{documento}")
async def eliminar_usuario(documento: int, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.documento == documento).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario_existente)
    db.commit()
    return {"message": "Usuario eliminado"}

# ----------------------------- Credenciales -----------------------------

@app.post("/insertarcredencial", response_model=CredencialesBase)
async def crear_credencial(credencial: CredencialesBase, db: Session = Depends(get_db)):
    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(credencial.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    nueva_credencial = Credenciales(
        empleado_documento=credencial.empleado_documento,
        password=hashed_password
    )
    
    db.add(nueva_credencial)
    db.commit()
    db.refresh(nueva_credencial)
    return nueva_credencial

@app.get("/consultarcredenciales", response_model=list[CredencialesBase])
async def obtener_credenciales(db: Session = Depends(get_db)):
    credenciales = db.query(Credenciales).all()
    return credenciales

@app.put("/modificarcredencial/{empleado_documento}", response_model=CredencialesBase)
async def modificar_credencial(empleado_documento: int, credencial: CredencialesBase, db: Session = Depends(get_db)):
    credencial_existente = db.query(Credenciales).filter(Credenciales.empleado_documento == empleado_documento).first()
    if not credencial_existente:
        raise HTTPException(status_code=404, detail="Credencial no encontrada")

    # Verificar si se está actualizando la contraseña
    if credencial.password:
        # Encriptar la nueva contraseña
        hashed_password = bcrypt.hashpw(credencial.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        credencial_existente.password = hashed_password
    else:
        # Mantener la contraseña actual si no se proporciona una nueva
        credencial_existente.password = credencial_existente.password

    # Actualizar otros campos de las credenciales
    for key, value in credencial.dict().items():
        if key != 'password':  # No actualizar la contraseña si no se proporciona una nueva
            setattr(credencial_existente, key, value)
    
    db.commit()
    db.refresh(credencial_existente)
    return credencial_existente

@app.delete("/eliminarcredencial/{empleado_documento}")
async def eliminar_credencial(empleado_documento: int, db: Session = Depends(get_db)):
    credencial_existente = db.query(Credenciales).filter(Credenciales.empleado_documento == empleado_documento).first()
    if not credencial_existente:
        raise HTTPException(status_code=404, detail="Credencial no encontrada")

    db.delete(credencial_existente)
    db.commit()
    return {"message": "Credencial eliminada exitosamente"}

# ----------------------------- Login -----------------------------

@app.post("/login")
async def login(request: Login, db: Session = Depends(get_db)):
    # Buscar el usuario por nombre de usuario
    credencial = db.query(Credenciales).filter(Credenciales.empleado_documento == request.nombre_usuario).first()
    
    # Verificar si el usuario existe
    if not credencial:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    # Verificar la contraseña
    if not bcrypt.checkpw(request.password.encode('utf-8'), credencial.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )
    
    # Obtener el rol del usuario a través de la relación de credenciales y usuario
    usuario = db.query(Usuario).filter(Usuario.documento == credencial.empleado_documento).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return {
        "message": "Inicio de sesión exitoso",
        "nombre": usuario.nombre,
        "rol": usuario.rol,
    }
