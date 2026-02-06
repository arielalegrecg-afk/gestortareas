"""Tests unitarios para los esquemas Pydantic de la API.

Este módulo contiene tests de validación para todos los modelos
definidos en api.schemas, incluyendo casos válidos e inválidos.

    como ejecutar los tests
    

    parametros:
        -v : salida detallada
        -q : salida silenciosa
        -k <expresión> : ejecutar tests que coincidan con la expresión
        -s : mostrar salida estándar durante los tests


"""

from datetime import datetime
import pytest
from pydantic import ValidationError
from api.schemas import (
    UsuarioCreate,
    UsuarioBase,
    UsuarioOut,
    EstadisticasUsuarios,
    LoginRequest,
    LoginResponse,
    TareaBase,
    TareaCreate,
    TareaOut,
    TareaDetalle,
    TareaUserRef,
    ComentarioOut,
    AsignarTareaRequest,
    EstadisticasTareas,
    
)

# ##################
# Tests de Usuario
# ##################

def test_usuario_create_valido():
    """Test de creación válida de UsuarioCreate."""

    data = {
        "nombre": "jdoe",
        
        "nombre_visible": "John Doe",
        # password opcional
        "rol": "admin",
    }

    usuario = UsuarioCreate(**data)

    assert usuario.nombre == "jdoe"
    
    assert usuario.nombre_visible == "John Doe"
    
    assert usuario.password is None
    
    assert usuario.rol == "admin"

def test_usuario_create_rol_invalido():
    """Verifica que UsuarioCreate acepta password opcional."""
    
    # Intento de crear un usuario con rol inválido
    # debe lanzar ValidationError
    with pytest.raises(ValidationError):
        UsuarioCreate(
            nombre = "jdoe",
            
            nombre_visible = "John Doe",
            
            rol = "otro",  # no permitido
        )

def test_usuario_create_con_password():
    """Verifica que UsuarioCreate acepta password opcional."""
    
    usuario = UsuarioCreate(
        nombre = "jdoe",
        
        nombre_visible = "John Doe",
        
        password = "securepass",
        
        rol = "user",
    )

    assert usuario.password == "securepass"
    assert usuario.rol == "user"

def test_usuario_create_rol_por_defecto():
    """Verifica que UsuarioCreate asigna rol por defecto."""
    
    usuario = UsuarioCreate(
        nombre = "jdoe",
        
        nombre_visible = "John Doe",
        
        password = "securepass",
    )

    assert usuario.rol == "user"  # rol por defecto

def test_usuario_base_valido():
    """Test de creación válida de UsuarioBase."""
    
    ahora = datetime.now()
    
    usuario = UsuarioBase(
        id="123",
        
        nombre="jdoe",
        
        nombre_visible="John Doe",
        
        rol="supervisor",
        
        fecha_creacion=ahora,
    )

    assert usuario.id == "123"
    
    assert usuario.nombre == "jdoe"
    
    assert usuario.rol == "supervisor"
    
    assert usuario.fecha_creacion == ahora

def test_usuario_out_hereda_de_base():
    """Verifica que UsuarioOut hereda de UsuarioBase."""
    
    ahora = datetime.now()
    
    usuario_out = UsuarioOut(
        id="123",
        
        nombre="jdoe",
        
        nombre_visible="John Doe",
        
        rol="user",
        
        fecha_creacion=ahora,
    )

    assert usuario_out.id == "123"
    
    assert usuario_out.nombre == "jdoe"
    
    assert usuario_out.rol == "user"
    
    assert usuario_out.fecha_creacion == ahora

# ##################
# TEST DE LOGIN
# ##################

def test_login_request_valido():
    """Test de creación válida de LoginRequest."""
    
    login = LoginRequest(
        nombre="jdoe",
        
        password="securepass",
    )

    assert login.nombre == "jdoe"
    
    assert login.password == "securepass"

def test_login_request_campos_requeridos():
    """Verifica que LoginRequest requiere ambos campos."""
    
    with pytest.raises(ValidationError):
        LoginRequest(
            nombre="jdoe"
            # falta password
        )
    
    with pytest.raises(ValidationError):
        LoginRequest(
            password="securepass"
            # falta nombre
        )

def test_login_response_valido():
    """Verifica LoginResponse con usuario válido."""
    ahora = datetime.now()
    
    usuario = UsuarioOut(
        id = "u1",
        nombre = "jdoe",
        nombre_visible = "John Doe",
        rol = "admin",
        fecha_creacion = ahora,
    )

    response = LoginResponse(usuario=usuario)

    assert response.usuario.nombre == "jdoe"
    
    assert response.usuario.rol == "admin"

