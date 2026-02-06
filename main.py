import sys

# from gestor_tareas import GestorTareas
from core import GestorTareas
from interfaz_consola import InterfazConsola
from usuarios import Usuario


# ==================================================
# Flujos principales
# ==================================================

def flujo_crear_admin_inicial(ui: InterfazConsola, gestor: GestorTareas) -> None:
    ui.limpiar_pantalla()
    ui.mostrar_titulo("Configuración inicial")

    ui.mostrar_advertencia(
        "No existe ningún administrador. Debe crearse uno para continuar."
    )

    while True:
        try:
            datos = ui.pedir_datos_nuevo_usuario()
            datos["rol"] = "admin"

            if not datos.get("password"):
                ui.mostrar_error("El administrador debe tener contraseña.")
                ui.pausa()
                continue

            gestor.crear_usuario(**datos)
            ui.mostrar_exito("Administrador creado correctamente.")
            ui.pausa()
            return

        except Exception as e:
            ui.mostrar_error(str(e))
            ui.pausa()


def flujo_login(ui: InterfazConsola, gestor: GestorTareas) -> Usuario:
    intentos = 3

    while intentos > 0:
        ui.limpiar_pantalla()
        usuario, password = ui.pedir_credenciales()

        try:
            usuario_autenticado = gestor.autenticar_usuario(usuario, password)

            # Primer login sin contraseña
            if usuario_autenticado.password_hash is None:
                nueva_pwd = ui.mostrar_asistente_crear_password()
                usuario_autenticado.cambiar_password(nueva_pwd)
                ui.mostrar_exito("Contraseña configurada correctamente.")

            ui.mostrar_bienvenida(usuario_autenticado)
            ui.pausa()
            return usuario_autenticado

        except Exception as e:
            intentos -= 1
            ui.mostrar_error(str(e))
            ui.mostrar_advertencia(f"Intentos restantes: {intentos}")
            ui.pausa()

    ui.mostrar_error("Demasiados intentos fallidos. Cerrando sistema.")
    sys.exit(1)


# ==================================================
# Menús
# ==================================================

def menu_admin(
    ui: InterfazConsola,
    gestor: GestorTareas,
    usuario: Usuario,
) -> None:
    while True:
        ui.limpiar_pantalla()
        opcion = ui.mostrar_menu_admin()

        try:
            if opcion == "1":
                ui.limpiar_pantalla()
                ui.mostrar_usuarios(gestor.listar_usuarios())
                ui.pausa()

            elif opcion == "2":
                ui.limpiar_pantalla()
                datos = ui.pedir_datos_nuevo_usuario()
                gestor.crear_usuario(**datos)
                ui.mostrar_exito("Usuario creado correctamente.")
                ui.pausa()

            elif opcion == "3":
                ui.limpiar_pantalla()
                nombre = ui.pedir_usuario_para_reset()
                gestor.resetear_password_usuario(usuario, nombre)
                ui.mostrar_exito("Contraseña reseteada.")
                ui.pausa()

            elif opcion == "4":
                ui.limpiar_pantalla()
                stats = gestor.obtener_estadisticas()
                ui.mostrar_estadisticas(stats)
                ui.pausa()

            elif opcion == "0":
                return

            else:
                ui.mostrar_advertencia("Opción inválida.")
                ui.pausa()

        except (ValueError, PermissionError) as e:
            ui.mostrar_error(str(e))
            ui.pausa()
        except Exception as e:
            ui.mostrar_error(f"Error inesperado: {e}")
            ui.pausa()


def menu_supervisor(
    ui: InterfazConsola,
    gestor: GestorTareas,
    usuario: Usuario,
) -> None:
    while True:
        ui.limpiar_pantalla()
        opcion = ui.mostrar_menu_supervisor()

        try:
            if opcion == "1":
                ui.limpiar_pantalla()
                datos = ui.pedir_datos_nueva_tarea()
                tarea = gestor.crear_tarea(usuario, **datos)
                ui.mostrar_exito("Tarea creada correctamente.")
                ui.pausa()

            elif opcion == "2":
                ui.limpiar_pantalla()
                nombre_usuario = ui.pedir_usuario_destino()
                nombre_tarea = ui.pedir_tarea_a_asignar()
                gestor.asignar_usuario_tarea(
                    usuario,
                    nombre_usuario,
                    nombre_tarea,
                )
                ui.mostrar_exito("Tarea asignada correctamente.")
                ui.pausa()

            elif opcion == "0":
                return

            else:
                ui.mostrar_advertencia("Opción inválida.")
                ui.pausa()

        except (ValueError, PermissionError) as e:
            ui.mostrar_error(str(e))
            ui.pausa()


def menu_usuario(
    ui: InterfazConsola,
    gestor: GestorTareas,
    usuario: Usuario,
) -> None:
    while True:
        ui.limpiar_pantalla()
        opcion = ui.mostrar_menu_usuario()

        try:
            if opcion == "1":
                ui.limpiar_pantalla()
                tareas = gestor.obtener_tareas_de_usuario(usuario)
                ui.mostrar_tareas(tareas)
                ui.pausa()

            elif opcion == "2":
                ui.limpiar_pantalla()
                datos = ui.pedir_datos_nueva_tarea()
                tarea = gestor.crear_tarea(**datos)
                gestor.asignar_usuario_tarea(usuario.nombre, tarea.nombre)
                ui.mostrar_exito("Tarea creada y asignada.")
                ui.pausa()

            elif opcion == "3":
                ui.limpiar_pantalla()
                nombre = ui.pedir_tarea_a_finalizar()
                gestor.finalizar_tarea(nombre)
                ui.mostrar_exito("Tarea finalizada.")
                ui.pausa()

            elif opcion == "4":
                ui.limpiar_pantalla()
                ui.mostrar_perfil(usuario)
                ui.pausa()

            elif opcion == "0":
                return

            else:
                ui.mostrar_advertencia("Opción inválida.")
                ui.pausa()

        except (ValueError, PermissionError) as e:
            ui.mostrar_error(str(e))
            ui.pausa()
        except Exception as e:
            ui.mostrar_error(f"Error inesperado: {e}")
            ui.pausa()


# ==================================================
# Main
# ==================================================

def main() -> None:
    ui = InterfazConsola()
    gestor = GestorTareas()

    if not gestor.existe_admin():
        flujo_crear_admin_inicial(ui, gestor)

    while True:
        usuario_actual = flujo_login(ui, gestor)

        if usuario_actual.es_admin():
            menu_admin(ui, gestor, usuario_actual)
        elif usuario_actual.es_supervisor():
            menu_supervisor(ui, gestor, usuario_actual)
        else:
            menu_usuario(ui, gestor, usuario_actual)



if __name__ == "__main__":
    main()
