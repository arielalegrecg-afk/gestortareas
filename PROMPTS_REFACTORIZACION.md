# 🎓 Prompts Progresivos: De Scripts Sueltos a Arquitectura Modular

Este documento contiene una secuencia de prompts diseñados para guiar a estudiantes en la refactorización de un proyecto Python desde scripts sueltos hasta una arquitectura modular profesional.

**Objetivo**: Transformar un proyecto con archivos sueltos en la raíz a una estructura organizada con módulos `core/`, `api/`, y `test/`.

**Metodología**: Cada prompt simula una conversación con un LLM (ChatGPT, Claude, etc.) donde el estudiante aprende conceptos y recibe código guiado.

---

## 📋 Contexto del Proyecto Inicial

**Situación de partida** (lo que tienen los alumnos):
```
gestortareas/
├── usuarios.py          # Script con clase Usuario
├── tareas.py            # Script con clase Tarea
├── gestor_tareas.py     # Script con GestorTareas
├── utils.py             # Funciones de persistencia
├── interfaz_consola.py  # Menú CLI
├── main.py              # Punto de entrada
└── requirements.txt     # Dependencias básicas
```

**Situación objetivo** (arquitectura modular):
```
gestortareas/
├── core/                # Lógica de negocio
│   ├── __init__.py
│   ├── usuarios.py
│   ├── tareas.py
│   ├── gestor.py
│   └── utils.py
├── api/                 # Capa de API/Schemas
│   ├── __init__.py
│   ├── schemas.py
│   └── app.py
├── test/                # Tests
│   ├── __init__.py
│   ├── test_schemas.py
│   └── test_core.py
├── main.py
├── interfaz_consola.py
├── pyproject.toml       # Gestión moderna de dependencias
└── requirements.txt
```

---

## 🎯 Secuencia de Prompts

### **Fase 1: Entender la Arquitectura Actual**

#### Prompt 1.1: Análisis del Código Existente

```
Rol: Actúa como un arquitecto de software senior especializado en Python.

Contexto: Soy estudiante y tengo un proyecto de gestión de tareas en Python. 
Actualmente todos mis archivos están en la raíz del proyecto:
- usuarios.py (clase Usuario con autenticación bcrypt)
- tareas.py (clase Tarea con estados y comentarios)
- gestor_tareas.py (clase GestorTareas que orquesta todo)
- utils.py (funciones de persistencia con pickle)
- interfaz_consola.py (menú interactivo CLI)
- main.py (punto de entrada)

Tarea:
1. Explícame qué problemas tiene esta estructura para un proyecto que va a crecer
2. ¿Qué es una "arquitectura modular" y por qué es mejor?
3. Muéstrame un diagrama de cómo debería organizarse el proyecto

Formato: Explicación didáctica con ejemplos visuales.
```

---

#### Prompt 1.2: Conceptos de Separación de Responsabilidades

```
Rol: Actúa como profesor de ingeniería de software.

Contexto: Entiendo que debo modularizar mi proyecto, pero no tengo claro 
qué significa "separar responsabilidades" en la práctica.

Pregunta:
1. ¿Qué es el patrón "Separation of Concerns"?
2. ¿Qué diferencia hay entre "lógica de negocio" (core) y "capa de presentación" (API/UI)?
3. En mi proyecto de tareas, ¿qué código va en cada capa?

Ejemplos concretos:
- ¿La validación de passwords va en core o en API?
- ¿La autenticación con bcrypt va en core o en API?
- ¿Los schemas de Pydantic van en core o en API?

Formato: Explicación con tabla comparativa y ejemplos de mi proyecto.
```

---

### **Fase 2: Crear la Estructura de Carpetas**

#### Prompt 2.1: Planificar la Migración

```
Rol: Actúa como consultor de refactorización de código.

Contexto: Quiero reorganizar mi proyecto Python en módulos pero tengo miedo 
de romper algo. Actualmente tengo 6 archivos en la raíz.

Tarea:
1. Dame un plan paso a paso para migrar sin romper el código
2. ¿Qué carpetas debo crear primero?
3. ¿En qué orden debo mover los archivos?
4. ¿Cómo manejo los imports que se van a romper?

Restricciones:
- No quiero hacer todo de golpe
- Quiero poder probar que funciona después de cada paso
- Necesito mantener la CLI funcionando durante la migración

Formato: Plan numerado con comandos Git para cada paso.
```

---

#### Prompt 2.2: Crear Módulo Core

