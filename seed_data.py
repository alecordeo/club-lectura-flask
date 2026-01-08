from database import SessionLocal
from models import Usuario, Libro

def seed_database():
    db = SessionLocal()

    # ===== ADMINS =====
    admins = [
        ("admin1", "admin1@mail.com", "admin123"),
        ("admin2", "admin2@mail.com", "admin123"),
    ]

    for username, email, password in admins:
        if not db.query(Usuario).filter_by(username=username).first():
            u = Usuario(username=username, email=email, rol="admin")
            u.set_password(password)
            db.add(u)

    # ===== USERS =====
    usuarios = [
        "lector01","lector02","lector03","lector04","lector05",
        "lector06","lector07","lector08","lector09","lector10",
        "lector11","lector12","lector13","lector14","lector15",
    ]

    for name in usuarios:
        if not db.query(Usuario).filter_by(username=name).first():
            u = Usuario(username=name, email=f"{name}@mail.com", rol="user")
            u.set_password("user123")
            db.add(u)

    # ===== LIBROS =====
    libros = [
        ("La ciudad y los perros", "Mario Vargas Llosa", "Seix Barral", 1963),
        ("Crimen y castigo", "Fiódor Dostoyevski", "Alianza", 1866),
        ("Cien años de soledad", "Gabriel García Márquez", "Sudamericana", 1967),
        ("1984", "George Orwell", "Secker & Warburg", 1949),
    ]

    for titulo, autor, editorial, anio in libros:
        if not db.query(Libro).filter_by(titulo=titulo).first():
            db.add(Libro(
                titulo=titulo,
                autor=autor,
                editorial=editorial,
                anio_publicacion=anio
            ))

    db.commit()
    db.close()
    print("✔ Base inicializada correctamente")