# ##################
# TEST DE TAREA
# ##################

def test_tarea_base_valida():
    """Verifica que TareaBase acepta datos válidos."""

    ahora = datetime.now()
    
    tarea = TareaBase(
        
        nombre = "Tarea 1",
        
        descripcion = "Desc",
        
        estado = "pendiente",
        
        fecha_creacion = ahora,
    )

    assert tarea.nombre == "Tarea 1"

    assert tarea.descripcion == "Desc"
    
    assert tarea.estado == "pendiente"
    
    assert tarea.fecha_creacion == ahora

def test_tarea_base_estado_invalido():
    """Verifica que estados inválidos son rechazados."""
    
    ahora = datetime.now()
    
    with pytest.raises(ValidationError):

        TareaBase(  
            nombre = "Tarea 1",
            
            descripcion = "Desc",
            
            estado = "en_progreso",  # inválido
            
            fecha_creacion = ahora,
        )

def test_tarea_base_descripcion_opcional():
    """Verifica que descripcion es opcional en TareaBase."""
    
    ahora = datetime.now()
    
    tarea = TareaBase(
        
        nombre = "Tarea 2",
        
        estado = "finalizada",
        
        fecha_creacion = ahora,
    )

    assert tarea.nombre == "Tarea 2"
    
    assert tarea.descripcion is None
    
    assert tarea.estado == "finalizada"

    assert tarea.fecha_creacion == ahora

def test_tarea_create_minima():
    """Verifica que TareaCreate solo requiere nombre."""
    
    tarea = TareaCreate(nombre="Solo nombre")
    
    assert tarea.nombre == "Solo nombre"
    
    assert tarea.descripcion is None

def test_tarea_create_con_descripcion():
    """Verifica TareaCreate con descripción."""
    tarea = TareaCreate(
        
        nombre = "Tarea completa",
        
        descripcion = "Con descripción detallada",
    )

    assert tarea.nombre == "Tarea completa"
    
    assert tarea.descripcion == "Con descripción detallada"

def test_tarea_out_sin_usuarios():
    """Verifica TareaOut con lista de usuarios vacía."""
    ahora = datetime.now()
    
    tarea = TareaOut(
        
        nombre = "Tarea sin asignar",
        
        estado = "pendiente",
        
        fecha_creacion=ahora,
    )

    assert tarea.usuarios_asignados == []

def test_tarea_out_con_usuarios():
    """Verifica TareaOut con usuarios asignados."""
    
    ahora = datetime.now()
    
    usuario = TareaUserRef(
        
        id = "u1",
        
        nombre = "jdoe",
        
        nombre_visible = "John Doe",
        
        rol = "user",
    )

    tarea = TareaOut(
        
        nombre = "Tarea asignada",
        
        estado = "pendiente",
        
        fecha_creacion = ahora,
        
        usuarios_asignados = [usuario],
    )

    assert len(tarea.usuarios_asignados) == 1
    
    assert tarea.usuarios_asignados[0].nombre == "jdoe"

def test_tarea_detalle_completo():
    """Verifica TareaDetalle con usuarios y comentarios."""
    
    ahora = datetime.now()
    
    usuario = TareaUserRef(
        
        id="u1",
        
        nombre="jdoe",
        
        nombre_visible="John Doe",
        
        rol="user",
    )
    
    comentario = ComentarioOut(
        
        texto="Buen trabajo",
        
        autor=usuario,
        
        fecha=ahora,
    )

    tarea = TareaDetalle(
        
        nombre="Tarea detallada",
        
        estado="finalizada",
        
        fecha_creacion=ahora,
        
        usuarios_asignados=[usuario],
        
        comentarios=[comentario],
    )

    assert len(tarea.usuarios_asignados) == 1
    
    assert tarea.usuarios_asignados[0].nombre == "jdoe"
    
    assert len(tarea.comentarios) == 1
    
    assert tarea.comentarios[0].texto == "Buen trabajo" 

# #################################################
# Tests de referencias y modelos anidados
# #################################################

def test_tarea_user_ref_valido():
    """Verifica TareaUserRef con datos válidos."""
    
    usuario_ref = TareaUserRef(
        
        id = "u1",
        
        nombre = "jdoe",
        
        nombre_visible = "John Doe",
        
        rol = "supervisor",
    )

    assert usuario_ref.id == "u1"
    
    assert usuario_ref.nombre == "jdoe"
    
    assert usuario_ref.rol == "supervisor"