```
Rol: Actúa como desarrollador Python senior.

Contexto: Voy a crear la carpeta `core/` para mi lógica de negocio.

Tarea:
1. ¿Qué archivos debo crear en `core/`?
2. ¿Qué debe contener el archivo `__init__.py`?
3. Muéstrame cómo mover `usuarios.py`, `tareas.py`, `gestor_tareas.py` y `utils.py` a `core/`
4. ¿Cómo actualizo los imports en `main.py` e `interfaz_consola.py`?

Código actual en main.py:
```python
from usuarios import Usuario
from tareas import Tarea
from gestor_tareas import GestorTareas
```

Formato: Comandos de terminal + código actualizado de imports.
```

---

#### Prompt 2.3: Crear Módulo API con Schemas

```
Rol: Actúa como experto en FastAPI y Pydantic.

Contexto: Ya tengo mi lógica de negocio en `core/`. Ahora quiero crear 
una capa de API con schemas de Pydantic para validación de datos.

Tarea:
1. Explícame qué son los "schemas" y por qué separarlos del core
2. Crea la estructura de la carpeta `api/`
3. Genera schemas de Pydantic para:
   - Crear usuario (UsuarioCreate)
   - Login (LoginRequest, LoginResponse)
   - Crear tarea (TareaCreate)
   - Ver tarea (TareaOut)

Información del core:
- Usuario tiene: nombre, password_hash, rol (user/supervisor/admin)
- Tarea tiene: titulo, descripcion, estado, usuarios_asignados, comentarios

Formato: Código completo de `api/schemas.py` con docstrings.
```

---

### **Fase 3: Testing y Validación**

#### Prompt 3.1: Crear Tests para Schemas

```
Rol: Actúa como especialista en testing con pytest.

Contexto: Acabo de crear `api/schemas.py` con 10 schemas de Pydantic. 
Necesito tests para asegurarme de que la validación funciona correctamente.

Tarea:
1. Explícame qué debo testear en un schema de Pydantic
2. Crea la estructura de `test/test_schemas.py`
3. Genera tests para validar:
   - Campos requeridos vs opcionales
   - Tipos de datos correctos
   - Validaciones (min_length, ge, Literal)
   - Casos edge (listas vacías, valores límite)

Schemas a testear:
- UsuarioCreate (nombre, password, rol)
- TareaCreate (titulo, descripcion)
- EstadisticasTareas (total, pendientes, finalizadas)

Formato: Código pytest con al menos 20 tests.
```

---

#### Prompt 3.2: Ejecutar y Entender Tests

```
Rol: Actúa como tutor de pytest.

Contexto: Tengo tests en `test/test_schemas.py` pero es la primera vez 
que uso pytest.

Preguntas:
1. ¿Cómo ejecuto los tests desde la terminal?
2. ¿Qué significan los símbolos . (punto) y F (efe) en la salida?
3. Si un test falla, ¿cómo leo el mensaje de error?
4. ¿Cómo ejecuto solo un test específico?
5. ¿Qué es "coverage" y cómo lo mido?

Comandos que necesito:
- Ejecutar todos los tests
- Ejecutar solo test_schemas.py
- Ejecutar un test específico
- Ver coverage

Formato: Guía de comandos con explicación de salidas.
```

---

### **Fase 4: Gestión Moderna de Dependencias**

#### Prompt 4.1: Migrar a pyproject.toml con uv

```
Rol: Actúa como experto en gestión de paquetes Python moderno.

Contexto: Mi proyecto usa `requirements.txt` pero quiero migrar a 
`pyproject.toml` usando `uv` (gestor de paquetes ultrarrápido).

Preguntas:
1. ¿Qué ventajas tiene pyproject.toml sobre requirements.txt?
2. ¿Qué es `uv` y por qué es más rápido que pip?
3. ¿Cómo creo un pyproject.toml desde cero?
4. ¿Cómo migro mis dependencias de requirements.txt?

Dependencias actuales:
```
pydantic>=2.0.0
bcrypt>=4.0.0
pytest>=7.0.0
rich>=13.0.0
```

Tarea:
- Genera un pyproject.toml completo
- Incluye metadata del proyecto
- Separa dependencias de desarrollo (dev) y web (futuras)
- Muestra comandos de uv para instalar

Formato: Archivo pyproject.toml + comandos de terminal.
```

---

#### Prompt 4.2: Entornos Virtuales con uv

```
Rol: Actúa como instructor de Python DevOps.

Contexto: Quiero usar `uv` para gestionar entornos virtuales y 
seleccionar versiones específicas de Python.

Preguntas:
1. ¿Cómo creo un entorno virtual con uv?
2. ¿Cómo selecciono una versión específica de Python (ej: 3.11)?
3. ¿Cómo instalo dependencias del pyproject.toml?
4. ¿Cómo activo el entorno en Windows vs Linux?
5. ¿Qué es el archivo uv.lock y para qué sirve?

Comandos que necesito:
- Ver versiones de Python disponibles
- Instalar Python 3.11
- Crear entorno con Python 3.11
- Sincronizar dependencias
- Activar entorno

Formato: Guía paso a paso con comandos para Windows y Linux.
```

