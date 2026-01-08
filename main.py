from database import engine, SessionLocal, Base
from models import Club, Socio, Libro, Prestamo
from datetime import date

# Crear tablas
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas")

db = SessionLocal()

# Crear club
club = db.query(Club).filter_by(nombre="Club de Lectura ESCOM").first()
if not club:
    club = Club(
        nombre="Club de Lectura ESCOM",
        descripcion="Club para fomentar la lectura entre estudiantes"
    )
    db.add(club)
    db.commit()
    db.refresh(club)

# Crear socio
socio = db.query(Socio).filter_by(correo="ian@email.com").first()
if not socio:
    socio = Socio(
        nombre="Ian",
        correo="ian@email.com",
        club_id=club.id
    )
    db.add(socio)
    db.commit()
    db.refresh(socio)

# Crear libro
libro = db.query(Libro).filter_by(titulo="Crimen y Castigo").first()
if not libro:
    libro = Libro(
        titulo="Crimen y Castigo",
        autor="Fiódor Dostoyevski",
        editorial="Penguin Clásicos",
        anio_publicacion=1866
    )
    db.add(libro)
    db.commit()
    db.refresh(libro)

# Crear préstamo
prestamo = db.query(Prestamo).filter_by(
    socio_id=socio.id,
    libro_id=libro.id
).first()

if not prestamo:
    prestamo = Prestamo(
        socio_id=socio.id,
        libro_id=libro.id,
        fecha_inicio=date.today()
    )
    db.add(prestamo)
    db.commit()

print("✅ Datos insertados correctamente")

print("\n🔄 PRÉSTAMOS REGISTRADOS:")
prestamos = db.query(Prestamo).all()

for p in prestamos:
    print(
        f"Socio: {p.socio.nombre} | "
        f"Libro: {p.libro.titulo} | "
        f"Fecha: {p.fecha_inicio}"
    )

db.close()
