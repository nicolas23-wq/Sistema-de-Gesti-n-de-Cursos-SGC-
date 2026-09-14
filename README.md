# Sistema de Gestión de Cursos

Prototipo funcional de un sistema de gestión de cursos académicos construido con **Python + Flask**, aplicando el patrón arquitectónico **MVC** y documentado siguiendo el **modelo de vistas 4+1**.

---

## Tabla de contenidos

1. [Instalación y ejecución](#1-instalación-y-ejecución)
2. [Credenciales de prueba](#2-credenciales-de-prueba)
3. [Arquitectura MVC](#3-arquitectura-mvc)
4. [Estructura del proyecto](#4-estructura-del-proyecto)
5. [Requisitos funcionales](#5-requisitos-funcionales)
6. [Requisitos no funcionales](#6-requisitos-no-funcionales)
7. [Modelo de vistas 4+1](#7-modelo-de-vistas-41)
8. [Justificación arquitectónica](#8-justificación-arquitectónica)
9. [Migración a PostgreSQL/MySQL](#9-migración-a-postgresqlmysql)
10. [Pruebas](#10-pruebas)

---

## 1. Instalación y ejecución

El proyecto corre dentro de un **entorno virtual (`venv`)** para aislar las dependencias del entorno global del sistema.

### 1.1 Crear el entorno virtual

```bash
python -m venv venv
```

### 1.2 Activarlo

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 1.3 Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 1.4 Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y ajusta los valores si es necesario:

```bash
copy .env.example .env     # Windows
cp .env.example .env       # macOS/Linux
```

El archivo `.env` contiene:

```
SECRET_KEY=clave-secreta-super-segura-para-desarrollo
SQLALCHEMY_DATABASE_URI=sqlite:///gestion_cursos.db
```

> **Importante:** el `.env` está en `.gitignore` y **no** debe subirse al repositorio. `SECRET_KEY` nunca debe estar hardcodeada en el código.

### 1.5 Ejecutar la aplicación

```bash
python run.py
```

Luego abre el navegador en `http://127.0.0.1:5000`.

> Al iniciar, `create_app()` llama a `seed_data(app)`: si la base de datos está vacía, crea automáticamente los usuarios de prueba, dos cursos y una inscripción. No requiere pasos manuales.

Los docentes y estudiantes adicionales de la institución se registran desde la sección **Usuarios** del panel del administrador (`/admin/usuarios`). El admin crea la cuenta con nombre, correo, contraseña y rol, y entrega las credenciales al usuario.

### 1.6 Desactivar el entorno

```bash
deactivate
```

### 1.7 Generar/actualizar `requirements.txt`

```bash
pip freeze > requirements.txt
```

---

## 2. Credenciales de prueba

| Rol | Email | Contraseña |
|-----|-------|------------|
| **Administrador** | `admin@correo.com` | `admin123` |
| **Docente** | `docente@correo.com` | `docente123` |
| **Estudiante** | `estudiante@correo.com` | `estudiante123` |

La contraseña se guarda hasheada con `werkzeug.security` (nunca en texto plano).

---

## 3. Arquitectura MVC

### 3.1 ¿Qué es MVC en este proyecto?

Flask es un microframework que no impone una estructura; aquí se implementa explícitamente **MVC** con responsabilidades claramente separadas en carpetas:

| Capa | Carpeta | Responsabilidad |
|------|---------|-----------------|
| **Modelo** | `app/models` | Entidades del dominio (Usuario, Curso, Inscripcion, Calificacion) declaradas con SQLAlchemy. Contienen las reglas de validación (unicidad, campos obligatorios), el hash de contraseñas y la comunicación con la base de datos. |
| **Vista** | `app/templates` | Plantillas Jinja2 (HTML + CSS + Bootstrap 5). Solo presentación: sin lógica de negocio ni acceso directo a datos. |
| **Controlador** | `app/controllers` | Blueprints Flask con funciones de vista que reciben la petición HTTP, validan la autorización por rol, invocan la capa Modelo/Services y seleccionan la Vista a renderizar. |
| **Services** *(auxiliar)* | `app/services` | Lógica de negocio compleja (inscripciones, calificaciones, autenticación) que no debe vivir en el Modelo ni en el Controlador, evitando "controladores gordos". |
| **Utils** | `app/utils` | Decoradores reutilizables como `@role_required()` y lógica transversal. |
| **Forms** | `app/forms` | Formularios Flask-WTF con validación y protección CSRF. |

### 3.2 Equivalencia con Flask

En Flask el término "view function" puede confundir. La equivalencia con MVC es:

- **Modelo** → clases en `app/models` (SQLAlchemy).
- **Vista** → plantillas Jinja2 en `app/templates`.
- **Controlador** → funciones de vista (view functions) dentro de los Blueprints de `app/controllers`.

### 3.3 Flujo de una petición

```
Usuario → [HTTP request] → Controlador (Blueprint)
                                │
                                ▼
                          Services (lógica)
                                │
                                ▼
                            Modelo (ORM)
                                │
                                ▼
                        Base de datos (SQLite)
                                │
                                ▼
                         Controlador (render)
                                │
                                ▼
Usuario ← [HTML renderizado] ← Vista (Jinja2)
```

### 3.4 ¿Por qué MVC mejora mantenibilidad, organización, escalabilidad y separación de responsabilidades?

- **Mantenibilidad:** cada cambio de negocio se localiza en una capa; los cambios visuales no afectan la lógica y viceversa.
- **Organización:** el código tiene un "mapa" claro: qué buscar y dónde (controladores, modelos, plantillas, formularios).
- **Escalabilidad:** la capa de servicios y el uso de ORM permiten cambiar de base de datos o crecer en funcionalidad sin reescribir la lógica de negocio.
- **Separación de responsabilidades:** la vista nunca consulta la BD, el controlador no contiene HTML y el modelo no maneja peticiones HTTP. Se respeta el principio de responsabilidad única.

---

## 4. Estructura del proyecto

```
gestion_cursos/
├── venv/                          # Entorno virtual (NO se sube al repo)
├── .env                           # Variables de entorno (NO se sube al repo)
├── .env.example                   # Plantilla de variables de entorno
├── .gitignore
├── config.py                      # Configuración de Flask y SQLAlchemy
├── run.py                         # Punto de entrada: python run.py
├── requirements.txt               # Dependencias con versiones fijas
├── README.md
├── app/
│   ├── __init__.py                # [FACTORY] create_app() + seed_data() automático
│   ├── controllers/               # [CONTROLADOR] Blueprints
│   │   ├── __init__.py
│   │   ├── auth.py                # Login y logout (/login, /logout)
│   │   ├── admin.py               # Dashboard, cursos, inscripciones
│   │   ├── docente.py             # Dashboard, cursos, calificaciones
│   │   └── estudiante.py          # Dashboard, cursos, calificaciones
│   ├── models/                    # [MODELO] Entidades ORM
│   │   ├── __init__.py
│   │   ├── usuario.py             # Usuario (con set_password/check_password)
│   │   ├── curso.py               # Curso
│   │   ├── inscripcion.py         # Inscripcion (N:M Usuario ↔ Curso)
│   │   └── calificacion.py        # Calificacion
│   ├── forms/                     # Formularios Flask-WTF (CSRF incluido)
│   │   ├── __init__.py
│   │   ├── auth_forms.py          # LoginForm
│   │   ├── admin_forms.py         # CrearCursoForm, InscribirEstudianteForm, CrearUsuarioForm
│   │   └── docente_forms.py       # CalificacionForm
│   ├── services/                  # Lógica de negocio auxiliar
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Autenticación, obtención de docentes/estudiantes
│   │   └── curso_service.py       # Cursos, inscripciones, calificaciones
│   ├── utils/
│   │   ├── __init__.py
│   │   └── decorators.py          # @role_required(*roles)
│   ├── templates/                 # [VISTA] Plantillas Jinja2
│   │   ├── base.html              # Layout con Bootstrap 5 y acento por rol
│   │   ├── login.html
│   │   ├── errores/
│   │   │   ├── 403.html
│   │   │   └── 404.html
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── usuarios.html
│   │   │   ├── crear_usuario.html
│   │   │   ├── cursos.html
│   │   │   ├── crear_curso.html
│   │   │   └── inscribir.html
│   │   ├── docente/
│   │   │   ├── dashboard.html
│   │   │   ├── mis_cursos.html
│   │   │   └── calificar.html
│   │   └── estudiante/
│   │       ├── dashboard.html
│   │       ├── mis_cursos.html
│   │       └── mis_calificaciones.html
│   └── static/
│       └── css/
│           └── style.css          # Variables de color por rol
└── tests/
    ├── __init__.py
    ├── conftest.py                # Fixtures de pytest con BD en memoria
    ├── test_auth.py               # RF1 y RF2
    ├── test_models.py             # Modelos y hashing
    ├── test_admin.py              # RF3
    ├── test_docente.py            # RF4
    └── test_estudiante.py         # RF5
```

### Color de acento por rol

Tema claro y neutro (Bootstrap 5) con un color de acento distinto según el rol, visible en el navbar y el badge de rol:

| Rol | Color | Badge |
|-----|-------|-------|
| Administrador | `#0d6efd` (azul) | `bg-primary` |
| Docente | `#198754` (verde) | `bg-success` |
| Estudiante | `#6f42c1` (púrpura) | `bg-secondary` |

---

## 5. Requisitos funcionales

| RF | Descripción | Rol | Estado |
|----|-------------|-----|--------|
| **RF1** | Inicio de sesión con usuario/contraseña (Flask-WTF + CSRF, hashing). | Todos | ✅ |
| **RF2** | Control de acceso por roles con `@role_required()` y redirección al dashboard de cada rol. Logout. | Todos | ✅ |
| **RF3** | Gestionar usuarios (docentes/estudiantes) de la institución, crear curso, consultar listado, inscribir estudiantes. | Administrador | ✅ |
| **RF4** | Consultar sus cursos, consultar estudiantes inscritos, registrar/actualizar calificaciones. | Docente | ✅ |
| **RF5** | Iniciar sesión, consultar cursos inscritos y calificaciones por curso. | Estudiante | ✅ |

**RF1 – Inicio de sesión**
- Pantalla de login en `/login` con `LoginForm` (Flask-WTF, protección CSRF).
- Usuarios predefinidos creados por el seed automático.
- Contraseñas hasheadas con `werkzeug.security.generate_password_hash`.

**RF2 – Control de acceso por roles**
- `Flask-Login` gestiona la sesión; `@login_required` protege los dashboards.
- `@role_required("admin")` (en `app/utils/decorators.py`) valida el rol y centraliza el control (no se repite manualmente en cada ruta).
- Tras el login se redirige a: `/admin/`, `/docente/` o `/estudiante/`.
- Ruta `/logout` cierra la sesión con `logout_user()`.

**RF3 – Gestión de cursos (Admin)**
- `GET /admin/usuarios` → listado de docentes y estudiantes de la institución (el registro de usuarios lo controla el admin).
- `POST /admin/usuarios/crear` → registra un docente o estudiante de la institución con su contraseña hasheada.
- `POST /admin/cursos/crear` → crea curso asignando un docente.
- `GET /admin/cursos` → listado de cursos con estudiantes inscritos.
- `POST /admin/inscribir` → registra un estudiante en un curso (evita duplicados).

**RF4 – Registro de calificaciones (Docente)**
- `GET /docente/mis-cursos` → cursos asignados con estudiantes inscritos.
- `POST /docente/calificar` → registra o actualiza la nota (0–20) de un estudiante en un curso.

**RF5 – Consulta del estudiante**
- `GET /estudiante/mis-cursos` → cursos inscritos.
- `GET /estudiante/mis-calificaciones` → calificaciones por curso con promedio.

---

## 6. Requisitos no funcionales

| RNF | Implementación |
|-----|----------------|
| **Seguridad** | Contraseñas hasheadas (`werkzeug.security`), protección de rutas por rol (`@role_required`), CSRF en todos los formularios (Flask-WTF), `SECRET_KEY` y URI de BD vía variables de entorno (`.env` + `python-dotenv`, nunca hardcodeadas). |
| **Mantenibilidad** | Separación estricta Modelo/Vista/Controlador, capa `services`, nombres claros y código comentado. |
| **Escalabilidad** | Acceso a datos vía ORM (SQLAlchemy); la capa `services` abstrae la lógica de negocio de la base de datos, permitiendo migrar a PostgreSQL/MySQL sin reescribir el negocio. |
| **Usabilidad** | Bootstrap 5 vía CDN, tema claro/neutro con acento por rol, mensajes flash de error/éxito claros. |
| **Rendimiento** | Relaciones con `lazy="joined"` (SQLAlchemy) para evitar consultas N+1 al listar cursos con sus inscripciones. |
| **Portabilidad** | `requirements.txt` con versiones fijas e instrucciones multiplataforma dentro de un `venv`. |
| **Disponibilidad de datos de prueba** | `seed_data()` dentro de `create_app()` crea usuarios/cursos de ejemplo solo si la BD está vacía (no duplica). |
| **Manejo de errores** | Handlers personalizados para 403 y 404 con plantillas en `templates/errores/`. |

### Sobre el patrón Repository / abstracción de acceso a datos

Para escalabilidad no se reescribe la lógica de negocio al cambiar de motor: `services/` actúa como punto único de acceso a datos. Si se desea un patrón Repository formal, bastaría con crear clases en `services/` que encapsulen las consultas (por ejemplo `CursoRepository.listar()`) y que los controladores dependan de esa interfaz, sin tocar las plantillas ni los formularios.

---

## 7. Modelo de vistas 4+1

### 7.1 Vista lógica (clases/entidades)

```mermaid
erDiagram
    USUARIO ||--o{ CURSO : "imparte (docente_id)"
    USUARIO ||--o{ INSCRIPCION : "se inscribe (estudiante)"
    USUARIO ||--o{ CALIFICACION : "recibe (estudiante)"
    CURSO ||--o{ INSCRIPCION : "tiene"
    CURSO ||--o{ CALIFICACION : "tiene"

    USUARIO {
        int id PK
        string nombre
        string email UK
        string password_hash
        string rol "admin|docente|estudiante"
    }
    CURSO {
        int id PK
        string nombre
        text descripcion
        int docente_id FK
    }
    INSCRIPCION {
        int id PK
        int estudiante_id FK
        int curso_id FK
    }
    CALIFICACION {
        int id PK
        int estudiante_id FK
        int curso_id FK
        float nota
        datetime fecha
    }
```

> El modelo `Estudiante` y `Docente` se representan a través de la entidad `Usuario` (campo `rol`), de acuerdo con la estructura de modelos indicada (`usuario.py, curso.py, inscripcion.py, calificacion.py`). La relación muchos a muchos Usuario–Curso se materializa con la tabla asociación `inscripciones`.

### 7.2 Vista de desarrollo (el árbol de carpetas)

Ver [sección 4 – Estructura del proyecto](#4-estructura-del-proyecto). La correspondencia es:

- **`app/models`** → **Modelo**
- **`app/templates`** → **Vista**
- **`app/controllers`** → **Controlador**
- **`app/services`, `app/forms`, `app/utils`** → capas de apoyo

```
GESTION_CURSOS
│   run.py ── inicia Flask
└── app
    ├── controllers (Controlador: Blueprints por rol)
    ├── models      (Modelo: entidades SQLAlchemy)
    ├── services    (lógica de negocio)
    ├── forms       (Flask-WTF)
    ├── utils       (decoradores, control de acceso)
    ├── templates   (Vista: Jinja2)
    └── static      (CSS)
```

### 7.3 Vista de procesos (autenticación)

```mermaid
flowchart TD
    A[Usuario] --> B[Envía credenciales al login]
    B --> C{Validar datos del formulario}<br>Flask-WTF + CSRF
    C -- no válido --> D[Muestra errores]
    C -- válido --> E{Verificar email y<br>contraseña hasheada}
    E -- inválido --> F[Flash: Credenciales invalidas]
    E -- válido --> G[login_user + identificar rol]
    G --> H{Rol del usuario}
    H -- admin --> I[Dashboard admin /admin/]
    H -- docente --> J[Dashboard docente /docente/]
    H -- estudiante --> K[Dashboard estudiante /estudiante/]
    I --> L[Acceso al sistema]
    J --> L
    K --> L
```

### 7.4 Vista física

```mermaid
flowchart LR
    subgraph Local[Computador del usuario]
        N[Navegador]
    end
    N -->|HTTP| W[Servidor web dev<br>Flask 127.0.0.1:5000]
    W --> A[Aplicacion Flask<br>MVC]
    A --> DB[(Base de datos<br>SQLite: gestion_cursos.db)]
```

**Escalado proyectado (producción):**

```mermaid
flowchart LR
    U[Usuarios] --> LB[Balanceador de carga]
    LB --> NG[Nginx]
    NG --> G1[Gunicorn - Flask app 1]
    NG --> G2[Gunicorn - Flask app 2]
    G1 --> R[(Redis cache)]
    G2 --> R
    G1 --> PG[(PostgreSQL)]
    G2 --> PG
```

Para 10.000 usuarios la aplicación pasaría de SQLite a un motor robusto y se desplegaría con Gunicorn + Nginx, caché con Redis, balanceo de carga y contenedores Docker.

### 7.5 Escenarios (2 casos de uso)

**Escenario 1: Un administrador registra usuarios, crea un curso y matricula a un estudiante**

1. El administrador inicia sesión con `admin@correo.com`.
2. En **"Usuarios"** → **"Nuevo usuario"** registra un docente (nombre, correo, contraseña, rol "docente"). El servicio `auth_service.crear_usuario()` valida unicidad del correo y crea la cuenta hasheada.
3. Registra un estudiante de la misma forma.
4. Desde el dashboard hace clic en **"Crear curso"**, completa nombre, descripción y selecciona al docente registrado. El servicio `curso_service.crear_curso()` persiste en la BD y redirige al listado.
5. En **"Inscribir estudiante"**, elige curso y estudiante; `curso_service.inscribir_estudiante()` valida que no esté ya inscrito y registra la inscripción.
6. El estudiante inscrito puede iniciar sesión y ver el curso en **"Mis cursos"**.

**Escenario 2: Un docente registra la calificación de un estudiante y este la consulta**

1. El docente inicia sesión con `docente@correo.com`.
2. En **"Calificar"** selecciona uno de sus cursos asignados; el formulario carga automáticamente los estudiantes inscritos.
3. Ingresa la nota (0–20); `curso_service.registrar_calificacion()` crea la calificación o la actualiza si ya existía (upsert).
4. El estudiante inicia sesión con `estudiante@correo.com`, entra en **"Mis calificaciones"** y ve la nota por curso, junto con el promedio en su dashboard.

---

## 8. Justificación arquitectónica

### 8.1 ¿Qué arquitectura se implementó?

MVC (Modelo–Vista–Controlador), con capa auxiliar de **Services** para mantener controladores y modelos delgados.

### 8.2 ¿Qué componentes principales tiene?

- **Modelo** (`app/models`): `Usuario`, `Curso`, `Inscripcion`, `Calificacion` con SQLAlchemy.
- **Vista** (`app/templates`): plantillas Jinja2 + Bootstrap 5.
- **Controlador** (`app/controllers`): Blueprints `auth`, `admin`, `docente`, `estudiante`.
- **Services** (`app/services`): `auth_service` y `curso_service` con la lógica de negocio.
- Además: `forms` (Flask-WTF), `utils` (decorador `@role_required`).

### 8.3 ¿Cómo se separó la presentación de la lógica de negocio?

- Las plantillas **solo** renderizan variables y recorren estructuras que reciben del controlador; **nunca** hacen consultas ni lógica de negocio.
- El controlador orquesta: valida formulario → consulta `services` → pasa datos a la plantilla.
- La lógica de negocio vive en `services`/`models`; el HTML en `templates`; el CSS en `static`.

### 8.4 ¿Cómo se comunica el Controlador con el Modelo, y este con la base de datos?

El controlador invoca funciones de `services` (por ejemplo `curso_service.listar_cursos()`). Las services usan el ORM SQLAlchemy (`db.session`, `Model.query`, `db.session.get(...)`), que traduce las operaciones a SQL sobre SQLite. El modelo `Usuario` también encapsula el hash de contraseñas con `set_password()` / `check_password()`.

### 8.5 ¿Qué ventaja tiene MVC frente a todo el código en un único archivo?

Si todo (rutas, consultas SQL y HTML) estuviera en un solo archivo: el código sería imposible de mantener, cualquier cambio en HTML o SQL rompería otras funciones, el control de acceso quedaría disperso y repetido, y el proyecto no escalaría ni permitiría trabajo en equipo. MVC divide esas responsabilidades, reduce el acoplamiento y permite cambiar, probar y extender cada capa de manera independiente.

### 8.6 Si el sistema tuviera 10.000 usuarios, ¿qué cambiaría?

1. **Motor de base de datos**: migrar de SQLite a **PostgreSQL** (ver sección 9).
2. **Servidor WSGI**: reemplazar el dev server de Flask por **Gunicorn** (o uWSGI) detrás de **Nginx**.
3. **Caché**: añadir **Redis** para sesiones, consultas frecuentes y throttling.
4. **Balanceo de carga**: múltiples réplicas de la app detrás de un balanceador, con caché compartida.
5. **Contenedores**: empacar la app en **Docker** y orquestar con Docker Compose/Kubernetes.
6. **API REST + frontend desacoplado**: exponer una API REST (p. ej. con Flask-RESTX o separar en microservicios por dominio: usuarios, cursos, calificaciones) y consumirla desde un SPA (React/Vue), desacoplando el frontend del backend Flask.
7. **Observabilidad**: logging centralizado, métricas (Prometheus) y monitoreo.

---

## 9. Migración a PostgreSQL/MySQL

La capa de negocio no cambia porque se accede a datos vía SQLAlchemy. Solo se modifica la cadena de conexión en `.env`:

```env
SQLALCHEMY_DATABASE_URI=postgresql://usuario:password@localhost/gestion_cursos
# o MySQL
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:password@localhost/gestion_cursos
```

Se instala el driver correspondiente (`psycopg2-binary` o `pymysql`). Para esquemas versionables conviene incorporar **Alembic/Flask-Migrate** en lugar de `db.create_all()`.

---

## 10. Pruebas

La suite de pruebas usa **pytest** con una base de datos SQLite en memoria, totalmente aislada de la de desarrollo.

```bash
python -m pytest tests -v
```

Resultado esperado: **17 tests, todos en verde**. Cobertura por requisito funcional:

| Archivo | RF cubierto |
|---------|-------------|
| `tests/test_auth.py` | RF1 (login/logout) y RF2 (rutas protegidas) |
| `tests/test_models.py` | Hashing y modelos |
| `tests/test_admin.py` | RF3 (crear/listar cursos, inscribir, denegación) |
| `tests/test_docente.py` | RF4 (ver cursos, registrar calificación, denegación) |
| `tests/test_estudiante.py` | RF5 (ver cursos/calificaciones, denegación) |

---

## Notas finales

- Los datos de prueba se crean automáticamente al iniciar la app (seed en `create_app()`), solo si la BD está vacía.
- La carpeta `venv/`, `__pycache__/`, `*.pyc`, `*.db` y `.env` están excluidas del repositorio mediante `.gitignore`.
- El proyecto se ejecuta con `python run.py` o `flask run` (con el entorno virtual activado).