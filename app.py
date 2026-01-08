from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy.sql import extract
from datetime import date
from functools import wraps

import os
from seed_data import seed_database

from database import SessionLocal, engine
from models import Base, Club, Libro, Prestamo, Resena, Usuario


app = Flask(__name__)
app.secret_key = "clave-secreta-club-lectura"

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Ejecutar seed SOLO si la variable existe
if os.environ.get("RUN_SEED") == "true":
    seed_database()

# =========================
# LOGIN REQUIRED
# =========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para acceder.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión.", "error")
            return redirect(url_for("login"))

        db = SessionLocal()
        usuario = db.query(Usuario).get(session["user_id"])
        db.close()

        if not usuario or usuario.rol != "admin":
            flash("No tienes permisos para acceder a esta sección.", "error")
            return redirect(url_for("libros"))

        return f(*args, **kwargs)
    return decorated_function


# =========================
# INDEX
# =========================
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# =========================
# CLUBES
# =========================
@app.route("/clubes", methods=["GET", "POST"])
@login_required
@admin_required
def clubes():
    db = SessionLocal()

    if request.method == "POST":
        nuevo_club = Club(
            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"]
        )
        db.add(nuevo_club)
        db.commit()
        db.close()
        return redirect(url_for("clubes"))

    clubes = db.query(Club).all()
    db.close()

    return render_template("clubes.html", clubes=clubes)


# =========================
# LIBROS
# =========================
@app.route("/libros", methods=["GET", "POST"])
@login_required
def libros():
    db = SessionLocal()

    if request.method == "POST":
        if session.get("rol") != "admin":
            flash("No tienes permisos para agregar libros.", "error")
            db.close()
            return redirect(url_for("libros"))
        
        nuevo_libro = Libro(
            titulo=request.form["titulo"],
            autor=request.form["autor"],
            editorial=request.form["editorial"],
            anio_publicacion=request.form["anio"]
        )
        db.add(nuevo_libro)
        db.commit()
        db.close()
        return redirect(url_for("libros"))

    libros = db.query(Libro).all()
    db.close()

    return render_template("libros.html", libros=libros)


# =========================
# PRÉSTAMOS
# =========================
@app.route("/prestamos", methods=["GET", "POST"])
@login_required
def prestamos():
    db = SessionLocal()

    # =========================
    # REGISTRAR PRÉSTAMO
    # =========================
    if request.method == "POST":
        libro_id = request.form["libro"]

        # Verificar solapamiento
        prestamo_activo = db.query(Prestamo).filter(
            Prestamo.libro_id == libro_id,
            Prestamo.fecha_fin.is_(None)
        ).first()

        if prestamo_activo:
            flash("El libro seleccionado no está disponible en este momento.", "error")
            db.close()
            return redirect(url_for("prestamos"))

        nuevo_prestamo = Prestamo(
            usuario_id=session["user_id"],
            libro_id=libro_id
        )
        db.add(nuevo_prestamo)
        db.commit()
        db.close()
        return redirect(url_for("prestamos"))

    # =========================
    # CONSULTA SEGÚN ROL
    # =========================
    if session.get("rol") == "admin":
        prestamos = (
            db.query(Prestamo)
            .options(
                joinedload(Prestamo.usuario),
                joinedload(Prestamo.libro)
            )
            .order_by(Prestamo.fecha_fin.is_(None).desc())
            .all()
        )
    else:
        prestamos = (
            db.query(Prestamo)
            .options(
                joinedload(Prestamo.usuario),
                joinedload(Prestamo.libro)
            )
            .filter(Prestamo.usuario_id == session["user_id"])
            .order_by(Prestamo.fecha_fin.is_(None).desc())
            .all()
        )

    libros = db.query(Libro).all()
    db.close()

    return render_template(
        "prestamos.html",
        prestamos=prestamos,
        libros=libros
    )



# =========================
# CERRAR PRÉSTAMO
# =========================
@app.route("/prestamos/cerrar/<int:prestamo_id>", methods=["POST"])
@login_required
def cerrar_prestamo(prestamo_id):
    db = SessionLocal()
    prestamo = db.query(Prestamo).get(prestamo_id)

    if not prestamo:
        flash("Préstamo no encontrado.", "error")
        db.close()
        return redirect(url_for("prestamos"))

    # USER solo puede cerrar sus préstamos
    if session.get("rol") != "admin" and prestamo.usuario_id != session["user_id"]:
        flash("No tienes permiso para cerrar este préstamo.", "error")
        db.close()
        return redirect(url_for("prestamos"))

    prestamo.fecha_fin = date.today()
    db.commit()
    db.close()

    flash("Préstamo cerrado correctamente.", "success")
    return redirect(url_for("prestamos"))


# =========================
# RESEÑAS
# =========================
@app.route("/resenas", methods=["GET", "POST"])
@login_required
def resenas():
    db = SessionLocal()

    if request.method == "POST":
        nueva_resena = Resena(
            usuario_id=session["user_id"],
            libro_id=request.form["libro"],
            calificacion=request.form["calificacion"],
            comentario=request.form["comentario"]
        )
        db.add(nueva_resena)
        db.commit()
        db.close()
        return redirect(url_for("resenas"))

    resenas = (
        db.query(Resena)
        .options(
            joinedload(Resena.usuario),
            joinedload(Resena.libro)
        )
        .all()
    )

    libros = db.query(Libro).all()
    db.close()

    return render_template(
        "resenas.html",
        resenas=resenas,
        libros=libros
    )


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    db = SessionLocal()

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existe = db.query(Usuario).filter(
            (Usuario.username == username) |
            (Usuario.email == email)
        ).first()

        if existe:
            flash("El usuario o correo ya existe.", "error")
            db.close()
            return redirect(url_for("register"))

        nuevo_usuario = Usuario(
            username=username,
            email=email,
            nombre=request.form["nombre"],
            club_id=request.form["club"],
            rol="user"
        )
        nuevo_usuario.set_password(password)

        db.add(nuevo_usuario)
        db.commit()
        db.close()

        flash("Usuario registrado correctamente.", "success")
        return redirect(url_for("login"))

    clubes = db.query(Club).all()
    db.close()
    return render_template("register.html", clubes=clubes)


