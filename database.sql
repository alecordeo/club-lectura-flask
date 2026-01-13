-- =========================================
-- BASE DE DATOS: CLUB DE LECTURA
-- PostgreSQL
-- =========================================

-- =========================
-- TABLA: clubes
-- =========================
CREATE TABLE clubes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- =========================
-- TABLA: usuarios
-- =========================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'user',
    nombre VARCHAR(100),
    club_id INTEGER,
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_club
        FOREIGN KEY (club_id)
        REFERENCES clubes(id)
        ON DELETE SET NULL
);

-- =========================
-- TABLA: libros
-- =========================
CREATE TABLE libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(100),
    editorial VARCHAR(100),
    anio_publicacion INTEGER
);

-- =========================
-- TABLA: prestamos
-- =========================
CREATE TABLE prestamos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    libro_id INTEGER NOT NULL,
    fecha_inicio DATE DEFAULT CURRENT_DATE,
    fecha_fin DATE,
    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_libro
        FOREIGN KEY (libro_id)
        REFERENCES libros(id)
        ON DELETE CASCADE
);

-- =========================
-- TABLA: resenas
-- =========================
CREATE TABLE resenas (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    libro_id INTEGER NOT NULL,
    calificacion INTEGER NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
    comentario TEXT,
    fecha DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_usuario_resena
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_libro_resena
        FOREIGN KEY (libro_id)
        REFERENCES libros(id)
        ON DELETE CASCADE
);

-- =========================================
-- DATOS DE PRUEBA
-- =========================================

-- CLUBES
INSERT INTO clubes (nombre, descripcion) VALUES
('Clásicos Universales', 'Lectura de obras clásicas'),
('Literatura Latinoamericana', 'Autores latinoamericanos'),
('Filosofía y Pensamiento', 'Ensayos y reflexión');

-- USUARIOS (password_hash es simbólico para el profesor)
INSERT INTO usuarios (username, email, password_hash, rol, nombre, club_id) VALUES
('admin1', 'admin1@mail.com', 'HASHED_PASSWORD', 'admin', 'Administrador Uno', 1),
('admin2', 'admin2@mail.com', 'HASHED_PASSWORD', 'admin', 'Administrador Dos', 2),

('lector01', 'lector01@mail.com', 'HASHED_PASSWORD', 'user', 'Juan Pérez', 1),
('lector02', 'lector02@mail.com', 'HASHED_PASSWORD', 'user', 'Ana López', 2),
('lector03', 'lector03@mail.com', 'HASHED_PASSWORD', 'user', 'Carlos Ruiz', 3),
('lector04', 'lector04@mail.com', 'HASHED_PASSWORD', 'user', 'María Gómez', 1),
('lector05', 'lector05@mail.com', 'HASHED_PASSWORD', 'user', 'Luis Fernández', 2);

-- LIBROS
INSERT INTO libros (titulo, autor, editorial, anio_publicacion) VALUES
('La ciudad y los perros', 'Mario Vargas Llosa', 'Seix Barral', 1963),
('Conversación en La Catedral', 'Mario Vargas Llosa', 'Seix Barral', 1969),
('Crimen y castigo', 'Fiódor Dostoyevski', 'Alianza', 1866),
('Los hermanos Karamázov', 'Fiódor Dostoyevski', 'Alianza', 1880),
('Cien años de soledad', 'Gabriel García Márquez', 'Sudamericana', 1967),
('El amor en los tiempos del cólera', 'Gabriel García Márquez', 'Oveja Negra', 1985),
('Rayuela', 'Julio Cortázar', 'Sudamericana', 1963),
('1984', 'George Orwell', 'Secker & Warburg', 1949),
('El extranjero', 'Albert Camus', 'Gallimard', 1942);

-- PRÉSTAMOS
INSERT INTO prestamos (usuario_id, libro_id) VALUES
(3, 1),
(4, 3),
(5, 5);

-- RESEÑAS
INSERT INTO resenas (usuario_id, libro_id, calificacion, comentario) VALUES
(3, 1, 5, 'Una obra impactante'),
(4, 3, 4, 'Lectura intensa'),
(5, 5, 5, 'Obra maestra');
