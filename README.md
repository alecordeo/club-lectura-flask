📚 Club de Lectura – Sistema de Gestión

Sistema web para la administración de un Club de Lectura, que permite gestionar usuarios, roles, clubes, libros, préstamos y reseñas, además de contar con un dashboard administrativo con estadísticas visuales.

Proyecto desarrollado con Flask + PostgreSQL, siguiendo principios de normalización (3FN) y buenas prácticas de desarrollo web.

🚀 Funcionalidades principales
👤 Usuarios

Registro e inicio de sesión

Roles:

Admin

User

Gestión de roles (asignar / quitar administrador)

Asociación de usuarios a clubes

🏛️ Clubes (solo Admin)

Crear clubes

Editar información de clubes

Eliminar clubes

Asignar usuarios a clubes

📚 Libros

Registrar libros

Listar libros disponibles

Información de autor, editorial y año

🔁 Préstamos

Registrar préstamos

Validación de disponibilidad de libros

Cierre de préstamos

Historial de préstamos

✍️ Reseñas

Crear reseñas de libros

Calificación (1 a 5)

Comentarios asociados a usuarios y libros

📊 Dashboard (Admin)

Total de libros

Total de usuarios

Préstamos activos y cerrados

Gráficas con Chart.js

Estado de préstamos

Préstamos por mes

Libros más prestados

🛠️ Tecnologías utilizadas

Backend: Flask (Python)

ORM: SQLAlchemy

Base de datos: PostgreSQL

Frontend: HTML, CSS, JavaScript

Gráficas: Chart.js

Autenticación: Sesiones de Flask

Despliegue: Render

Control de versiones: Git + GitHub

🗂️ Estructura del proyecto
club-lectura/
│
├── app.py                 # Rutas y lógica principal
├── models.py              # Modelos ORM
├── database.py            # Conexión a la base de datos
├── database.sql           # Script SQL (estructura + datos)
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── libros.html
│   ├── prestamos.html
│   ├── resenas.html
│   └── clubes.html
│
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   └── index.css
│   └── images/
│
├── requirements.txt
├── README.md
└── .gitignore

🧱 Base de datos y Normalización

La base de datos está diseñada siguiendo Tercera Forma Normal (3FN):

Cada tabla representa una sola entidad

No existen dependencias parciales

No hay dependencias transitivas

Relaciones mediante claves foráneas

Tablas principales:

usuarios

clubes

libros

prestamos

resenas

📄 El archivo database.sql contiene:

Creación completa de tablas

Llaves primarias y foráneas

Restricciones

Datos de prueba

⚙️ Configuración local
1️⃣ Clonar el repositorio
git clone https://github.com/tu-usuario/club-lectura.git
cd club-lectura

2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Configurar base de datos

Crear una base de datos PostgreSQL

Ajustar variables de entorno o DATABASE_URL

5️⃣ Ejecutar la aplicación
flask run

🌐 Despliegue en Render

El proyecto está preparado para ser desplegado en Render:

Base de datos PostgreSQL gestionada por Render

Variables de entorno para conexión segura

Inicialización automática de la app

📌 Notas finales

El rol Admin controla las secciones críticas del sistema

El sistema es escalable (ej. fotos de perfil, notificaciones, API)

Proyecto diseñado con enfoque académico y práctico

✍️ Autor

Proyecto académico – Club de Lectura
Desarrollado como sistema de gestión con enfoque en bases de datos y desarrollo web.
