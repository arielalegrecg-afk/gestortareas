import os
from typing import List, Dict, Tuple

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.prompt import Prompt, Confirm

from usuarios import Usuario
from tareas import Tarea


class InterfazConsola:
    """
    Capa de presentación del sistema usando Rich.
    No contiene lógica de negocio.
    """

    def __init__(self) -> None:
        theme = Theme(
            {
                "title": "bold blue",
                "success": "green",
                "error": "bold red",
                "warning": "yellow",
                "info": "cyan",
            }
        )
        self.console = Console(theme=theme)

    # ==================================================
    # Utilidades generales
    # ==================================================

    def limpiar_pantalla(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def pausa(self) -> None:
        self.console.print("\n[info]Presione ENTER para continuar...[/info]")
        Prompt.ask("", default="", show_default=False)

    # ==================================================
    # Mensajes básicos
    # ==================================================

    def mostrar_titulo(self, texto: str) -> None:
        panel = Panel(
            Align.center(f"[title]{texto}[/title]"),
            expand=False,
            border_style="blue",
        )
        self.console.print(panel)

    def mostrar_exito(self, texto: str) -> None:
        self.console.print(f"✅ [success]{texto}[/success]")

    def mostrar_error(self, texto: str) -> None:
        self.console.print(f"❌ [error]{texto}[/error]")

    def mostrar_advertencia(self, texto: str) -> None:
        self.console.print(f"⚠️ [warning]{texto}[/warning]")

    # ==================================================
    # Login y autenticación
    # ==================================================

    def pedir_credenciales(self) -> Tuple[str, str]:
        self.mostrar_titulo("Login")
        usuario = Prompt.ask("Usuario")
        password = Prompt.ask("Contraseña", password=True)
        return usuario, password

    def mostrar_bienvenida(self, usuario: Usuario) -> None:
        texto = (
            f"👋 Bienvenido [bold]{usuario.nombre_visible}[/bold]\n\n"
            f"Rol: [info]{usuario.rol.upper()}[/info]"
        )
        panel = Panel(Align.center(texto), title="Sesión iniciada", expand=False)
        self.console.print(panel)

    def mostrar_asistente_crear_password(self) -> str:
        self.mostrar_titulo("Configuración de contraseña")
        self.console.print(
            "Este es tu primer ingreso. Debés configurar una contraseña.\n",
            style="info",
        )

        while True:
            pwd1 = Prompt.ask("Nueva contraseña", password=True)
            pwd2 = Prompt.ask("Repetir contraseña", password=True)

            if pwd1 != pwd2:
                self.mostrar_error("Las contraseñas no coinciden.")
            elif not pwd1:
                self.mostrar_error("La contraseña no puede estar vacía.")
            else:
                self.mostrar_exito("Contraseña configurada.")
                return pwd1

    # ==================================================
    # Menús
    # ==================================================

    def mostrar_menu_admin(self) -> str:
        panel = Panel(
            "\n".join(
                [
                    "1️⃣ Ver usuarios",
                    "2️⃣ Crear usuario",
                    "3️⃣ Resetear password",
                    "4️⃣ Ver estadísticas",
                    "",
                    "0️⃣ Logout",
                ]
            ),
            title="Menú Administrador",
            border_style="blue",
        )
        self.console.print(panel)
        return Prompt.ask("Opción")

    def mostrar_menu_usuario(self) -> str:
        panel = Panel(
            "\n".join(
                [
                    "1️⃣ Ver mis tareas",
                    "2️⃣ Crear tarea",
                    "3️⃣ Finalizar tarea",
                    "4️⃣ Ver perfil",
                    "",
                    "0️⃣ Logout",
                ]
            ),
            title="Menú Usuario",
            border_style="blue",
        )
        self.console.print(panel)
        return Prompt.ask("Opción")

    # ==================================================
    # Usuarios
    # ==================================================

    def mostrar_usuarios(self, usuarios: List[Usuario]) -> None:
        table = Table(title="Usuarios del sistema", show_lines=True)
        table.add_column("Username")
        table.add_column("Nombre visible")
        table.add_column("Rol")
        table.add_column("Creado")

        for u in usuarios:
            table.add_row(
                u.nombre,
                u.nombre_visible,
                u.rol,
                u.fecha_creacion.strftime("%Y-%m-%d"),
            )

        self.console.print(table)

    def pedir_datos_nuevo_usuario(self) -> Dict:
        self.mostrar_titulo("Crear usuario")

        nombre = Prompt.ask("Username")
        visible = Prompt.ask("Nombre visible")
        rol = Prompt.ask("Rol", choices=["user", "admin"], default="user")
        tiene_pwd = Confirm.ask("¿Asignar contraseña ahora?", default=False)

        password = None
        if tiene_pwd:
            password = Prompt.ask("Contraseña", password=True)

        return {
            "nombre": nombre,
            "nombre_visible": visible,
            "rol": rol,
            "password": password,
        }

    def pedir_usuario_para_reset(self) -> str:
        return Prompt.ask("Username a resetear")

    # ==================================================
    # Tareas
    # ==================================================

    def mostrar_tareas(self, tareas: List[Tarea]) -> None:
        table = Table(title="Tareas", show_lines=True)
        table.add_column("Nombre")
        table.add_column("Estado")
        table.add_column("Creada")
        table.add_column("Usuarios")

        for t in tareas:
            usuarios = ", ".join(u.nombre_visible for u in t.usuarios_asignados)
            table.add_row(
                t.nombre,
                t.estado,
                t.fecha_creacion.strftime("%Y-%m-%d"),
                usuarios or "-",
            )

        self.console.print(table)

    def pedir_datos_nueva_tarea(self) -> Dict:
        self.mostrar_titulo("Crear tarea")
        nombre = Prompt.ask("Nombre de la tarea")
        descripcion = Prompt.ask("Descripción")
        return {"nombre": nombre, "descripcion": descripcion}

    def pedir_tarea_a_finalizar(self) -> str:
        return Prompt.ask("Nombre de la tarea a finalizar")

    # ==================================================
    # Perfil y estadísticas
    # ==================================================

    def mostrar_perfil(self, usuario: Usuario) -> None:
        texto = (
            f"👤 {usuario.nombre_visible}\n\n"
            f"Username: {usuario.nombre}\n"
            f"Rol: {usuario.rol}\n"
            f"Creado: {usuario.fecha_creacion.strftime('%Y-%m-%d %H:%M')}"
        )
        panel = Panel(texto, title="Perfil", border_style="cyan")
        self.console.print(panel)

    def mostrar_estadisticas(self, stats: Dict[str, int]) -> None:
        table = Table(title="Estadísticas de tareas")
        table.add_column("Total")
        table.add_column("Pendientes")
        table.add_column("Finalizadas")

        table.add_row(
            str(stats.get("total", 0)),
            str(stats.get("pendientes", 0)),
            str(stats.get("finalizadas", 0)),
        )

        self.console.print(table)
