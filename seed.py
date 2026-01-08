from database import SessionLocal
from models import Usuario, Libro

db = SessionLocal()

# =====================
# USUARIOS ADMIN
# =====================
admins = [
    ("admin1", "admin1@mail.com", "admin123"),
    ("admin2", "admin2@mail.com", "admin123"),
]

for username, email, password in admins:
    u = Usuario(username=username, email=email, rol="admin")
    u.set_password(password)
    db.add(u)

# =====================
# USUARIOS NORMALES
# =====================
usuarios = [
    "lector01", "lector02", "lector03", "lector04", "lector05",
    "lector06", "lector07", "lector08", "lector09", "lector10",
    "lector11", "lector12", "lector13", "lector14", "lector15",
]

for name in usuarios:
    u = Usuario(
        username=name,
        email=f"{name}@mail.com",
        rol="user"
    )
    u.set_password("user123")
    db.add(u)

# =====================
# LIBROS
# =====================
libros = [
    # Vargas Llosa
    ("La ciudad y los perros", "Mario Vargas Llosa", "Seix Barral", 1963),
    ("Conversación en La Catedral", "Mario Vargas Llosa", "Seix Barral", 1969),
    ("La fiesta del chivo", "Mario Vargas Llosa", "Alfaguara", 2000),

    # Dostoyevski
    ("Crimen y castigo", "Fiódor Dostoyevski", "Alianza", 1866),
    ("Los hermanos Karamázov", "Fiódor Dostoyevski", "Alianza", 1880),
    ("El idiota", "Fiódor Dostoyevski", "Alianza", 1869),

    # García Márquez
    ("Cien años de soledad", "Gabriel García Márquez", "Sudamericana", 1967),
    ("El amor en los tiempos del cólera", "Gabriel García Márquez", "Oveja Negra", 1985),
    ("Crónica de una muerte anunciada", "Gabriel García Márquez", "Oveja Negra", 1981),

    # Otros clásicos
    ("1984", "George Orwell", "Secker & Warburg", 1949),
    ("Un mundo feliz", "Aldous Huxley", "Chatto & Windus", 1932),
    ("El extranjero", "Albert Camus", "Gallimard", 1942),
    ("Rayuela", "Julio Cortázar", "Sudamericana", 1963),
]

for titulo, autor, editorial, anio in libros:
    l = Libro(
        titulo=titulo,
        autor=autor,
        editorial=editorial,
        anio_publicacion=anio
    )
    db.add(l)

db.commit()
db.close()

print("✔ Datos de prueba insertados correctamente")