# =========================
# LOGIN / LOGOUT
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    session.pop("_flashes", None)  # Limpia mensajes anteriores
    db = SessionLocal()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        usuario = db.query(Usuario).filter(
            Usuario.username == username
        ).first()

        if usuario and usuario.check_password(password):
            session["user_id"] = usuario.id
            session["username"] = usuario.username
            session["rol"] = usuario.rol  # 🔹 CLAVE PARA LOS ROLES

            db.close()
            flash("Sesión iniciada correctamente.", "success")
            return redirect(url_for("index"))

        flash("Usuario o contraseña incorrectos.", "error")
        db.close()
        return redirect(url_for("login"))

    db.close()
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("index"))

@app.route("/usuarios")
@admin_required
def usuarios():
    db = SessionLocal()
    usuarios = db.query(Usuario).all()
    db.close()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/usuarios/promover/<int:usuario_id>", methods=["POST"])
@admin_required
def promover_usuario(usuario_id):
    db = SessionLocal()
    usuario = db.query(Usuario).get(usuario_id)

    if usuario and usuario.rol != "admin":
        usuario.rol = "admin"
        db.commit()

    db.close()
    flash("Usuario promovido a admin.", "success")
    return redirect(url_for("usuarios"))

@app.route("/usuarios/degradar/<int:usuario_id>", methods=["POST"])
@admin_required
def degradar_usuario(usuario_id):
    # 🔒 No permitir auto-degradación
    if session.get("user_id") == usuario_id:
        flash("No puedes quitarte tu propio rol de administrador.", "error")
        return redirect(url_for("usuarios"))

    db = SessionLocal()
    usuario = db.query(Usuario).get(usuario_id)

    if usuario and usuario.rol == "admin":
        usuario.rol = "user"
        db.commit()
        flash("Administrador degradado a usuario.", "success")

    db.close()
    return redirect(url_for("usuarios"))

@app.route("/clubes/editar/<int:club_id>", methods=["GET", "POST"])
@admin_required
def editar_club(club_id):
    db = SessionLocal()
    club = db.query(Club).get(club_id)

    if not club:
        flash("Club no encontrado.", "error")
        db.close()
        return redirect(url_for("clubes"))

    if request.method == "POST":
        club.nombre = request.form["nombre"]
        club.descripcion = request.form["descripcion"]
        db.commit()
        db.close()
        flash("Club actualizado correctamente.", "success")
        return redirect(url_for("clubes"))

    db.close()
    return render_template("editar_club.html", club=club)

@app.route("/clubes/eliminar/<int:club_id>", methods=["POST"])
@admin_required
def eliminar_club(club_id):
    db = SessionLocal()
    club = db.query(Club).get(club_id)

    if not club:
        flash("Club no encontrado.", "error")
        db.close()
        return redirect(url_for("clubes"))

    usuarios_asignados = db.query(Usuario).filter(
        Usuario.club_id == club_id
    ).count()

    if usuarios_asignados > 0:
        flash("No se puede eliminar un club con usuarios asignados.", "error")
        db.close()
        return redirect(url_for("clubes"))

    db.delete(club)
    db.commit()
    db.close()

    flash("Club eliminado correctamente.", "success")
    return redirect(url_for("clubes"))

@app.route("/dashboard")
@login_required
@admin_required
def dashboard():
    db = SessionLocal()

    # ===== TARJETAS =====
    total_libros = db.query(Libro).count()
    total_usuarios = db.query(Usuario).count()

    prestamos_activos = db.query(Prestamo).filter(
        Prestamo.fecha_fin.is_(None)
    ).count()

    prestamos_cerrados = db.query(Prestamo).filter(
        Prestamo.fecha_fin.isnot(None)
    ).count()

    # ===== PRÉSTAMOS POR MES =====
    prestamos_por_mes = (
        db.query(
            func.date_trunc('month', Prestamo.fecha_inicio).label('mes'),
            func.count(Prestamo.id).label('total')
        )
        .group_by('mes')
        .order_by('mes')
        .all()
    )

    # Convertir a listas para JS
    meses = [p.mes.strftime("%Y-%m") for p in prestamos_por_mes]
    totales = [p.total for p in prestamos_por_mes]

    # ===== LIBROS MÁS PRESTADOS =====
    libros_mas_prestados = (
        db.query(
            Libro.titulo,
            func.count(Prestamo.id).label("total")
        )
        .join(Prestamo, Libro.id == Prestamo.libro_id)
        .group_by(Libro.titulo)
        .order_by(func.count(Prestamo.id).desc())
        .limit(5)
        .all()
    )

    titulos_libros = [l.titulo for l in libros_mas_prestados]
    totales_libros = [l.total for l in libros_mas_prestados]

    db.close()

    return render_template(
    "dashboard.html",
    total_libros=total_libros,
    total_usuarios=total_usuarios,
    prestamos_activos=prestamos_activos,
    prestamos_cerrados=prestamos_cerrados,
    meses=meses,
    totales=totales,
    titulos_libros=titulos_libros,
    totales_libros=totales_libros
)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(debug=True)