def test_tarea_user_ref_rol_invalido():
    """Verifica que TareaUserRef rechaza roles inválidos."""
    
    with pytest.raises(ValidationError):
        TareaUserRef(
            id = "u1",
            
            nombre = "jdoe",
            
            nombre_visible = "John Doe",
            
            rol = "invitado",  # no permitido
        )

def test_comentario_out_valido():
    """Verifica ComentarioOut con todos los campos."""
    ahora = datetime.now()
    
    autor = TareaUserRef(
        
        id = "u1",
        
        nombre = "jdoe",
        
        nombre_visible = "John Doe",
        
        rol = "user",
    )
    
    comentario = ComentarioOut(
        
        texto = "Comentario de prueba",
        
        autor = autor,
        
        fecha = ahora,
    )

    assert comentario.texto == "Comentario de prueba"
    
    assert comentario.autor.nombre == "jdoe"
    
    assert comentario.fecha == ahora

def test_comentario_out_texto_vacio():
    """Verifica que ComentarioOut acepta texto vacío."""
    
    ahora = datetime.now()
    
    autor = TareaUserRef(
        
        id = "u1",
        
        nombre = "jdoe",
        
        nombre_visible = "John Doe",
        
        rol = "user",
    )
    
    comentario = ComentarioOut(
        
        texto = "",
        
        autor = autor,
        
        fecha = ahora,
    )

    assert comentario.texto == ""

# #################################################
# Tests de peticiones de acciones
# #################################################

def test_asignar_tarea_request_valido():
    """Verifica AsignarTareaRequest con datos válidos."""
    
    request = AsignarTareaRequest(
        
        actor_id = "t1",

        nombre_usuario = "jdoe",

        nombre_tarea = "Tarea 1",
    )

    assert request.actor_id == "t1"
    
    assert request.nombre_usuario == "jdoe"
    
    assert request.nombre_tarea == "Tarea 1"

def test_asignar_tarea_request_campos_requeridos():
    """Verifica que todos los campos son obligatorios."""
    
    with pytest.raises(ValidationError):
        AsignarTareaRequest(
            actor_id = "t1",
            nombre_usuario = "jdoe",
            # falta nombre_tarea
        )
    
    with pytest.raises(ValidationError):
        AsignarTareaRequest(
            actor_id = "t1",
            nombre_tarea = "Tarea 1",
            # falta nombre_usuario
        )
    
    with pytest.raises(ValidationError):
        AsignarTareaRequest(
            nombre_usuario = "jdoe",
            nombre_tarea = "Tarea 1",
            # falta actor_id
        )

# #################################################
# Tests de EstadisticasUsuarios
# #################################################

def test_estadisticas_tareas_valido():
    """Verifica creación de EstadisticasTareas con datos válidos."""
    
    estadisticas = EstadisticasTareas(
        
        total = 20,
        
        finalizadas = 12,
        
        pendientes = 8,
    )

    assert estadisticas.total == 20
    
    assert estadisticas.finalizadas == 12
    
    assert estadisticas.pendientes == 8 

def test_estadisticas_tareas_cero():
    """Verifica EstadisticasTareas con sistema vacío."""
    estadisticas = EstadisticasTareas(
        total=0,
        finalizadas=0,
        pendientes=0,
    )

    assert estadisticas.total == 0
    assert estadisticas.finalizadas == 0
    assert estadisticas.pendientes == 0

def test_estadisticas_tareas_solo_finalizadas():
    """Verifica estadísticas con solo tareas finalizadas."""
    estadisticas = EstadisticasTareas(
        total=5,
        finalizadas=5,
        pendientes=0,
    )

    assert estadisticas.finalizadas == estadisticas.total
    assert estadisticas.pendientes == 0

def test_estadisticas_tareas_solo_pendientes():
    """Verifica estadísticas con solo tareas pendientes."""
    estadisticas = EstadisticasTareas(
        total=10,
        finalizadas=0,
        pendientes=10,
    )

    assert estadisticas.pendientes == estadisticas.total
    assert estadisticas.finalizadas == 0

def test_estadisticas_tareas_campos_requeridos():
        """Verifica que todos los campos de EstadisticasTareas son obligatorios."""
        
        with pytest.raises(ValidationError):
            EstadisticasTareas(
                total = 20,
                finalizadas = 12,
                # falta pendientes
            )
        
        with pytest.raises(ValidationError):
            EstadisticasTareas(
                total = 20,
                pendientes = 8,
                # falta finalizadas
            )
        
        with pytest.raises(ValidationError):
            EstadisticasTareas(
                finalizadas = 12,
                pendientes = 8,
                # falta total
            )   