---

### **Fase 5: Documentación del Proyecto**

#### Prompt 5.1: Actualizar README

```
Rol: Actúa como redactor técnico especializado en documentación de software.

Contexto: Acabo de refactorizar mi proyecto a una arquitectura modular. 
Necesito actualizar el README.md para reflejar los cambios.

Tarea:
1. Genera un README.md profesional que incluya:
   - Descripción del proyecto
   - Arquitectura (diagrama de carpetas)
   - Instalación con uv (paso a paso)
   - Uso (CLI y futura API web)
   - Testing (cómo ejecutar tests)
   - Estructura del proyecto (explicada)

Información del proyecto:
- Nombre: Gestor de Tareas
- Tecnologías: Python 3.8+, Pydantic, bcrypt, pytest, FastAPI (futuro)
- Arquitectura: Modular (core, api, test)
- Tests: 38 tests pasando (100% schemas)

Formato: Markdown con emojis, badges, y secciones colapsables.
```

---

#### Prompt 5.2: Documentar Decisiones de Arquitectura

```
Rol: Actúa como arquitecto de software documentando decisiones técnicas.

Contexto: Quiero documentar POR QUÉ tomé ciertas decisiones arquitectónicas 
para que otros desarrolladores (o yo en el futuro) entiendan el razonamiento.

Tarea:
Crea un documento `docs/ARQUITECTURA.md` que explique:

1. ¿Por qué separar core de api?
2. ¿Por qué usar Pydantic para schemas en vez de validación manual?
3. ¿Por qué usar bcrypt en core y no en api?
4. ¿Por qué pytest en vez de unittest?
5. ¿Por qué pyproject.toml en vez de requirements.txt?
6. ¿Por qué uv en vez de pip/poetry?

Formato: Documento estilo ADR (Architecture Decision Record) con:
- Contexto
- Decisión
- Consecuencias
- Alternativas consideradas
```

---

### **Fase 6: Preparación para Web (FastAPI)**

#### Prompt 6.1: Entender Seguridad en APIs

```
Rol: Actúa como experto en seguridad de aplicaciones web.

Contexto: Voy a crear una interfaz web con FastAPI. Necesito entender 
cómo implementar autenticación y validación de forma segura.

Preguntas:
1. ¿Por qué usar Pydantic y PyJWT juntos para seguridad?
2. ¿Qué vulnerabilidades previene cada uno?
3. ¿Qué es un JWT y cómo funciona?
4. ¿Cómo se complementan en una arquitectura de seguridad?

Casos de uso:
- Usuario hace login → ¿Cómo genero el token?
- Usuario crea tarea → ¿Cómo valido token + datos?
- Atacante intenta modificar token → ¿Cómo lo prevengo?

Formato: Explicación didáctica con diagramas y ejemplos de código.
```

---

#### Prompt 6.2: Guía de PyJWT

```
Rol: Actúa como instructor de autenticación web con JWT.

Contexto: Voy a usar PyJWT (no python-jose) para autenticación en mi API.

Tarea:
1. Explícame los conceptos básicos de JWT (header, payload, signature)
2. Muestra cómo crear un token con PyJWT
3. Muestra cómo verificar y decodificar un token
4. Integración con FastAPI (cookies HttpOnly)
5. Mejores prácticas de seguridad

Casos de uso de mi proyecto:
- Login: crear token con username y rol
- Dashboard: verificar token desde cookie
- Logout: eliminar cookie

Formato: Guía completa con código funcional y explicaciones.
```

---

#### Prompt 6.3: Estructura de la Aplicación Web

```
Rol: Actúa como arquitecto de aplicaciones FastAPI.

Contexto: Quiero crear una interfaz web con FastAPI que use Server-Side 
Rendering (Jinja2), NO una API REST JSON.

Requisitos:
- Renderizar HTML directamente (no SPA)
- Autenticación con JWT en cookies
- Conectar directamente con el core (sin capa REST intermedia)
- Templates con Jinja2

Tarea:
1. Diseña la estructura de archivos para la app web
2. Explica qué va en cada archivo (app.py, auth.py, dependencies.py)
3. Muestra cómo configurar FastAPI + Jinja2
4. Crea las rutas básicas (/, /login, /dashboard, /logout)

Formato: Estructura de carpetas + código de ejemplo para cada archivo.
```

---

### **Fase 7: Integración y Testing**

#### Prompt 7.1: Tests de Autenticación

