# 📋 Gestor de Tareas

Sistema completo de gestión de tareas con autenticación, roles de usuario e interfaz web con FastAPI + Jinja2.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-38%20passing-brightgreen.svg)](test/test_schemas.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📑 Tabla de Contenidos

- [Descripción](#-descripción)
- [Estado del Proyecto](#-estado-del-proyecto)
- [Características](#-características)
- [Arquitectura](#️-arquitectura)
- [Tecnologías](#️-tecnologías)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Testing](#-testing)
- [Roadmap](#️-roadmap)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribución](#-contribución)

---

## 🎯 Descripción

Sistema de gestión de tareas con tres niveles de usuarios (**user**, **supervisor**, **admin**), autenticación segura con bcrypt, y persistencia de datos. Incluye interfaz de consola CLI y próximamente interfaz web con FastAPI + Jinja2.

### Casos de Uso

- **Usuarios comunes** (`user`): Ver tareas asignadas, agregar comentarios
- **Supervisores** (`supervisor`): Crear tareas, asignar a usuarios comunes
- **Administradores** (`admin`): Control total del sistema, gestión de usuarios y tareas

---

## 🚦 Estado del Proyecto

### ✅ Completado

| Componente | Estado | Descripción |
|------------|--------|-------------|
| **Core - Modelo de Datos** | ✅ 100% | Clases `Usuario`, `Tarea`, `GestorTareas` |
| **Core - Autenticación** | ✅ 100% | bcrypt, roles, permisos |
| **Core - Persistencia** | ✅ 100% | pickle para usuarios/tareas, JSON para histórico |
| **API - Schemas Pydantic** | ✅ 100% | 10 schemas con validación completa |
| **Tests - Schemas** | ✅ 100% | 38 tests pasando, coverage completo |
| **CLI - Interfaz Consola** | ✅ 100% | Menú interactivo funcional |
| **Documentación - Docstrings** | ✅ 100% | Estilo Google en todos los módulos |

### 🚧 En Progreso

| Componente | Estado | Prioridad |
|------------|--------|-----------|
| **Tests - Core** | ⏳ 0% | Alta |

### 📋 Pendiente

| Componente | Estado | Prioridad |
|------------|--------|-----------|
| **FastAPI + Jinja2** | ❌ | Alta |
| **Templates HTML** | ❌ | Alta |
| **CSS/JavaScript** | ❌ | Media |
| **Tests de API** | ❌ | Alta |
| **Deploy** | ❌ | Baja |

---

## ✨ Características

### Core ✅

- ✅ **Gestión de usuarios** con 3 roles (user, supervisor, admin)
- ✅ **Autenticación segura** con bcrypt (hashing + salt)
- ✅ **Sistema de tareas** con estados (pendiente, finalizada)
- ✅ **Asignación múltiple** de usuarios a tareas
- ✅ **Comentarios** en tareas (solo usuarios asignados)
- ✅ **Persistencia** con pickle (usuarios/tareas) y JSON (histórico)
- ✅ **Validación de permisos** por rol
- ✅ **Estadísticas** de tareas y usuarios
- ✅ **Histórico** de tareas finalizadas

### API/Schemas ✅

- ✅ **14 Schemas Pydantic** con validación automática
- ✅ **Validación de tipos** y valores (ge=0, Literal, etc.)
- ✅ **Documentación automática** con docstrings estilo Google
- ✅ **38 tests unitarios** con 100% de cobertura de schemas

### Web 📋 (Pendiente)

- ⏳ Interfaz web con FastAPI + Jinja2
- ⏳ Templates HTML responsivos
- ⏳ Autenticación basada en sesiones/cookies
- ⏳ Dashboard con estadísticas
- ⏳ CRUD completo de tareas y usuarios
- ⏳ Panel de administración

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│   Interfaz (CLI ✅ / Web 📋)            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   API Layer (Schemas Pydantic ✅)       │
│   - Validación de entrada/salida        │
│   - Serialización automática            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Core Business Logic ✅                │
│   - GestorTareas (orquestador)          │
│   - Usuario (autenticación, roles)      │
│   - Tarea (estado, comentarios)         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Persistencia ✅                       │
│   - Pickle: usuarios.dat, tareas.dat    │
│   - JSON: tareas_finalizadas.json       │
└─────────────────────────────────────────┘
```

### Flujo de Datos

```
Usuario → CLI/Web → Schemas (validación) → GestorTareas → Modelos (Usuario/Tarea) → Persistencia
```

---

## 🛠️ Tecnologías

### Backend Core ✅

- **Python 3.10+**: Type hints, pattern matching
- **bcrypt 4.0+**: Hashing seguro de contraseñas (Blowfish)
- **pickle**: Serialización de objetos Python
- **json**: Histórico de tareas en formato legible

### API y Validación ✅

- **Pydantic 2.0+**: Validación de datos, serialización, type coercion

### Web 📋 (Próximamente)

- **FastAPI**: Framework web asíncrono de alto rendimiento
- **Jinja2**: Motor de plantillas HTML
- **Uvicorn**: Servidor ASGI
- **itsdangerous**: Cookies seguras para sesiones

### Testing ✅

- **pytest 7.0+**: Framework de testing
- **httpx** 📋: Cliente HTTP para tests de API

---

## 📦 Instalación

### Requisitos Previos

- **Python 3.8 o superior**
- **uv** (gestor de paquetes ultrarrápido) - [Instalación](https://docs.astral.sh/uv/getting-started/installation/) (Recomendado)
- **pip** (gestor de paquetes de Python) - [Instalación](https://pip.pypa.io/en/stable/installation/) (Recomendado)

### Instalación de uv

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalación
uv --version
```

---

### 🚀 Método 1: Instalación con uv (Recomendado)

#### Opción A: Usando pyproject.toml (Proyecto ya inicializado)

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/gestortareas.git
cd gestortareas

# 2. Sincronizar dependencias (crea .venv automáticamente)
uv sync

# 3. Activar entorno virtual
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 4. Ejecutar tests
uv run pytest test/test_schemas.py -v
```

#### Opción B: Seleccionar versión específica de Python

```bash
# Ver versiones de Python disponibles
uv python list

# Instalar una versión específica (ejemplo: Python 3.11)
uv python install 3.11

# Crear proyecto con Python 3.11
uv venv --python 3.11

# Sincronizar dependencias
uv sync

# Activar entorno
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

#### Opción C: Migrar desde requirements.txt a pyproject.toml

Si tienes un `requirements.txt` y quieres migrar a `uv`:

```bash
# 1. Inicializar proyecto uv
uv init .

# 2. Agregar dependencias desde requirements.txt
uv add pydantic bcrypt rich

# 3. Agregar dependencias de desarrollo
uv add --dev pytest

# 4. Sincronizar (instala todo y genera uv.lock)
uv sync

# 5. (Opcional) Eliminar requirements.txt antiguo
# rm requirements.txt
```

**Dependencias instaladas:**
```toml
[project.dependencies]
pydantic>=2.0.0      # Validación de datos
bcrypt>=4.0.0        # Hashing de passwords
rich>=13.0.0         # Interfaz de consola

[project.optional-dependencies.dev]
pytest>=7.0.0        # Testing
```

#### Verificar instalación

```bash
# Verificar dependencias (sin activar entorno)
uv run python -c "import pydantic, bcrypt, pytest, rich; print('✅ Instalación correcta')"

# Ejecutar tests
uv run pytest test/test_schemas.py -v

# O con entorno activado
pytest test/test_schemas.py -v
```

---

### 🐍 Método 2: Instalación tradicional con pip

Si prefieres usar `pip` en lugar de `uv`:

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/gestortareas.git
cd gestortareas

# 2. Crear entorno virtual
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar tests
pytest test/test_schemas.py -v
```

---

### 🌐 Instalación Completa con Dependencias Web (Futuro)

Para instalar todas las dependencias incluidas las de desarrollo web:

```bash
# Con uv
uv sync --extra web

# Con pip (descomentar líneas en requirements.txt)
pip install fastapi uvicorn[standard] jinja2 python-multipart itsdangerous httpx
```

---

## 🚀 Uso

### Interfaz de Consola (CLI) ✅

```bash
python main.py
```

**Funcionalidades del menú:**
- Login de usuarios
- Crear tareas (admin/supervisor)
- Asignar tareas a usuarios
- Ver tareas asignadas
- Agregar comentarios
- Cambiar estado de tareas
- Ver estadísticas
- Gestión de usuarios (admin)

**Usuario administrador por defecto:**

Si no existen usuarios, se crea automáticamente:
- **Usuario:** `admin`
- **Contraseña:** Se genera aleatoriamente y se muestra en consola

### Interfaz Web (Futuro) 📋

```bash
# Iniciar servidor (cuando esté implementado)
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

**Rutas planificadas:**
- `http://localhost:8000` → Página principal
- `http://localhost:8000/login` → Login
- `http://localhost:8000/dashboard` → Dashboard
- `http://localhost:8000/docs` → Documentación automática de API

---

## 🧪 Testing

### Tests Actuales ✅

**Schemas Pydantic: 38/38 tests pasando** ✅

```bash
# Ejecutar todos los tests de schemas
pytest test/test_schemas.py -v

# Output esperado:
# ========== 38 passed in 0.37s ==========
```

**Cobertura de tests:**

| Schema | Tests | Estado |
|--------|-------|--------|
| UsuarioCreate | 4 | ✅ |
| UsuarioBase/Out | 2 | ✅ |
| LoginRequest/Response | 3 | ✅ |
| TareaBase/Create | 5 | ✅ |
| TareaOut/Detalle | 3 | ✅ |
| TareaUserRef | 2 | ✅ |
| ComentarioOut | 2 | ✅ |
| AsignarTareaRequest | 2 | ✅ |
| EstadisticasTareas | 7 | ✅ |
| EstadisticasUsuarios | 8 | ✅ |

**Validaciones testeadas:**
- ✅ Campos requeridos vs opcionales
- ✅ Tipos de datos (int, str, datetime, etc.)
- ✅ Valores literales (roles: "user"/"admin"/"supervisor")
- ✅ Constraints (`Field(ge=0)` para evitar negativos)
- ✅ Listas vacías y con datos
- ✅ Modelos anidados (usuarios en tareas, etc.)
- ✅ Casos edge (valores límite, sistemas vacíos)

### Tests Pendientes ⏳

**Core - Usuario, Tarea, GestorTareas** (Tarea para estudiantes)

```bash
# Crear archivo test/test_core.py
# Tests sugeridos:
# - test_crear_usuario_valido()
# - test_autenticar_usuario()
# - test_cambiar_password()
# - test_crear_tarea()
# - test_asignar_usuario_a_tarea()
# - test_permisos_por_rol()
# etc.
```

### Ejecutar Todos los Tests

```bash
# Modo verbose
pytest -v

# Con coverage
pytest --cov=api --cov=core --cov-report=html

# Específicos
pytest test/test_schemas.py::test_usuario_create_valido -v
```

---

## 🗺️ Roadmap

### ✅ Fase 1: Core (COMPLETADO)

- [x] Modelo de datos (Usuario, Tarea)
- [x] GestorTareas (orquestador)
- [x] Persistencia (pickle + JSON)
- [x] Autenticación bcrypt
- [x] Sistema de roles y permisos
- [x] CLI interactiva
- [x] Docstrings estilo Google

### ✅ Fase 2: Schemas y Validación (COMPLETADO)

- [x] 10 Schemas Pydantic
- [x] Validación automática de datos
- [x] 38 tests de schemas (100% passing)
- [x] Documentación completa

### 🚧 Fase 3: Tests de Core (EN PROGRESO - Para estudiantes)

- [ ] Tests unitarios de `core/usuarios.py` (15-20 tests)
- [ ] Tests unitarios de `core/tareas.py` (15-20 tests)
- [ ] Tests unitarios de `core/gestor.py` (20-25 tests)
- [ ] Tests de integración
- [ ] Coverage > 80%

### 📋 Fase 4: Backend Web (PLANIFICADO)

- [ ] Setup FastAPI + Jinja2
- [ ] Sistema de sesiones/cookies
- [ ] Templates base (base.html, navbar, etc.)
- [ ] Autenticación web (login/logout)
- [ ] Dashboard con estadísticas
- [ ] CRUD de tareas (lista, detalle, crear)
- [ ] Panel de administración
- [ ] Tests de endpoints (httpx)

### 📋 Fase 5: Frontend (PLANIFICADO)

- [ ] Templates HTML completos
- [ ] CSS responsivo (mobile-first)
- [ ] JavaScript para interactividad
- [ ] Formularios con validación
- [ ] Mensajes flash
- [ ] Dark mode opcional

### 📋 Fase 6: Producción (PLANIFICADO)

- [ ] Migrar a PostgreSQL/SQLite
- [ ] Docker containerization
- [ ] CI/CD con GitHub Actions
- [ ] Deploy (Railway/Render/Heroku)
- [ ] Logs y monitoreo

---

## 📂 Estructura del Proyecto

```
gestortareas/
│
├── 📁 core/                      # ✅ Lógica de negocio
│   ├── __init__.py
│   ├── gestor.py                # ✅ Orquestador principal
│   ├── usuarios.py              # ✅ Modelo Usuario + autenticación
│   ├── tareas.py                # ✅ Modelo Tarea + comentarios
│   └── utils.py                 # ✅ Persistencia y utilidades
│
├── 📁 api/                       # ✅ Schemas / 📋 App Web
│   ├── __init__.py
│   ├── schemas.py               # ✅ 10 Schemas Pydantic
│   └── app.py                   # 📋 FastAPI + Jinja2 (pendiente)
│
├── 📁 test/                      # ✅ Tests unitarios
│   ├── __init__.py
│   ├── test_schemas.py          # ✅ 38 tests (100% passing)
│   ├── test_core.py             # ⏳ Pendiente (para estudiantes)
│   └── test_app.py              # 📋 Tests de API (pendiente)
│
├── 📁 templates/                 # 📋 Templates Jinja2 (pendiente)
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── tareas/
│
├── 📁 static/                    # 📋 CSS/JS (pendiente)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
│
├── 📄 main.py                    # ✅ Punto de entrada CLI
├── 📄 interfaz_consola.py        # ✅ Menú interactivo
├── 📄 requirements.txt           # ✅ Dependencias
├── 📄 README.md                  # ✅ Este archivo
├── 📄 .gitignore                 # ✅ Ignorar archivos
│
└── 🗃️ datos/ (generado en runtime)
    ├── usuarios.dat              # Usuarios (pickle)
    ├── tareas.dat                # Tareas (pickle)
    └── tareas_finalizadas.json   # Histórico (JSON)
```

---

## 🎓 ¿Por qué Pydantic?

**Pydantic** es la librería estándar de facto para validación de datos en Python moderno.

### Ventajas

1. **Validación automática**: Convierte y valida datos en una sola operación
2. **Type hints nativos**: Usa las anotaciones de tipo de Python
3. **Documentación automática**: Genera schemas OpenAPI/Swagger
4. **Rendimiento**: Core escrito en Rust (pydantic-core)
5. **Developer-friendly**: Mensajes de error claros y útiles
6. **Integración perfecta** con FastAPI

### Ejemplo Práctico

```python
from pydantic import BaseModel, Field

class UsuarioCreate(BaseModel):
    """Crear usuario con validación automática."""
    nombre: str
    edad: int = Field(ge=0, le=150, description="Edad entre 0 y 150")
    email: str | None = None

# ✅ Válido
usuario = UsuarioCreate(nombre="Juan", edad=25)

# ❌ ValidationError (edad negativa)
usuario = UsuarioCreate(nombre="Ana", edad=-5)
```

### Validaciones Implementadas

En este proyecto usamos:

```python
# Valores literales (enums)
rol: Literal["user", "admin", "supervisor"]

# Constraints numéricos
total: int = Field(ge=0, description="No puede ser negativo")

# Campos opcionales
descripcion: Optional[str] = None

# Listas con tipos
usuarios: List[TareaUserRef] = []

# Modelos anidados
autor: TareaUserRef  # Otro modelo Pydantic
```

---

## 🤝 Contribución

### Para Estudiantes

Este proyecto está diseñado como material educativo. Áreas abiertas para contribuir:

#### 1. Tests de Core (Prioridad Alta) ⏳

Crear `test/test_core.py` con tests para:

- **`core/usuarios.py`**:
  - Creación de usuarios
  - Autenticación (password correcta/incorrecta)
  - Cambio de password
  - Reseteo de password
  - Roles (es_admin, es_supervisor)
  - Serialización (to_dict, from_dict)

- **`core/tareas.py`**:
  - Creación de tareas
  - Cambio de estado
  - Agregar/quitar usuarios
  - Agregar comentarios (validar permisos)
  - Serialización

- **`core/gestor.py`**:
  - CRUD de usuarios
  - CRUD de tareas
  - Validación de permisos por rol
  - Persistencia
  - Estadísticas

**Meta:** 50+ tests, coverage > 80%

#### 2. Implementación de FastAPI (Prioridad Alta) 📋

- Setup de FastAPI + Jinja2
- Sistema de sesiones
- Endpoints de autenticación
- CRUD de tareas
- Panel de administración

#### 3. Frontend (Prioridad Media) 📋

- Templates HTML con Jinja2
- CSS responsivo
- JavaScript para interactividad

#### 4. Mejoras (Prioridad Baja)

- Migrar a base de datos SQL
- Implementar búsqueda de tareas
- Filtros avanzados
- Exportar reportes

### Guía de Estilo

- **Docstrings**: Estilo Google obligatorio
- **Type hints**: En todas las funciones
- **Tests**: Cobertura mínima 80%
- **Commits**: Mensajes descriptivos en español
- **Code style**: black + ruff

### Workflow

```bash
# 1. Crear rama
git checkout -b feature/tests-core

# 2. Hacer cambios
# ... escribir código ...

# 3. Ejecutar tests
pytest -v

# 4. Commit y push
git add .
git commit -m "feat: agregar tests para core/usuarios.py"
git push origin feature/tests-core

# 5. Crear Pull Request en GitHub
```

---

## 📚 Recursos de Aprendizaje

### Documentación Oficial

- [Python 3.10+](https://docs.python.org/3/)
- [Pydantic](https://docs.pydantic.dev/)
- [FastAPI](https://fastapi.tiangolo.com/) (futuro)
- [Jinja2](https://jinja.palletsprojects.com/) (futuro)
- [pytest](https://docs.pytest.org/)

### Tutoriales Recomendados

- **Pydantic**: [Tutorial oficial](https://docs.pydantic.dev/latest/concepts/models/)
- **Testing con pytest**: [Real Python Guide](https://realpython.com/pytest-python-testing/)
- **FastAPI + Jinja2**: [Tutorial oficial](https://fastapi.tiangolo.com/advanced/templates/)
- **Type Hints**: [Python Typing](https://docs.python.org/3/library/typing.html)

---

## 📄 Licencia

MIT License - Ver archivo `LICENSE` para más detalles.

---

## 👥 Autores

- **Instructor/Profesor**: Arquitectura, diseño y revisión
- **Estudiantes**: Implementación, tests y mejoras

---

## 📞 Soporte

Para dudas o problemas:

1. Revisar la documentación en este README
2. Consultar docstrings en el código
3. Revisar tests existentes como ejemplos
4. Abrir un Issue en GitHub
5. Preguntar en clase

---

## 🎯 Quick Start

```bash
# 1. Clonar e instalar
git clone <repo-url>
cd gestortareas
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Ejecutar tests
pytest test/test_schemas.py -v
# ✅ 38 passed

# 3. Usar CLI
python main.py

# 4. (Futuro) Iniciar web
# uvicorn api.app:app --reload
```

---

## 📊 Métricas del Proyecto

| Métrica | Valor |
|---------|-------|
| **Líneas de código** | ~1500+ |
| **Tests pasando** | 38/38 (100%) |
| **Coverage (schemas)** | 100% |
| **Coverage (core)** | 0% (pendiente) |
| **Schemas Pydantic** | 10 |
| **Clases principales** | 3 (Usuario, Tarea, GestorTareas) |
| **Roles de usuario** | 3 (user, supervisor, admin) |
| **Estados de tarea** | 2 (pendiente, finalizada) |

---

## 🔐 Seguridad

- ✅ **Passwords hasheados** con bcrypt (cost factor 12)
- ✅ **Validación de entrada** con Pydantic
- ✅ **Permisos por rol** implementados
- 📋 **Sesiones seguras** con itsdangerous (pendiente)
- 📋 **HTTPS** en producción (pendiente)

---

**¡Happy Coding!** 🚀

*Última actualización: 6 de febrero de 2026*
