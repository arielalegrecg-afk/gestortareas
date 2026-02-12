from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.gestor import GestorTareas
from core.usuarios import Usuario

# ============================================
# Configuración básica
# ============================================

app = FastAPI()
templates = Jinja2Templates(directory="api/templates")

gestor = GestorTareas()


# ============================================
# Helper simple: usuario desde cookie
# ============================================

def obtener_usuario_actual(request: Request) -> Usuario:
    username = request.cookies.get("username")

    if not username:
        raise HTTPException(status_code=401)

    usuario = gestor.usuarios.get(username)

    if not usuario:
        raise HTTPException(status_code=401)

    return usuario


# ============================================
# RUTAS
# ============================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )



# ---------------- LOGIN ----------------

@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    try:
        usuario = gestor.autenticar_usuario(username, password)

        response = RedirectResponse("/dashboard", status_code=302)
        response.set_cookie(
            key="username",
            value=usuario.nombre,
            httponly=True
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
    response.delete_cookie("username")
    return response
