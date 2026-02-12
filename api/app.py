from core import GestorTareas

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# from core.gestor import GestorTareas
from core.usuarios import Usuario

# import jwt
from datetime import datetime, timedelta

# ==================================================
# Configuración básica
# ==================================================

app = FastAPI()
templates = Jinja2Templates(directory="api/templates")

gestor = GestorTareas()

SECRET_KEY = "clave_super_secreta"
ALGORITHM = "HS256"

# ==================================================
# JWT helpers
# ==================================================

def crear_token(usuario: Usuario):
    payload = {
        "sub": usuario.nombre,
        "rol": usuario.rol,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def obtener_usuario_actual(request: Request) -> Usuario:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        usuario = gestor.usuarios.get(username)

        if not usuario:
            raise HTTPException(status_code=401)

        return usuario

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ==================================================
# Rutas HTML
# ==================================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# ---------------- LOGIN ----------------

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        usuario = gestor.autenticar_usuario(username, password)

        token = crear_token(usuario)

        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  # evita acceso desde JS
            secure=False    # poner True en producción con HTTPS
        )
        return response

    except Exception:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Credenciales inválidas"
            }
        )


# ---------------- DASHBOARD ----------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    usuario: Usuario = Depends(obtener_usuario_actual)
):
    tareas = gestor.obtener_tareas_de_usuario(usuario)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "usuario": usuario,
            "tareas": tareas
        }
    )


# ---------------- LOGOUT ----------------

@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response


