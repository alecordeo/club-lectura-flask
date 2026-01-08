from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash


# =========================
# CLUB
# =========================
class Club(Base):
    __tablename__ = "clubes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)

    usuarios = relationship("Usuario", back_populates="club")


# =========================
# USUARIO
# =========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), default="user")
    fecha_creacion = Column(Date, default=date.today)

    nombre = Column(String(100))
    club_id = Column(Integer, ForeignKey("clubes.id"))

    club = relationship("Club", back_populates="usuarios")

    prestamos = relationship("Prestamo", back_populates="usuario")
    resenas = relationship("Resena", back_populates="usuario")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# =========================
# LIBRO
# =========================
class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    autor = Column(String(100))
    editorial = Column(String(100))
    anio_publicacion = Column(Integer)

    prestamos = relationship("Prestamo", back_populates="libro")
    resenas = relationship("Resena", back_populates="libro")


# =========================
# PRÉSTAMO
# =========================
class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    fecha_inicio = Column(Date, default=date.today)
    fecha_fin = Column(Date)

    usuario = relationship("Usuario", back_populates="prestamos")
    libro = relationship("Libro", back_populates="prestamos")


# =========================
# RESEÑA
# =========================
class Resena(Base):
    __tablename__ = "resenas"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    calificacion = Column(Integer, nullable=False)
    comentario = Column(Text)
    fecha = Column(Date, default=date.today)

    usuario = relationship("Usuario", back_populates="resenas")
    libro = relationship("Libro", back_populates="resenas")