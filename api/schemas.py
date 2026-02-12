"""Esquemas Pydantic para la API REST del gestor de tareas.

Este módulo define los modelos de datos utilizados para validación,
serialización y documentación automática de la API.

Typical usage example:

    usuario = UsuarioCreate(
        nombre="jdoe",
        nombre_visible="John Doe",
        rol="admin"
    )
"""

from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel , ConfigDict, Field


class UsuarioBase(BaseModel):
    """Modelo base de usuario.

    Attributes:
        id (str): Identificador único del usuario.
        
        nombre (str): Nombre de usuario utilizado para login.
        
        nombre_visible (str): Nombre mostrado en la interfaz.
        
        rol (str): Rol del usuario ('user', 'admin' o 'supervisor').
        
        fecha_creacion (datetime): Fecha y hora de creación del usuario.
    """

    id: str
    
    nombre: str
    
    nombre_visible: str
    
    rol: Literal["user", "admin", "supervisor"]
    
    fecha_creacion: datetime
    
    # para permitir la creación desde objetos con atributos
    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(BaseModel):
    """Datos necesarios para crear un usuario.

    Attributes:
        
        nombre (str): Nombre de usuario utilizado para login.
            unico en el sistema.
        
        nombre_visible (str): Nombre mostrado en la interfaz.
        
        password (Optional[str]): Contraseña inicial del usuario.
            Opcional, puede ser None.
        
        rol (str): Rol del usuario ('user', 'admin' o 'supervisor').
            por defecto es 'user'.
    """

    nombre: str
    
    nombre_visible: str
    
    password: Optional[str] = None
    
    rol: Literal["user", "admin", "supervisor"] = "user"

class UsuarioOut(UsuarioBase):
    """Datos expuestos de un usuario en respuestas de la API.

    Hereda todos los atributos de UsuarioBase.
    """
    pass

class LoginRequest(BaseModel):
    """Credenciales de inicio de sesión.

    Attributes:

        nombre (str): Nombre de usuario.
        
        password (str): Contraseña en texto plano.
    """

    nombre: str
    
    password: str

class LoginResponse(BaseModel):
    """Respuesta de inicio de sesión.

    Attributes:
        
        usuario (UsuarioOut): Datos del usuario autenticado.
    """

    usuario: UsuarioOut

class TareaUserRef(BaseModel):
    """Referencia ligera a un usuario dentro de una tarea.

    Attributes:
        
        id (str): Identificador único del usuario.
        
        nombre (str): Nombre de usuario.
        
        nombre_visible (str): Nombre mostrado en la interfaz.
        
        rol (str): Rol del usuario asociado a la tarea.
    """

    id: str
    
    nombre: str
    
    nombre_visible: str
    
    rol: Literal["user", "admin", "supervisor"]

class ComentarioOut(BaseModel):
    """Comentario asociado a una tarea.

    Attributes:
        
        texto (str): Contenido del comentario.
        
        autor (TareaUserRef): Usuario autor del comentario.
        
        fecha (datetime): Fecha y hora en que se creó el comentario.
    """

    texto: str
    
    autor: TareaUserRef
    
    fecha: datetime

class TareaBase(BaseModel):
    """Modelo base de tarea.

    Attributes:
        
        nombre (str): Nombre o título de la tarea.
        
        descripcion (Optional[str]): Descripción detallada de la tarea.
        
        estado (str): Estado actual de la tarea ('pendiente' o 'finalizada').
        
        fecha_creacion (datetime): Fecha y hora de creación de la tarea.
    """
    
    nombre: str
    
    descripcion: Optional[str] = None
    
    estado: Literal["pendiente", "finalizada"]
    
    fecha_creacion: datetime

    # para permitir la creación desde objetos con atributos
    model_config = ConfigDict(from_attributes=True)

class TareaCreate(BaseModel):
    """Datos necesarios para crear una tarea.

    Attributes:
        
        nombre (str): Nombre o título de la tarea.
        
        descripcion (Optional[str]): Descripción detallada de la tarea.
    """
    
    nombre: str

    descripcion: Optional[str] = None

class TareaOut(TareaBase):
    """Salida simplificada de una tarea.

    Hereda los campos base de TareaBase.
    """

    usuarios_asignados: List[TareaUserRef] = []

class TareaDetalle(TareaBase):
    """Detalle completo de una tarea.

    Attributes:
        
        usuarios_asignados (List[TareaUserRef]): Usuarios asignados a la tarea.
        
        comentarios (List[ComentarioOut]): Comentarios registrados en la tarea.
    """

    usuarios_asignados: List[TareaUserRef] = []
    
    comentarios: List[ComentarioOut] = []

class AsignarTareaRequest(BaseModel):
    """Petición para asignar una tarea a un usuario.

    Attributes:
        
        actor_id (str): Identificador del usuario que realiza la acción.
        
        nombre_usuario (str): Nombre del usuario al que se asigna la tarea.
        
        nombre_tarea (str): Nombre de la tarea a asignar.
    """

    actor_id: str
    
    nombre_usuario: str
    
    nombre_tarea: str

class EstadisticasTareas(BaseModel):
    """Estadísticas agregadas de tareas.

    Attributes:
        
        total (int): Número total de tareas.
        
        finalizadas (int): Número de tareas en estado 'finalizada'.
        
        pendientes (int): Número de tareas en estado 'pendiente'.

        todos los campos son calculados a partir de la base de datos 
        y no se reciben en peticiones y no deben ser negativos.

    """

    total: int = Field(
        # igual o mayor que 0, ya que no puede haber un número negativo de tareas
        ge = 0, 
        
        description = "Número total de tareas, no puede ser negativo."
        )
    
    finalizadas: int = Field(
        
        ge = 0, 
        
        description="Número de tareas finalizadas, no puede ser negativo."
        )
    
    pendientes: int = Field(
        
        ge = 0, 
        
        description = "Número de tareas pendientes, no puede ser negativo.")

class EstadisticasUsuarios(BaseModel):
    """Estadísticas agregadas de usuarios.

    Attributes:
        
        total (int): Número total de usuarios.
        
        admins (int): Número de usuarios con rol 'admin'.
        
        supervisores (int): Número de usuarios con rol 'supervisor'.
        
        users (int): Número de usuarios con rol 'user'.
    """

    total: int = Field(
        ge = 0, 
        
        description = "Número total de usuarios, no puede ser negativo."
        )
    
    admins: int = Field(
        ge = 0,
        
        description = "Número de usuarios con rol 'admin', no puede ser negativo."
        )
    
    supervisores: int = Field(
        ge = 0,
        
        description = "Número de usuarios con rol 'supervisor', no puede ser negativo."
        )
    
    users: int = Field(
        ge = 0,
        
        description = "Número de usuarios con rol 'user', no puede ser negativo."
        )