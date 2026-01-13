📚 Club de Lectura – Sistema de Gestión

Sistema web para la administración de un Club de Lectura, que permite gestionar usuarios, roles, clubes, libros, préstamos y reseñas, además de contar con un dashboard administrativo con estadísticas visuales.

Proyecto desarrollado con Flask + PostgreSQL, siguiendo principios de normalización (3FN) y buenas prácticas de desarrollo web.

🚀 Funcionalidades principales
👤 Usuarios

Registro e inicio de sesión

Gestión de roles:

Admin

User

Asignación y revocación de permisos de administrador

Asociación de usuarios a clubes de lectura

🏛️ Clubes (solo Admin)

Crear clubes

Editar información de clubes

Eliminar clubes

Asignar usuarios a clubes

📚 Libros

Registro de libros

Listado de libros disponibles

Información de autor, editorial y año

🔁 Préstamos

Registro de préstamos

Validación de disponibilidad de libros

Cierre de préstamos

Historial completo de préstamos

✍️ Reseñas

Creación de reseñas de libros

Calificación de 1 a 5 estrellas

Comentarios asociados a usuarios y libros

📊 Dashboard (Admin)

Total de libros

Total de usuarios

Préstamos activos y cerrados

Visualización de datos con Chart.js:

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

La base de datos está diseñada siguiendo la Tercera Forma Normal (3FN):

Cada tabla representa una sola entidad

No existen dependencias parciales

No hay dependencias transitivas

Relaciones implementadas mediante claves foráneas

Tablas principales

usuarios

clubes

libros

prestamos

resenas

📄 Archivo database.sql

Incluye:

Creación completa de tablas

Llaves primarias y foráneas

Restricciones de integridad

Datos de prueba

⚙️ Configuración local
1️⃣ Clonar el repositorio
git clone https://github.com/tu-usuario/club-lectura.git
cd club-lectura

2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Configurar base de datos

Crear una base de datos en PostgreSQL

Configurar las variables de entorno o DATABASE_URL

5️⃣ Ejecutar la aplicación
flask run

🌐 Despliegue en Render

El proyecto está preparado para ser desplegado en Render:

Base de datos PostgreSQL gestionada por Render

Variables de entorno para conexión segura

Inicialización automática de la aplicación

📌 Notas finales

El rol Admin controla las secciones críticas del sistema

El sistema es escalable (ej. fotos de perfil, notificaciones, API REST)

Proyecto diseñado con enfoque académico y práctico

Documentación
<img width="921" height="416" alt="image" src="https://github.com/user-attachments/assets/edb2fe17-7145-4652-9374-72ad9c8793ce" />
<img width="921" height="550" alt="image" src="https://github.com/user-attachments/assets/c3368148-e7b9-4e6a-83fc-9313c713474d" />


✍️ Autor

Proyecto académico – Club de Lectura
Desarrollado como sistema de gestión con enfoque en bases de datos y desarrollo web.
