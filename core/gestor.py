from __future__ import annotations

import os
from typing import Dict, Optional

from usuarios import Usuario
from tareas import Tarea
import utils


class GestorTareas:
    """
    Controlador principal del sistema de gestión de tareas.

    Coordina usuarios, tareas, persistencia y reglas de negocio.
    """

    def __init__(self) -> None:
        """
        Inicializa el gestor y carga los datos desde disco.
        Las rutas se calculan automáticamente desde el directorio del proyecto.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self._usuarios_path = os.path.join(base_dir, "usuarios.dat")
        self._tareas_path = os.path.join(base_dir, "tareas.dat")
        self._historico_path = os.path.join(base_dir, "tareas_finalizadas.json")

        self.usuarios: Dict[str, Usuario] = {
            u.nombre: u for u in utils.cargar_datos(self._usuarios_path)
        }
        self.tareas: Dict[str, Tarea] = {
            t.nombre: t for t in utils.cargar_datos(self._tareas_path)
        }

    # ==================================================
    # Persistencia
    # ==================================================

    def _guardar_todo(self) -> None:
        """Guarda usuarios y tareas en disco."""
        utils.guardar_datos(self._usuarios_path, list(self.usuarios.values()))
        utils.guardar_datos(self._tareas_path, list(self.tareas.values()))

    # ==================================================
    # Usuarios
    # ==================================================

    def crear_usuario(
        self,
        nombre: str,
        nombre_visible: str,
        rol: str = "user",
        password: Optional[str] = None,
    ) -> Usuario:
        """
        Crea un nuevo usuario.

        Raises:
            ValueError: Si el nombre ya existe.
        """
        if nombre in self.usuarios:
            raise ValueError("Ya existe un usuario con ese nombre.")

        usuario = Usuario(
            nombre=nombre,
            nombre_visible=nombre_visible,
            rol=rol,
            password=password,
        )

        self.usuarios[nombre] = usuario
        self._guardar_todo()
        return usuario

    def autenticar_usuario(self, nombre: str, password: str) -> Usuario:
        """
        Autentica un usuario por nombre y contraseña.

        Raises:
            ValueError: Si las credenciales son inválidas.
        """
        usuario = self.usuarios.get(nombre)
        if not usuario:
            raise ValueError("Usuario inexistente.")

        if not usuario.verificar_password(password):
            raise ValueError("Contraseña incorrecta.")

        return usuario

    def resetear_password_usuario(
        self,
        admin: Usuario,
        nombre_usuario: str,
    ) -> None:
        """
        Resetea la contraseña de un usuario (solo admin).

        Raises:
            PermissionError: Si el solicitante no es admin.
        """
        if not admin.es_admin():
            raise PermissionError("Solo un admin puede resetear contraseñas.")

        usuario = self.usuarios.get(nombre_usuario)
        if not usuario:
            raise ValueError("Usuario inexistente.")

        usuario.resetear_password()
        self._guardar_todo()

    # ==================================================
    # Tareas
    # ==================================================


    def crear_tarea(self, nombre: str, descripcion: str, actor: Usuario) -> Tarea:
        """
        Crea una nueva tarea.

        Raises:
            ValueError: Si el nombre ya existe.
        """
        if not (actor.es_admin() or actor.es_supervisor()):
            raise PermissionError(
                "Solo administradores o supervisores pueden crear tareas."
            )


        if nombre in self.tareas:
            raise ValueError("Ya existe una tarea con ese nombre.")

        tarea = Tarea(nombre=nombre, descripcion=descripcion)
        self.tareas[nombre] = tarea
        self._guardar_todo()
        return tarea


    def asignar_usuario_tarea(
        self,
        actor: Usuario,
        nombre_usuario: str,
        nombre_tarea: str,
    ) -> None:
        if not (actor.es_admin() or actor.es_supervisor()):
            raise PermissionError("No tiene permisos para asignar tareas.")

        usuario = self.usuarios.get(nombre_usuario)
        tarea = self.tareas.get(nombre_tarea)

        if not usuario or not tarea:
            raise ValueError("Usuario o tarea inexistente.")

        if actor.es_supervisor() and usuario.rol != "user":
            raise PermissionError(
                "Un supervisor solo puede asignar tareas a usuarios comunes."
            )

        tarea.agregar_usuario(usuario)
        self._guardar_todo()


    def finalizar_tarea(self, nombre_tarea: str) -> None:
        """
        Finaliza una tarea y la guarda en el histórico JSON.
        """
        tarea = self.tareas.get(nombre_tarea)
        if not tarea:
            raise ValueError("Tarea inexistente.")

        tarea.cambiar_estado("finalizada")

        historico = utils.leer_json(self._historico_path, default=[])
        historico.append(tarea.obtener_detalle())
        utils.escribir_json(self._historico_path, historico)

        self._guardar_todo()

    def eliminar_tarea(self, nombre_tarea: str) -> None:
        """
        Elimina una tarea solo si está finalizada.
        """
        tarea = self.tareas.get(nombre_tarea)
        if not tarea:
            raise ValueError("Tarea inexistente.")

        if tarea.estado != "finalizada":
            raise ValueError("Solo se pueden eliminar tareas finalizadas.")

        del self.tareas[nombre_tarea]
        self._guardar_todo()

    # ==================================================
    # Consulta
    # ==================================================

    def listar_tareas(self) -> None:
        """Imprime todas las tareas."""
        if not self.tareas:
            print("No hay tareas.")
            return

        for tarea in self.tareas.values():
            print("-" * 40)
            print(tarea.obtener_info_detallada())

    def existe_admin(self) -> bool:
        """
        Verifica si existe al menos un usuario con rol admin.
        """
        return any(usuario.es_admin() for usuario in self.usuarios.values())
        
    def listar_usuarios(self) -> list[Usuario]:
        """
        Devuelve la lista de todos los usuarios del sistema.
        """
        return list(self.usuarios.values())

    def obtener_tareas_de_usuario(self, usuario: Usuario) -> list[Tarea]:
        """
        Devuelve todas las tareas asignadas a un usuario.
        """
        return [
            tarea
            for tarea in self.tareas.values()
            if any(u.id == usuario.id for u in tarea.usuarios_asignados)
        ]

    def obtener_estadisticas(self) -> dict[str, int]:
        """
        Devuelve estadísticas generales de las tareas.
        """
        return utils.calcular_estadisticas_tareas(list(self.tareas.values()))

