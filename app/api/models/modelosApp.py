from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Instancia para la base de datos para crear tablas
Base = declarative_base()

# Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50))
    edad = Column(Integer)
    telefono = Column(String(14))
    correo = Column(String(20))
    contrasena = Column(String(10))
    fechaRegistro = Column(Date)
    ciudad = Column(String(50))

    # Relaciones
    remitente_transacciones = relationship('Transaccion', foreign_keys='Transaccion.remitente_id', back_populates='remitente')
    destinatario_transacciones = relationship('Transaccion', foreign_keys='Transaccion.destinatario_id', back_populates='destinatario')

# Gasto
class Gasto(Base):
    __tablename__ = 'gastos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Float)
    fecha = Column(Date)
    descripcion = Column(String(100))
    nombre = Column(String(50))
    categoria_id = Column(Integer, ForeignKey('categoria.id'))

    # Relaciones
    categoria = relationship('Categoria', back_populates='gastos')

# Categoría
class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombreCategoria = Column(String(100))
    descripcion = Column(String(100))
    fotoIcono = Column(String(50))

    # Relaciones
    gastos = relationship('Gasto', back_populates='categoria')
    presupuestos = relationship('Presupuesto', back_populates='categoria')
    ingresos = relationship('Ingreso', back_populates='categoria')

# Ingreso Transacción
class Transaccion(Base):
    __tablename__ = 'ingresoTransaccion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Float)
    fecha = Column(Date)
    remitente_id = Column(Integer, ForeignKey('usuarios.id'))
    destinatario_id = Column(Integer, ForeignKey('usuarios.id'))
    metodoPago_id = Column(Integer, ForeignKey('metodoPago.id'))
    tipoTransaccion_id = Column(Integer, ForeignKey('tipos_transaccion.id'))

    # Relaciones
    remitente = relationship('Usuario', foreign_keys=[remitente_id], back_populates='remitente_transacciones')
    destinatario = relationship('Usuario', foreign_keys=[destinatario_id], back_populates='destinatario_transacciones')
    metodo_pago = relationship('Pago', back_populates='transacciones')
    tipo_transaccion = relationship('TipoTransaccion', back_populates='transacciones')

# Método de Pago
class Pago(Base):
    __tablename__ = 'metodoPago'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombreMetodo = Column(String(100))
    descripcion = Column(String(100))
    entidad = Column(String(100))

    # Relaciones
    transacciones = relationship('Transaccion', back_populates='metodo_pago')

# Presupuesto
class Presupuesto(Base):
    __tablename__ = 'presupuestos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Float, nullable=False)
    fechaInicio = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))

    # Relaciones
    categoria = relationship('Categoria', back_populates='presupuestos')

# Tipo de Transacción
class TipoTransaccion(Base):
    __tablename__ = 'tipos_transaccion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(100))

    # Relaciones
    transacciones = relationship('Transaccion', back_populates='tipo_transaccion')

# Ingreso (como alternativa a la tabla de transacción de ingresos)
class Ingreso(Base):
    __tablename__ = 'ingresos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    monto = Column(Float)
    fecha = Column(Date)
    descripcion = Column(String(100))
    categoria_id = Column(Integer, ForeignKey('categoria.id'))

    # Relaciones
    categoria = relationship('Categoria', back_populates='ingresos')