def test_estadisticas_tareas_valores_negativos():
        """Verifica que EstadisticasTareas no acepta valores negativos."""
        
        with pytest.raises(ValidationError):
            EstadisticasTareas(
                total = -1,
                finalizadas = 12,
                pendientes = 8,
            )
        
        with pytest.raises(ValidationError):
            EstadisticasTareas(
                total = 20,
                finalizadas = -5,
                pendientes = 8,
            )
        
        with pytest.raises(ValidationError):
            EstadisticasTareas(
                total = 20,
                finalizadas = 12,
                pendientes = -3,
            )   

def test_estadisticas_tareas_tipos_invalidos():
    """Verifica que EstadisticasTareas rechaza tipos incorrectos."""
    
    with pytest.raises(ValidationError):
        EstadisticasTareas(
            
            total="diez",  # debe ser int
            
            finalizadas=3,
            
            pendientes=7,
        )
    
    with pytest.raises(ValidationError):
        EstadisticasTareas(
            total=20,
            
            finalizadas="doce",  # debe ser int
            
            pendientes=8,
        )
    with pytest.raises(ValidationError):
        EstadisticasTareas(
            
            total=20,
            
            finalizadas=12,
            
            pendientes="ocho",  # debe ser int
        )

# #################################################
# Tests de EstadisticasUsuarios
# #################################################

def test_estadisticas_usuarios_valido():
    """test de EstadisticasTareas con lista de EstadisticaUsuario."""
    
    estadisticas = EstadisticasUsuarios(
        
        total = 10,

        admins = 1,
        
        supervisores = 3,

        users = 6,
    )

    assert estadisticas.total == 10

    assert estadisticas.admins == 1
    
    assert estadisticas.supervisores == 3
    
    assert estadisticas.users == 6

def test_estadisticas_usuarios_cero():
    """Verifica EstadisticasUsuarios con sistema vacío."""
    estadisticas = EstadisticasUsuarios(
        total=0,
        admins=0,
        supervisores=0,
        users=0,
    )

    assert estadisticas.total == 0

def test_estadisticas_usuarios_solo_admins():
    """Verifica estadísticas con solo admins."""
    estadisticas = EstadisticasUsuarios(
        total=3,
        admins=3,
        supervisores=0,
        users=0,
    )

    assert estadisticas.admins == estadisticas.total

def test_estadisticas_usuarios_solo_supervisores():
    """Verifica estadísticas con solo supervisores."""
    estadisticas = EstadisticasUsuarios(
        total = 5,
        admins = 0,
        supervisores = 5,
        users = 0,
    )

    assert estadisticas.supervisores == estadisticas.total

def test_estadisticas_usuarios_solo_users():
    """Verifica estadísticas con solo users."""
    estadisticas = EstadisticasUsuarios(
        total = 20,
        admins = 0,
        supervisores = 0,
        users = 20,
    )

    assert estadisticas.users == estadisticas.total

def test_estadisticas_usuarios_campos_requeridos():
    """Verifica que todos los campos de EstadisticasUsuarios son obligatorios."""
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = 2,
            supervisores = 4,
            # falta users
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = 2,
            users = 9,
            # falta supervisores
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            supervisores = 4,
            users = 9,
            # falta admins
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            admins = 2,
            supervisores = 4,
            users = 9,
            # falta total
        )
    
def test_estadisticas_usuarios_valores_negativos():
    """Verifica que EstadisticasUsuarios no acepta valores negativos."""
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = -1,
            admins = 2,
            supervisores = 4,
            users = 9,
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = -2,
            supervisores = 4,
            users = 9,
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = 2,
            supervisores = -4,
            users = 9,
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = 2,
            supervisores = 4,
            users = -9,
        )

def test_estadisticas_usuarios_tipos_invalidos():
    """Verifica que EstadisticasUsuarios rechaza tipos incorrectos."""
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = "quince",  # debe ser int
            admins = 2,
            supervisores = 4,
            users = 9,
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = "dos",  # debe ser int
            supervisores = 4,
            users = 9,
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = 2,
            supervisores = "cuatro",  # debe ser int
            users = 9,
        )
    
    with pytest.raises(ValidationError):
        EstadisticasUsuarios(
            total = 15,
            admins = 2,
            supervisores = 4,
            users = "nueve",  # debe ser int
        )