```
Rol: Actúa como especialista en testing de seguridad.

Contexto: Implementé autenticación con PyJWT. Necesito tests para 
asegurarme de que es segura.

Tarea:
Crea `test/test_auth.py` con tests para:

1. Crear token válido
2. Verificar token válido
3. Rechazar token expirado
4. Rechazar token con firma incorrecta
5. Rechazar token modificado (tampering)
6. Validar claims del payload

Módulo a testear:
```python
# api/auth.py
def crear_access_token(username: str, rol: str) -> str
def verificar_access_token(token: str) -> dict | None
```

Formato: Código pytest con al menos 10 tests de seguridad.
```

---

#### Prompt 7.2: Integración Core + API

```
Rol: Actúa como desarrollador full-stack Python.

Contexto: Tengo el core (lógica de negocio) y los schemas (validación) 
separados. Necesito integrarlos en endpoints de FastAPI.

Tarea:
Muestra cómo crear un endpoint que:
1. Recibe datos validados por Pydantic
2. Verifica autenticación con PyJWT
3. Llama a la lógica del core
4. Devuelve respuesta validada

Ejemplo: Endpoint POST /tareas para crear tarea

Capas involucradas:
- FastAPI (routing)
- Pydantic (validación de TareaCreate)
- PyJWT (verificar usuario autenticado)
- Core (gestor.crear_tarea())

Formato: Código completo del endpoint con comentarios explicativos.
```

---

### **Fase 8: Deployment y Buenas Prácticas**

#### Prompt 8.1: Variables de Entorno

```
Rol: Actúa como DevOps engineer especializado en Python.

Contexto: Tengo secretos hardcodeados en mi código (SECRET_KEY para JWT). 
Necesito usar variables de entorno.

Tarea:
1. Explica por qué es peligroso hardcodear secretos
2. Muestra cómo usar variables de entorno en Python
3. Crea un archivo .env.example
4. Configura python-dotenv o pydantic-settings
5. Actualiza .gitignore para no commitear secretos

Secretos en mi proyecto:
- JWT_SECRET_KEY
- DATABASE_PATH (futuro)
- ADMIN_PASSWORD (futuro)

Formato: Código + archivo .env.example + guía de seguridad.
```

---

#### Prompt 8.2: Git y Control de Versiones

```
Rol: Actúa como instructor de Git y GitHub.

Contexto: Acabo de refactorizar mi proyecto. Quiero hacer commits 
organizados y crear una rama para la interfaz web.

Tarea:
1. ¿Cómo hago commits semánticos? (feat, fix, refactor, docs)
2. ¿Cómo creo una rama para la interfaz web?
3. ¿Qué archivos debo ignorar en .gitignore?
4. ¿Cómo escribo buenos mensajes de commit?

Cambios realizados:
- Refactorización a arquitectura modular
- Creación de schemas con Pydantic
- Tests con pytest
- Migración a pyproject.toml

Formato: Comandos Git + ejemplos de mensajes de commit.
```

---

## 🎓 Cómo Usar Estos Prompts en Clase

### Metodología Sugerida

1. **Presentación (5 min)**
   - Mostrar proyecto inicial (scripts sueltos)
   - Mostrar proyecto objetivo (arquitectura modular)

2. **Demostración en Vivo (40 min)**
   - Usar prompts 1.1 y 1.2 con un LLM en vivo
   - Mostrar cómo el LLM explica conceptos
   - Ejecutar código generado y verificar que funciona

3. **Práctica Guiada (30 min)**
   - Estudiantes usan prompts 2.1 a 2.3
   - Crean estructura de carpetas
   - Mueven archivos con ayuda del LLM

4. **Trabajo Autónomo (resto de clase)**
   - Estudiantes avanzan con prompts 3.x a 6.x
   - Profesor asiste dudas específicas

### Tips para Estudiantes

✅ **Hacer**:
- Leer la respuesta del LLM completa antes de copiar código
- Probar el código después de cada cambio
- Hacer commits frecuentes
- Preguntar "¿por qué?" cuando no entiendas algo

❌ **Evitar**:
- Copiar código sin entender
- Hacer todos los cambios de golpe sin probar
- Ignorar errores y seguir adelante
- Usar prompts fuera de orden

### Evaluación Sugerida

- **Checkpoint 1**: Estructura de carpetas creada (Fase 2)
- **Checkpoint 2**: Tests pasando (Fase 3)
- **Checkpoint 3**: pyproject.toml funcionando (Fase 4)
- **Entrega Final**: Proyecto completo con documentación (Fase 5-8)

---

## 📚 Recursos Adicionales

- **Documentación de uv**: https://docs.astral.sh/uv/
- **Pydantic Tutorial**: https://docs.pydantic.dev/latest/
- **PyJWT Docs**: https://pyjwt.readthedocs.io/
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/
- **pytest Docs**: https://docs.pytest.org/

