import json
import os
import qrcode
import cv2
from datetime import datetime
import smtplib
from email.message import EmailMessage
import tkinter
import customtkinter as ctk
from customtkinter import CTkImage

remitente = "asistencia.cocurricular@gmail.com"
contrasena = "einr soie bxtt flrs"

BD_USUARIOS = "BaseDatos.json"
BD_ASISTENCIA = "AsistenciaDatos.json"
ADMIN_DATA = "AdminData.json"

def evitar_error_focus():
    def focus_safe(*args, **kwargs):
        try:
            return original_focus(*args, **kwargs)
        except tkinter.TclError:
            pass

    original_focus = tkinter.Widget.focus
    tkinter.Widget.focus = focus_safe

def guardar_asistencia(asistencia):
    with open("asistenciadatos.json", "w", encoding="utf-8") as archivo:
        json.dump(asistencia, archivo, indent=2, ensure_ascii=False)

def guardarAdminData(admin_data):
    with open(ADMIN_DATA, "w", encoding="utf-8") as f:
        json.dump(admin_data, f, indent=2, ensure_ascii=False)

def cargarAdminData():
    try:
        with open(ADMIN_DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        data = {
            "historialAcciones": [],
            "erroresReportados": [],
            "configuracion": {
                "toleranciaAsistencia": 15,
                "porcentajeAdvertencia": 25
            }
        }
        guardarAdminData(data)
        return data     
       
def cargar_datos():
    if os.path.exists(BD_USUARIOS):
        with open(BD_USUARIOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    else:
        return {"estudiantes": [], "maestros": [], "actividades": [], "administrador": []}

def guardarCambios(datos):
    with open(BD_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)

 # Cerrar sesión
def cerrar_sesion(ventana):
    ventana.destroy()
    nuevo_login = LoginApp()
    nuevo_login.mainloop()

def cargar_asistencia():
    try:
        with open(BD_ASISTENCIA, "r", encoding="utf-8") as f:
            datos = json.load(f)
        if not isinstance(datos.get("registros"), dict):
            datos["registros"] = {}
        return datos
    except:
        return {"registros": {}}

def guardarAsistencia(asistencia):
    with open(BD_ASISTENCIA, "w", encoding="utf-8") as archivo:
        json.dump(asistencia, archivo, indent=2, ensure_ascii=False)

#crearUsuario(datos)

#editarUsuario(datos)

#eliminarUsuario(datos)

#registrarAccionAdmin(adminData, usuario, rol, accion)

#modificarPorcentajeAdvertencia(admin_data)

def enviarCorreoOutlook(destinatario, asunto, cuerpo):
    remitente = "asistencia.cocurricular@gmail.com"
    contrasena = "nwiu xriq katr alyz"

    mensaje = EmailMessage()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(remitente, contrasena)
            smtp.send_message(mensaje)
            print(f"[Correo enviado] a {destinatario}")
    except Exception as e:
        print(f"[Error al enviar correo] {e}")

def reportarError(datos, usuario, titulo, descripcion):
    nuevo_error = {
        "usuario": usuario,
        "titulo": titulo,
        "descripcion": descripcion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    adminData = cargarAdminData()

    if "erroresReportados" not in adminData:
        adminData["erroresReportados"] = []

    adminData["erroresReportados"].append(nuevo_error)
    guardarAdminData(adminData)

def reportarErrorVentana(parent, datos, usuario):
    ventana = ctk.CTkToplevel(parent)
    ventana.title("Reportar Error")
    ventana.geometry("520x500")
    ventana.configure(fg_color="#f0f8ff")  # Fondo celeste claro

    frame = ctk.CTkFrame(ventana, fg_color="white", corner_radius=20)
    frame.pack(padx=30, pady=30, fill="both", expand=True)

    # Título principal
    ctk.CTkLabel(
        frame, text="Reportar Error", font=("Arial", 22, "bold"),
        text_color="#003366"
    ).pack(pady=(20, 10))

    # Campo: Título
    ctk.CTkLabel(
        frame, text="Título del error:", font=("Arial", 14),
        text_color="#003366"
    ).pack(pady=(10, 2), anchor="w", padx=40)

    entry_titulo = ctk.CTkEntry(frame, width=400, height=35, corner_radius=8)
    entry_titulo.pack(pady=5)

    # Campo: Descripción
    ctk.CTkLabel(
        frame, text="Descripción:", font=("Arial", 14),
        text_color="#003366"
    ).pack(pady=(15, 2), anchor="w", padx=40)

    entry_desc = ctk.CTkTextbox(frame, height=150, width=400, corner_radius=8)
    entry_desc.pack(pady=5)

    # Mensaje de estado
    mensaje = ctk.CTkLabel(frame, text="", text_color="green", wraplength=450, font=("Arial", 12))
    mensaje.pack(pady=10)

    def enviar():
        titulo = entry_titulo.get().strip()
        descripcion = entry_desc.get("1.0", "end").strip()

        if not titulo or not descripcion:
            mensaje.configure(text="Completa todos los campos.", text_color="orange")
            return

        reportarError(datos, usuario, titulo, descripcion)
        mensaje.configure(text="✅ Error reportado correctamente.", text_color="green")
        ventana.after(1500, ventana.destroy)

    # Botón enviar
    ctk.CTkButton(
        frame, text="Enviar", command=enviar,
        fg_color="#007acc", hover_color="#005f99",
        corner_radius=10, width=180, height=40,
        font=("Arial", 14, "bold"), text_color="white"
    ).pack(pady=20)

def pedirHora_gui(master, mensaje="Ingresa la hora (HH:MM):"):
    ventana = VentanaHora(master, mensaje)
    master.wait_window(ventana)
    return ventana.respuesta

def mostrar_popup(parent, mensaje, titulo="Aviso"):
    popup = ctk.CTkToplevel(parent)
    popup.title(titulo)
    popup.geometry("400x200")
    popup.transient(parent)     # Se mantiene encima de la ventana principal
    popup.grab_set()            # Bloquea interacción con la ventana padre

    label = ctk.CTkLabel(popup, text=mensaje, wraplength=350)
    label.pack(pady=20)

    boton = ctk.CTkButton(popup, text="Cerrar", command=popup.destroy)
    boton.pack(pady=10)

def mostrar_popup_horario_invalido(ventana_padre):
    ventana = ctk.CTkToplevel(ventana_padre)
    ventana.title("Horario inválido")
    ventana.geometry("400x200")
    ventana.configure(fg_color="#f0f4f8")
    ventana.resizable(False, False)
    ventana.grab_set()  # Bloquea la ventana principal hasta cerrar esta

    ctk.CTkLabel(
        ventana,
        text="Horario inválido",
        font=("Arial", 20, "bold"),
        text_color="#4100cc"
    ).pack(pady=(25, 10))

    ctk.CTkLabel(
        ventana,
        text="Hoy no hay clase registrada para esta actividad.",
        font=("Arial", 14),
        text_color="#333333",
        wraplength=350,
        justify="center"
    ).pack(pady=10)

    ctk.CTkButton(
        ventana,
        text="Cerrar",
        font=("Arial", 14, "bold"),
        fg_color="#007acc",
        hover_color="#005f99",
        text_color="white",
        corner_radius=10,
        command=ventana.destroy
    ).pack(pady=20)

def escanear_qr_opencv(usuario, datos, asistencia, ventana_padre):
        detector = cv2.QRCodeDetector()
        cam = cv2.VideoCapture(0)

        while True:
            _, frame = cam.read()
            data, _, _ = detector.detectAndDecode(frame)

            if data:
                try:
                    idActividad, nombreActividad, horario_str = data.split("|", 2)
                    horario = eval(horario_str)  # ← OJO: solo si tú controlas el QR

                    hoy = datetime.now().strftime("%A")
                    hoy_esp = {
                        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
                        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
                    }.get(hoy, "")

                    """# FORZAR REGISTRO aunque el día no coincida (para pruebas)
                    primer_horario = horario[0]  # toma el primer bloque del QR
                    bloque = f'{primer_horario["dia"]} {primer_horario["inicio"]}-{primer_horario["fin"]}'
                    registrar_asistencia(usuario, idActividad, nombreActividad, bloque, asistencia, ventana_padre)
                    cam.release()
                    cv2.destroyAllWindows()
                    return {
                        "usuario": usuario,
                        "idActividad": idActividad
                    }"""

                    horarioHoy = next((h for h in horario if h["dia"] == hoy_esp), None)

                    if horarioHoy:
                        bloque = f'{horarioHoy["dia"]} {horarioHoy["inicio"]}-{horarioHoy["fin"]}'
                        registrar_asistencia(usuario, idActividad, nombreActividad, bloque, asistencia, ventana_padre)
                        cam.release()
                        cv2.destroyAllWindows()
                        return {
                            "usuario": usuario,
                            "idActividad": idActividad
                        }
                    else:
                        mostrar_popup_horario_invalido(ventana_padre)
                        break

                except Exception as e:
                    mostrar_popup(ventana_padre, f"Error al procesar el QR:\n{e}", "Error")
                    break

            cv2.imshow("Escáner QR", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        cam.release()
        cv2.destroyAllWindows()
        return False

# Interfaz gráfica básica con espacio para el logo y login

class AlumnoApp(ctk.CTkToplevel):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.master = master
        self.title("Menú Alumno")
        self.geometry("700x700")
        self.usuario = usuario
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        self.datos = cargar_datos()
        self.asistencia = cargar_asistencia()

        self.configure(fg_color="#e6f2ff")  # Fondo celeste claro

        self.frame_contenedor = ctk.CTkFrame(self, fg_color="#d0e7ff", corner_radius=20)
        self.frame_contenedor.pack(padx=30, pady=30, fill="both", expand=True)

        # Contenedor horizontal para texto + avatar
        bienvenida_frame = ctk.CTkFrame(self.frame_contenedor, fg_color="transparent")
        bienvenida_frame.pack(pady=15)

        ctk.CTkLabel(
            bienvenida_frame,
            text=f"Bienvenido, {usuario}",
            font=("Arial", 22, "bold"),
            text_color="#003366"
        ).pack(side="left", padx=10)

        avatar_btn = ctk.CTkButton(
            bienvenida_frame,
            text="👤",  # o usa una imagen
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#0066cc",
            hover_color="#004c99",
            text_color="white",
            font=("Arial", 18, "bold"),
            command=self.mostrar_perfil_estudiante
        )
        avatar_btn.pack(side="left")


        self.frame_menu = ctk.CTkFrame(self.frame_contenedor, fg_color="transparent")
        self.frame_menu.pack(pady=10)

        self.boton1 = ctk.CTkButton(
            self.frame_menu, text="1. Ver actividades inscritas", command=self.ver_actividades,
            fg_color="white", text_color="#003366", hover_color="#b3d9ff",
            corner_radius=15, width=300, height=40, font=("Arial", 14, "bold")
        )
        self.boton1.pack(pady=6)

        self.boton2 = ctk.CTkButton(
            self.frame_menu, text="2. Inscribirse en nueva actividad", command=self.inscribirse_actividad,
            fg_color="white", text_color="#003366", hover_color="#b3d9ff",
            corner_radius=15, width=300, height=40, font=("Arial", 14, "bold")
        )
        self.boton2.pack(pady=6)

        self.crear_botones_extra_alumno()

        self.boton_cerrar = ctk.CTkButton(
            self.frame_contenedor, text="Cerrar sesión", command=self.cerrar_aplicacion,
            fg_color="#0066cc", text_color="white", hover_color="#004c99",
            corner_radius=12, width=300, height=45, font=("Arial", 15, "bold")
        )
        self.boton_cerrar.pack(pady=(20, 10))

    def crear_botones_extra_alumno(self):
        botones = [
            ("3. Tablero de noticias", self.tablero_noticias),
            ("4. Historial de asistencia", self.historial_asistencia),
            ("5. Activar notificaciones", self.activar_notificaciones),
            ("6. Notificar errores", self.notificar_errores),
            ("7. Escanear QR para asistencia", self.mostrar_ventana_escanear_qr),
        ]

        for texto, comando in botones:
            ctk.CTkButton(
                self.frame_menu,
                text=texto,
                command=comando,
                fg_color="white", 
                text_color="#003366", 
                hover_color="#b3d9ff",
                corner_radius=15, 
                width=300, 
                height=40, 
                font=("Arial", 14, "bold")
            ).pack(pady=6)

    def mostrar_perfil_estudiante(self):
        estudiante = next((e for e in self.datos["estudiantes"] if e["usuario"] == self.usuario), None)
        asistencia = cargar_asistencia()

        if not estudiante:
            self.popup("Estudiante no encontrado.")
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("🎓 Perfil del Estudiante")
        ventana.geometry("650x540")
        ventana.configure(fg_color="#f5faff")

        frame = ctk.CTkFrame(ventana, fg_color="white", corner_radius=15)
        frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Título principal
        ctk.CTkLabel(
            frame, text="🧾 Perfil del Estudiante", font=("Arial", 24, "bold"),
            text_color="#003366"
        ).pack(pady=(20, 10))

        # Info básica del estudiante
        info = (
            f"👤 Nombre: {estudiante['usuario']}\n"
            f"🎓 Carnet: {estudiante['carnet']}\n"
            f"📧 Correo: {estudiante['correo']}\n"
            f"📚 Carrera: {estudiante['carrera']}"
        )
        ctk.CTkLabel(
            frame, text=info, font=("Arial", 14), justify="left", text_color="#003366"
        ).pack(pady=(0, 15), anchor="w", padx=30)

        # Mostrar actividades inscritas
        ctk.CTkLabel(
            frame, text="📝 Actividades Inscritas:", font=("Arial", 15, "bold"),
            text_color="#003366", anchor="w"
        ).pack(pady=(10, 5), anchor="w", padx=50)

        for act in estudiante.get("actividadesInscritas", []):
            actividad = next(
                (a for a in self.datos.get("actividades", []) + self.datos.get("actividadesFinalizadas", [])
                if a["idActividad"] == act["idActividad"]),
                None
            )
            if actividad:
                estado = actividad.get("estado", "Desconocido")
                sesiones = asistencia["registros"].get(actividad["idActividad"], {}).get("sesiones", {})
                total_asistencias = sum(
                    1 for lista in sesiones.values() for reg in lista if reg["usuario"] == self.usuario
                )

                texto = (
                    f"📍 Actividad: {actividad['nombreActividad']}\n"
                    f"   • Estado: {estado.capitalize()}\n"
                    f"   • Asistencias: {total_asistencias}"
                )
                ctk.CTkLabel(
                    frame, text=texto, font=("Arial", 13),
                    justify="left", anchor="w", text_color="#333333"
                ).pack(pady=8, anchor="w", padx=50)

        # ✅ Mostrar progreso real basado en actividadesCompletadas
        completadas = estudiante.get("actividadesCompletadas", [])
        cantidad_completadas = len(completadas)

        ctk.CTkLabel(
            frame,
            text=f"✅ Has finalizado {cantidad_completadas} de las 3 actividades requeridas para graduarte.",
            font=("Arial", 13, "bold"), text_color="#004080",
            wraplength=550, justify="left"
        ).pack(pady=(0, 20), anchor="w", padx=50)


    def tablero_noticias(self):
        datos = self.datos
        noticias = datos.get("noticias", [])

        ventana = ctk.CTkToplevel(self)
        ventana.title("Tablero de Noticias")
        ventana.geometry("800x500")
        ventana.configure(fg_color="#e6f2ff")

        frame_contenedor = ctk.CTkFrame(ventana, fg_color="#d0e7ff", corner_radius=20)
        frame_contenedor.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            frame_contenedor,
            text="📢 Tablero de Noticias",
            font=("Arial", 22, "bold"),
            text_color="#003366"
        ).pack(pady=(10, 5))

        scroll = ctk.CTkScrollableFrame(frame_contenedor, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        if not noticias:
            ctk.CTkLabel(
                scroll,
                text="No hay noticias disponibles.",
                font=("Arial", 14),
                text_color="#003366"
            ).pack(pady=10)
        else:
            for noticia in noticias:
                tarjeta = ctk.CTkFrame(scroll, fg_color="white", corner_radius=15)
                tarjeta.pack(fill="x", padx=5, pady=8)

                texto = (
                    f"📝 Título: {noticia.get('titulo', 'Sin título')}\n"
                    f"📄 Descripción: {noticia.get('descripcion', 'Sin descripción')}\n"
                    f"📅 Fecha: {noticia.get('fecha', 'Sin fecha')}\n"
                    f"👤 Publicado por: {noticia.get('remitente', 'Anónimo')}"
                )

                ctk.CTkLabel(
                    tarjeta,
                    text=texto,
                    anchor="w",
                    justify="left",
                    text_color="#003366",
                    font=("Arial", 13)
                ).pack(padx=(15, 5), pady=(8, 5), anchor="w")

    def activar_notificaciones(self):
        estudiante = next((e for e in self.datos["estudiantes"] if e["usuario"] == self.usuario), None)

        if not estudiante:
            self.popup("Estudiante no encontrado.")
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Activar Notificaciones")
        ventana.geometry("450x250")
        ventana.configure(fg_color="#e6f2ff")

        # Frame elegante
        frame = ctk.CTkFrame(ventana, fg_color="white", corner_radius=20)
        frame.pack(expand=True, padx=30, pady=30, fill="both")

        ctk.CTkLabel(
            frame,
            text="🔔 ¿Deseas activar las notificaciones?",
            font=("Arial", 17, "bold"),
            text_color="#003366"
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            frame,
            text="Estas pueden incluir recordatorios por correo",
            font=("Arial", 13),
            text_color="#003366"
        ).pack(pady=(0, 20))

        def confirmar(opcion):
            if opcion == "si":
                estudiante["notificaciones"] = True
                mensaje = "✅ Notificaciones activadas."
            elif opcion == "no":
                estudiante["notificaciones"] = False
                mensaje = "🔕 Notificaciones desactivadas."
            else:
                mensaje = "❌ Opción no válida."

            guardarCambios(self.datos)
            ventana.destroy()
            self.after(100, lambda: self.popup(mensaje))

        contenedor_botones = ctk.CTkFrame(frame, fg_color="transparent")
        contenedor_botones.pack(pady=10)

        ctk.CTkButton(
            contenedor_botones, text="Sí",
            fg_color="#0066cc", hover_color="#004c99",
            text_color="white", font=("Arial", 14),
            corner_radius=12, width=100, height=35,
            command=lambda: confirmar("si")
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            contenedor_botones, text="No",
            fg_color="#cccccc", hover_color="#999999",
            text_color="#003366", font=("Arial", 14),
            corner_radius=12, width=100, height=35,
            command=lambda: confirmar("no")
        ).pack(side="left", padx=20)

    def notificar_errores(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Notificar Error")
        ventana.geometry("520x430")
        ventana.configure(fg_color="#d6ecff")  # Celeste de fondo general

        # Contenedor blanco centrado
        frame = ctk.CTkFrame(ventana, fg_color="white", corner_radius=20)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Título del formulario
        ctk.CTkLabel(
            frame,
            text="📌 Reportar un Error",
            font=("Arial", 22, "bold"),
            text_color="#003366"
        ).pack(pady=(15, 10))

        # Campo de título del error
        ctk.CTkLabel(
            frame,
            text="Título del error:",
            text_color="#004080",
            font=("Arial", 14),
            anchor="w"
        ).pack(padx=20, anchor="w")

        entrada_titulo = ctk.CTkEntry(frame, width=420, height=35, corner_radius=10, border_width=1)
        entrada_titulo.pack(pady=5)

        # Campo de descripción
        ctk.CTkLabel(
            frame,
            text="Descripción del error:",
            text_color="#004080",
            font=("Arial", 14),
            anchor="w"
        ).pack(padx=20, pady=(10, 0), anchor="w")

        entrada_descripcion = ctk.CTkTextbox(frame, height=150, width=420, corner_radius=10, border_width=1)
        entrada_descripcion.pack(pady=5)

        # Botón para enviar
        def enviar():
            titulo = entrada_titulo.get().strip()
            descripcion = entrada_descripcion.get("1.0", "end").strip()

            if not titulo or not descripcion:
                self.popup("Por favor, completa todos los campos.")
                return

            reportarError(self.datos, self.usuario, titulo, descripcion)
            guardarCambios(self.datos)
            ventana.destroy()
            self.after(100, lambda: self.popup("✅ Error reportado exitosamente."))

        ctk.CTkButton(
            frame,
            text="Enviar reporte",
            command=enviar,
            fg_color="#007acc",  # Azul fuerte
            hover_color="#005f99",  # Azul oscuro
            text_color="white",
            font=("Arial", 14, "bold"),
            width=160,
            height=40,
            corner_radius=12
        ).pack(pady=20)


    def historial_asistencia(self):
        asistencia = cargar_asistencia()
        datos = self.datos
        estudiante = next((e for e in datos["estudiantes"] if e["usuario"] == self.usuario), None)

        ventana = ctk.CTkToplevel(self)
        ventana.title("Historial de Asistencia")
        ventana.geometry("700x500")
        ventana.configure(fg_color="#e6f2ff")

        ctk.CTkLabel(
            ventana,
            text="📊 Historial de Asistencia",
            font=("Arial", 20, "bold"),
            text_color="#003366"
        ).pack(pady=(15, 5))

        scroll = ctk.CTkScrollableFrame(ventana, fg_color="#e6f2ff")
        scroll.pack(fill="both", expand=True, padx=20, pady=10)

        if not estudiante:
            ctk.CTkLabel(
                scroll,
                text="⚠ Estudiante no encontrado.",
                font=("Arial", 14),
                text_color="#cc0000"
            ).pack(pady=20)
            return

        tiene_registros = False

        for idActividad, registro in asistencia.get("registros", {}).items():
            verificarAdvertenciaAsistencia(self.usuario, idActividad, datos, asistencia, mostrar_ventana=self)

            actividadInfo = next((a for a in datos["actividades"] if a["idActividad"] == idActividad), None)
            if not actividadInfo:
                continue

            asistencias = sum(
                1 for lista in registro.get("sesiones", {}).values()
                for r in lista if r["usuario"] == self.usuario
            )

            faltas = registro.get("faltas", {}).get(self.usuario, [])
            canceladas = registro.get("canceladas", [])
            faltas_validas = [f for f in faltas if f not in canceladas]
            total_sesiones = asistencias + len(faltas_validas)

            if total_sesiones == 0:
                continue

            tiene_registros = True
            porcentaje = (asistencias / total_sesiones) * 100

            texto = (
                f"🎯 Actividad: {actividadInfo['nombreActividad']}\n"
                f"✅ Asistencias: {asistencias}\n"
                f"❌ Faltas válidas: {len(faltas_validas)}\n"
                f"📅 Total de sesiones: {total_sesiones}\n"
                f"📈 Porcentaje de asistencia: {porcentaje:.1f}%"
            )

            tarjeta = ctk.CTkFrame(scroll, fg_color="white", corner_radius=15)
            tarjeta.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                tarjeta,
                text=texto,
                anchor="w",
                justify="left",
                text_color="#003366",
                font=("Arial", 13)
            ).pack(padx=10, pady=10)

        if not tiene_registros:
            ctk.CTkLabel(
                scroll,
                text="🔍 No se encontraron registros de asistencia.",
                font=("Arial", 14),
                text_color="#003366"
            ).pack(pady=30)

    def cerrar_aplicacion(self):
        self.destroy()
        self.master.deiconify()  # Vuelve a mostrar el login

    def ver_actividades(self):
        estudiante = next((e for e in self.datos["estudiantes"] if e["usuario"] == self.usuario), None)
        if not estudiante or not estudiante["actividadesInscritas"]:
            self.popup("No estás inscrito en ninguna actividad.")
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Actividades Inscritas")
        ventana.geometry("800x600")
        ventana.configure(fg_color="#e6f2ff")

        # Título
        ctk.CTkLabel(
            ventana,
            text="Actividades Inscritas",
            font=("Arial", 20, "bold"),
            text_color="#003366"
        ).pack(pady=(15, 5))

        scroll_frame = ctk.CTkScrollableFrame(ventana, fg_color="#e6f2ff")
        scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        for act in estudiante["actividadesInscritas"]:
            actividad = next((a for a in self.datos["actividades"] if a["idActividad"] == act["idActividad"]), None)
            if actividad:
                frame = ctk.CTkFrame(scroll_frame, fg_color="white", corner_radius=20)
                frame.pack(padx=10, pady=15, fill="x", expand=True)

                # Nombre en negrita
                ctk.CTkLabel(frame, text=f"{actividad['nombreActividad']} ({actividad['categoria']})",
                            anchor="w", justify="left", text_color="#003366",
                            font=("Arial", 14, "bold")).pack(padx=15, pady=(10, 2), anchor="w")

                info = (
                    f"Encargado: {actividad['personaEncargada']}\n"
                    f"Lugar: {actividad['lugar']}\n"
                    f"Detalles: {actividad['detalles']}\n"
                    f"Estado: {actividad['estado']}\n"
                    f"Horario:"
                )

                ctk.CTkLabel(frame, text=info, anchor="w", justify="left",
                            text_color="#003366", font=("Arial", 13)).pack(padx=15, anchor="w")

                for h in actividad["horario"]:
                    ctk.CTkLabel(frame, text=f"- {h['dia']} de {h['inicio']} a {h['fin']}",
                                anchor="w", justify="left", text_color="#003366", font=("Arial", 13)).pack(padx=25, anchor="w")

    def inscribirse_actividad(self):
        estudiante = next((e for e in self.datos["estudiantes"] if e["usuario"] == self.usuario), None)

        if not estudiante:
            self.popup("Estudiante no encontrado.")
            return

        inscritasIds = [a["idActividad"] for a in estudiante["actividadesInscritas"]]
        disponibles = [a for a in self.datos["actividades"]
                    if a["idActividad"] not in inscritasIds and a["estado"].lower() == "activa"]

        if not disponibles:
            self.popup("✅ Ya estás inscrito en todas las actividades activas.")
            return

        ventana = ctk.CTkToplevel(self)
        ventana.title("Actividades Disponibles")
        ventana.geometry("800x600")
        ventana.configure(fg_color="#e6f2ff")

        ctk.CTkLabel(ventana, text="Actividades Disponibles",
                    font=("Arial", 20, "bold"), text_color="#003366").pack(pady=(15, 5))

        frame_scroll = ctk.CTkScrollableFrame(ventana, fg_color="#e6f2ff")
        frame_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        for actividad in disponibles:
            frame = ctk.CTkFrame(frame_scroll, fg_color="white", corner_radius=20)
            frame.pack(padx=10, pady=15, fill="x", expand=True)

            ctk.CTkLabel(frame,
                        text=f"{actividad['nombreActividad']} ({actividad['categoria']})",
                        anchor="w", justify="left",
                        font=("Arial", 14, "bold"), text_color="#003366").pack(padx=15, pady=(10, 2), anchor="w")

            info = (
                f"Encargado: {actividad['personaEncargada']}\n"
                f"Detalles: {actividad['detalles']}\n"
                f"Cupos disponibles: {actividad['cuposMaximos'] - len(actividad.get('inscritos', []))}"
            )

            ctk.CTkLabel(frame, text=info, anchor="w", justify="left",
                        font=("Arial", 13), text_color="#003366").pack(padx=15, anchor="w")

            ctk.CTkButton(
                frame, text="Inscribirse",
                fg_color="#0066cc", hover_color="#004c99", text_color="white",
                corner_radius=12, font=("Arial", 13, "bold"),
                width=120, height=35,
                command=lambda a=actividad: self.confirmar_inscripcion(a, ventana)
            ).pack(pady=10, padx=15, anchor="e")

    def confirmar_inscripcion(self, actividad, ventana_padre):
        respuesta = ctk.CTkInputDialog(text=f"¿Confirmas inscribirte a:\n{actividad['nombreActividad']}?", title="Confirmación")
        if respuesta.get_input() is not None:
            estudiante = next((e for e in self.datos["estudiantes"] if e["usuario"] == self.usuario), None)
            if estudiante:
                estudiante["actividadesInscritas"].append({
                    "idActividad": actividad["idActividad"]
                })
                actividad.setdefault("inscritos", []).append(self.usuario)
                guardarCambios(self.datos)
                self.popup("✅ ¡Inscripción realizada con éxito!")
                ventana_padre.destroy()

    def inscribirse(self, actividad, ventana):
        estudiante = next((e for e in self.datos["estudiantes"] if e["usuario"] == self.usuario), None)
        if any(a["idActividad"] == actividad["idActividad"] for a in estudiante["actividadesInscritas"]):
            self.popup("Ya estás inscrito en esta actividad.")
            return

        estudiante["actividadesInscritas"].append({
            "idActividad": actividad["idActividad"],
            "nombreActividad": actividad["nombreActividad"]
        })
        actividad.setdefault("inscritos", []).append(self.usuario)

        guardarCambios(self.datos)
        self.popup(f"Inscripción exitosa en {actividad['nombreActividad']}.")
        ventana.destroy()

    def escanear_qr_opencv(usuario, datos, asistencia, ventana_padre):
        detector = cv2.QRCodeDetector()
        cam = cv2.VideoCapture(0)

        while True:
            _, frame = cam.read()
            data, _, _ = detector.detectAndDecode(frame)

            if data:
                try:
                    idActividad, nombreActividad, horario_str = data.split("|", 2)
                    horario = eval(horario_str)  # ← solo si tú generas el QR

                    # Ignorar validación de día y tomar siempre el primer horario
                    primer_horario = horario[0]
                    bloque = f'{primer_horario["dia"]} {primer_horario["inicio"]}-{primer_horario["fin"]}'

                    # Registrar asistencia directamente
                    registrar_asistencia(usuario, idActividad, nombreActividad, bloque, asistencia, ventana_padre)
                    cam.release()
                    cv2.destroyAllWindows()
                    return {"usuario": usuario, "idActividad": idActividad}

                except Exception as e:
                    mostrar_popup(ventana_padre, f"Error al procesar el QR:\n{e}", "Error")
                    cam.release()
                    cv2.destroyAllWindows()
                    return False


            cv2.imshow("Escáner QR", frame)
            if cv2.waitKey(1) == ord("q"):
                break

        cam.release()
        cv2.destroyAllWindows()
        return False

    def popup(self, mensaje):
            ventana = ctk.CTkToplevel(self)
            ventana.title("Mensaje")
            ventana.geometry("400x150")
            ctk.CTkLabel(ventana, text=mensaje).pack(pady=20)
            ctk.CTkButton(ventana, text="OK", command=ventana.destroy).pack(pady=10)

    def escanearQR_asistencia_gui(self):
        estudiante = next((e for e in self.datos["estudiantes"] if e["usuario"] == self.usuario), None)

        if not estudiante:
            mostrar_popup(self, "Estudiante no encontrado.", "Error")
            return

        resultado = escanear_qr_opencv(self.usuario, self.datos, self.asistencia, self)

        if not isinstance(resultado, dict):
            return

        idActividad = resultado.get("idActividad")

        if idActividad:
            verificarAdvertenciaAsistencia(self.usuario, idActividad, self.datos, self.asistencia, self)
            guardarAsistencia(self.asistencia)
            guardarCambios(self.datos)
            mostrar_popup(self, "Asistencia registrada correctamente.", "Registro exitoso")
        else:
            mostrar_popup(self, "El QR no contiene un ID de actividad válido.", "QR inválido")

    def mostrar_ventana_escanear_qr(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Escanear Código QR")
        ventana.geometry("600x420")
        ventana.configure(fg_color="#e6f2ff")

        ctk.CTkLabel(
            ventana,
            text="📸 Escanear Código QR",
            font=("Arial", 22, "bold"),
            text_color="#003366"
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            ventana,
            text="Escanea el código proporcionado por tu docente\n"
                "para registrar tu asistencia automáticamente.",
            font=("Arial", 14),
            text_color="#003366",
            justify="center"
        ).pack(pady=10)

        # Al presionar, cierra esta ventana y llama al escaneo real
        ctk.CTkButton(
            ventana,
            text="Iniciar Escaneo",
            font=("Arial", 14, "bold"),
            fg_color="#0066cc",
            hover_color="#004c99",
            text_color="white",
            corner_radius=10,
            width=160,
            height=40,
            command=lambda: [ventana.destroy(), self.escanearQR_asistencia_gui()]
        ).pack(pady=25)

        # Frame decorativo de cámara
        cam_frame = ctk.CTkFrame(ventana, width=400, height=200, fg_color="white", corner_radius=15)
        cam_frame.pack(pady=10)
        ctk.CTkLabel(cam_frame, text="(Vista previa de la cámara aquí)", text_color="#666666").place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(ventana, text="Cancelar", command=ventana.destroy).pack(pady=10)

# ────── FUNCIONES ADICIONALES ADMINISTRATIVAS ──────

class GestionUsuarios(ctk.CTkToplevel):
    def __init__(self, datos):
        super().__init__()
        self.title("Gestión de Usuarios")
        self.geometry("600x600")
        self.datos = datos

        self.opciones = ["Alumno", "Docente", "Administrador"]
        self.tipo = ctk.CTkComboBox(self, values=self.opciones)
        self.tipo.set("Alumno")
        self.tipo.pack(pady=5)

        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Nombre de usuario")
        self.usuario_entry.pack(pady=5)

        self.contra_entry = ctk.CTkEntry(self, placeholder_text="Contraseña")
        self.contra_entry.pack(pady=5)

        self.correo_entry = ctk.CTkEntry(self, placeholder_text="Correo electrónico")
        self.correo_entry.pack(pady=5)

        self.extra_entries = []
        self.extra_labels = []

        self.tipo.bind("<FocusOut>", lambda e: self.actualizar_campos_extra())
        self.actualizar_campos_extra()

        self.btn_crear = ctk.CTkButton(self, text="Crear Usuario", command=self.crear_usuario)
        self.btn_crear.pack(pady=10)

    def actualizar_campos_extra(self):
        for widget in self.extra_entries + self.extra_labels:
            widget.destroy()
        self.extra_entries.clear()
        self.extra_labels.clear()

        tipo = self.tipo.get()
        campos = []

        if tipo == "Alumno":
            campos = ["Carnet", "ID del estudiante", "Carrera"]
        elif tipo == "Docente":
            campos = ["ID del docente", "Rol"]
        elif tipo == "Administrador":
            campos = ["ID del administrador", "Cargo"]

        for campo in campos:
            lbl = ctk.CTkLabel(self, text=campo)
            lbl.pack()
            entry = ctk.CTkEntry(self)
            entry.pack(pady=2)
            self.extra_labels.append(lbl)
            self.extra_entries.append(entry)

    def crear_usuario(self):
        tipo = self.tipo.get()
        usuario = self.usuario_entry.get()
        contrasena = self.contra_entry.get()
        correo = self.correo_entry.get()

        if tipo == "Alumno":
            carnet, idEstudiante, carrera = [e.get() for e in self.extra_entries]
            nuevo = {
                "tipoUsuario": tipo,
                "usuario": usuario,
                "contrasena": contrasena,
                "carnet": carnet,
                "idEstudiante": idEstudiante,
                "correo": correo,
                "carrera": carrera,
                "notificaciones": False,
                "actividadesInscritas": []
            }
            self.datos["estudiantes"].append(nuevo)

        elif tipo == "Docente":
            idDocente, rol = [e.get() for e in self.extra_entries]
            nuevo = {
                "tipoUsuario": tipo,
                "usuario": usuario,
                "contrasena": contrasena,
                "idMaestro": idDocente,
                "correo": correo,
                "rol": rol
            }
            self.datos["maestros"].append(nuevo)

        elif tipo == "Administrador":
            idAdmin, cargo = [e.get() for e in self.extra_entries]
            nuevo = {
                "tipoUsuario": tipo,
                "usuario": usuario,
                "contrasena": contrasena,
                "idAdministrador": idAdmin,
                "correo": correo,
                "cargoAdministrativo": cargo
            }
            self.datos["administrador"].append(nuevo)

        guardarCambios(self.datos)
        aviso = ctk.CTkToplevel(self)
        aviso.geometry("300x150")
        aviso.title("Éxito")
        ctk.CTkLabel(aviso, text=f"Usuario {usuario} ({tipo}) creado con éxito").pack(pady=20)
        ctk.CTkButton(aviso, text="OK", command=aviso.destroy).pack(pady=10)
        self.destroy()

# ────── VENTANA PARA PEDIR HORA ──────

class VentanaHora(ctk.CTkToplevel):
    def __init__(self, master, mensaje):
        super().__init__(master)
        self.title("Ingresar hora")
        self.geometry("350x200")
        self.respuesta = None
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text=mensaje).pack(pady=10)
        self.entrada = ctk.CTkEntry(self, placeholder_text="Ejemplo: 10:30")
        self.entrada.pack(pady=5)

        self.mensaje = ctk.CTkLabel(self, text="", text_color="red")
        self.mensaje.pack()

        ctk.CTkButton(self, text="Aceptar", command=self.validar).pack(pady=10)

    def validar(self):
        hora = self.entrada.get().strip()
        if ":" not in hora:
            self.mensaje.configure(text="Debe contener ':' como en 10:00.")
            return
        partes = hora.split(":")
        if len(partes) != 2 or not all(p.isdigit() for p in partes):
            self.mensaje.configure(text="Formato inválido. Usa HH:MM.")
            return
        h, m = map(int, partes)
        if 0 <= h <= 23 and 0 <= m <= 59:
            self.respuesta = f"{h:02d}:{m:02d}"
            self.destroy()
        else:
            self.mensaje.configure(text="Horas entre 00-23 y minutos entre 00-59.")

def inscribirEstudiante_gui(master, usuario, datos, guardarCambios):
    actividades_disponibles = [a for a in datos["actividades"] if a["estado"] == "activa"]
    estudiante = next((e for e in datos["estudiantes"] if e["usuario"] == usuario), None)

    if not actividades_disponibles or not estudiante:
        print("[Error] No hay actividades disponibles o estudiante no encontrado.")
        return

    ventana = ctk.CTkToplevel(master)
    ventana.title("Inscribirse en Actividad")
    ventana.geometry("500x400")

    lista = ctk.CTkScrollableFrame(ventana)
    lista.pack(pady=10, fill="both", expand=True)

    for actividad in actividades_disponibles:
        if any(a["idActividad"] == actividad["idActividad"] for a in estudiante["actividadesInscritas"]):
            continue

        frame = ctk.CTkFrame(lista)
        frame.pack(padx=10, pady=5, fill="x")

        ctk.CTkLabel(frame, text=f"{actividad['nombreActividad']} ({actividad['categoria']})").pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Inscribirse", command=lambda a=actividad: master.confirmar_inscripcion(a, ventana)).pack(side="right", padx=5)


def mostrar_inscripciones_gui(master, datos):
    ventana = ctk.CTkToplevel(master)
    ventana.title("Inscripciones por Actividad")
    ventana.geometry("600x500")

    for act in datos["actividades"]:
        if act["estado"].lower() != "activa":
            continue

        inscritos = [
            e["usuario"]
            for e in datos["estudiantes"]
            if any(a["idActividad"] == act["idActividad"] for a in e.get("actividadesInscritas", []))
        ]

        frame = ctk.CTkFrame(ventana)
        frame.pack(pady=5, fill="x")
        ctk.CTkLabel(frame, text=f"{act['nombreActividad']} ({len(inscritos)} inscritos)", font=("Arial", 14)).pack()

        for i, est in enumerate(inscritos, 1):
            ctk.CTkLabel(frame, text=f"{i}. {est}").pack()

def mostrarQR_gui(master, usuario, datos):
    user_obj = next((u for u in datos["estudiantes"] + datos["maestros"] if u["usuario"] == usuario), None)
    if not user_obj or "qrGenerado" not in user_obj:
        print("[Error] QR no encontrado para este usuario.")
        return

    ruta = user_obj["qrGenerado"]
    if not os.path.exists(ruta):
        print("[Error] Archivo QR no existe.")
        return

    os.system(f'start {ruta}' if os.name == 'nt' else f'xdg-open "{ruta}"')

def buscarActividadHistorial_gui(master, datos, asistencia):
    ventana = ctk.CTkToplevel(master)
    ventana.title("Buscar Actividad")
    ventana.geometry("500x400")

    entrada = ctk.CTkEntry(ventana, placeholder_text="Buscar por nombre, categoría u horario")
    entrada.pack(pady=10)

    resultado = ctk.CTkLabel(ventana, text="")
    resultado.pack()

    def buscar():
        nombre = entrada.get().lower()
        for actividad in datos["actividades"]:
            if nombre in actividad["nombreActividad"].lower() or nombre in actividad["idActividad"].lower():
                sesiones = asistencia["registros"].get(actividad["idActividad"], {}).get("sesiones", {})
                texto = f"Actividad: {actividad['nombreActividad']}\nEncargado: {actividad['personaEncargada']}\nDetalles: {actividad['detalles']}\nCupos: {len(actividad.get('inscritos', []))}/{actividad['cuposMaximos']}\n\n"
                for usuario in actividad.get("inscritos", []):
                    total = sum(1 for lista in sesiones.values() for r in lista if r["usuario"] == usuario)
                    texto += f"{usuario}: {total} asistencias\n"
                resultado.configure(text=texto)
                return
        resultado.configure(text="No se encontró la actividad.")

    ctk.CTkButton(ventana, text="Buscar", command=buscar).pack(pady=5)

def registrar_falta_gui(usuario, idActividad, fechaHoy):
    try:
        with open("asistenciadatos.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except Exception as e:
        print(f"[Error] No se pudo cargar el archivo de asistencia: {e}")
        return

    actividad = datos["registros"].get(idActividad)
    if not actividad:
        print(f"[Info] Actividad no encontrada: {idActividad}")
        return

    if fechaHoy in actividad.get("canceladas", []):
        print(f"[Info] Clase cancelada el {fechaHoy}, no se registra falta.")
        return

    actividad.setdefault("faltas", {})
    faltasUsuario = actividad["faltas"].setdefault(usuario, [])

    if fechaHoy not in faltasUsuario:
        faltasUsuario.append(fechaHoy)
        print(f"[Registrado] Falta registrada para {usuario} el {fechaHoy}.")
    else:
        print("[Duplicado] La falta ya estaba registrada para hoy.")

    with open("asistenciadatos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)
def confirmar_finalizacion(actividad, usuario, datos, guardarCambios, cargarAdminData, guardarAdminData, enviarCorreoOutlook, ventana):
    actividad["estado"] = "Finalizada"
    guardarCambios(datos)

    adminData = cargarAdminData()
    adminData.setdefault("historialAcciones", []).append({
        "usuario": usuario,
        "rol": "Docente",
        "accion": f"Finalizó la actividad '{actividad['nombreActividad']}'",
        "fechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    guardarAdminData(adminData)

    for usuarioEst in actividad.get("inscritos", []):
        estudiante = next((e for e in datos["estudiantes"] if e["usuario"] == usuarioEst), None)
        if estudiante:
            try:
                print(f"Intentando enviar correo a {estudiante['correo']}...")
                enviarCorreoOutlook(
                    destinatario=estudiante["correo"],
                    asunto=f"Actividad finalizada: {actividad['nombreActividad']}",
                    cuerpo=f"Hola {usuarioEst},\nLa actividad '{actividad['nombreActividad']}' ha sido finalizada. ¡Gracias por participar!"
                )
                print(f"Correo enviado a {estudiante['correo']}")
            except Exception as e:
                print(f"Error enviando correo a {estudiante['correo']}: {e}")

    print(f"[Finalizado] Actividad '{actividad['nombreActividad']}' finalizada.")
    ventana.destroy()

# Funciones gráficas
class DocenteFunciones:
    def __init__(self, master, datos, asistencia, usuario):
        self.master = master
        self.datos = datos
        self.asistencia = asistencia
        self._usuario = usuario


    def mostrar_perfil_docente(self):
        docente = next((m for m in self.datos["maestros"] if m["usuario"] == self._usuario), None)

        if not docente:
            self.master.popup("No se encontró el perfil del docente.")
            return

        ventana = ctk.CTkToplevel(self.master)
        ventana.title("Perfil del Docente")
        ventana.geometry("500x400")
        ventana.configure(fg_color="#e6f2ff")

        ctk.CTkLabel(ventana, text="👤 Perfil del Docente", font=("Arial", 20, "bold"), text_color="#003366").pack(pady=20)

        for clave in ["usuario", "correo", "idMaestro", "rol"]:
            valor = docente.get(clave, "No disponible")
            texto = f"{clave.capitalize()}: {valor}"
            ctk.CTkLabel(ventana, text=texto, font=("Arial", 14), text_color="#003366").pack(pady=5)

    def generarOEditarActividad(self, ventana_padre):
        ventana = ctk.CTkToplevel(ventana_padre)
        ventana.title("Gestión de Actividades")
        ventana.geometry("420x360")
        ventana.configure(fg_color="#e6f2ff")  # Fondo general claro

        frame = ctk.CTkFrame(ventana, fg_color="#d0e7ff", corner_radius=20)
        frame.pack(padx=25, pady=25, fill="both", expand=True)

        header = ctk.CTkFrame(frame, fg_color="#cce6ff", corner_radius=10)
        header.pack(pady=(20, 15), fill="x", padx=10)

        ctk.CTkLabel(
            header, text="¿Qué deseas hacer?",
            font=("Arial", 20, "bold"), text_color="#003366"
        ).pack(pady=10)

        # Botones con estilo
        ctk.CTkButton(
            frame, text="1. Editar actividad",
            command=lambda: self.editarActividad(ventana_padre),
            fg_color="white", text_color="#003366", hover_color="#b3d9ff",
            corner_radius=15, width=280, height=40, font=("Arial", 13, "bold")
        ).pack(pady=8)

        ctk.CTkButton(
            frame, text="2. Crear nueva actividad",
            command=lambda: self.crearActividad(self.usuario),
            fg_color="white", text_color="#003366", hover_color="#b3d9ff",
            corner_radius=15, width=280, height=40, font=("Arial", 13, "bold")
        ).pack(pady=8)

        ctk.CTkButton(
            frame, text="3. Eliminar actividad",
            command=lambda: self.eliminarActividad(ventana_padre),
            fg_color="white", text_color="#003366", hover_color="#b3d9ff",
            corner_radius=15, width=280, height=40, font=("Arial", 13, "bold")
        ).pack(pady=8)

        ctk.CTkButton(
            frame, text="4. Finalizar actividad",
            command=lambda: self.finalizarActividad(ventana_padre),
            fg_color="white", text_color="#003366", hover_color="#b3d9ff",
            corner_radius=15, width=280, height=40, font=("Arial", 13, "bold")
        ).pack(pady=8)

        ctk.CTkButton(
            frame, text="5. Reactivar actividad",
            command=lambda: self.reactivarActividad(ventana_padre),
            fg_color="white", text_color="#003366", hover_color="#b3d9ff",
            corner_radius=15, width=280, height=40, font=("Arial", 13, "bold")
        ).pack(pady=8)


        ctk.CTkButton(
            frame, text="Cerrar",
            command=ventana.destroy,
            fg_color="#0066cc", text_color="white", hover_color="#004c99",
            corner_radius=12, width=280, height=40, font=("Arial", 13, "bold")
        ).pack(pady=(20, 10))

    def generarCodigoQR(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("Generar Código QR")
        ventana.geometry("500x300")

        ctk.CTkLabel(ventana, text="Título de la actividad:", anchor="w").pack(pady=10)
        entry_titulo = ctk.CTkEntry(ventana, width=400)
        entry_titulo.pack(pady=5)

        resultado = ctk.CTkLabel(ventana, text="", wraplength=450)
        resultado.pack(pady=20)

        def generar_qr():
            titulo = entry_titulo.get().strip()
            if not titulo:
                resultado.configure(text="Ingresa un título.", text_color="orange")
                return

            actividad = next((a for a in self.datos.get("actividades", []) if a["nombreActividad"].lower() == titulo.lower()), None)

            if not actividad:
                resultado.configure(text="Actividad no encontrada.", text_color="red")
                return

            data_qr = f"{actividad['idActividad']}|{actividad['nombreActividad']}|{actividad['horario']}"
            nombre_archivo_qr = f"QR_{actividad['nombreActividad'].replace(' ', '_')}.png"

            try:
                qr = qrcode.make(data_qr)
                qr.save(nombre_archivo_qr)

                resultado.configure(text=f"QR generado como {nombre_archivo_qr}", text_color="green")

                # Abrir el QR en el visor de imágenes predeterminado
                os.startfile(nombre_archivo_qr)  # Solo funciona en Windows

            except Exception as e:
                resultado.configure(text=f"Error al generar QR: {e}", text_color="red")

        ctk.CTkButton(ventana, text="Generar QR", command=generar_qr).pack(pady=10)
        
    def publicarNoticia(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("📰 Publicar Noticia")
        ventana.geometry("650x650")
        ventana.configure(fg_color="#e6f2ff")  # Fondo celeste claro

        frame = ctk.CTkFrame(ventana, fg_color="white", corner_radius=15)
        frame.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="📝 Publicar Noticia", font=("Arial", 22, "bold"),
            text_color="#003366"
        ).pack(pady=(20, 10))

        # Título
        ctk.CTkLabel(frame, text="Título de la noticia:", font=("Arial", 14), text_color="#003366").pack(pady=(10, 0), anchor="w", padx=30)
        entry_titulo = ctk.CTkEntry(frame, width=480, height=35)
        entry_titulo.pack(pady=(0, 15), padx=30)

        # Descripción
        ctk.CTkLabel(frame, text="Descripción:", font=("Arial", 14), text_color="#003366").pack(pady=(5, 0), anchor="w", padx=30)
        entry_descripcion = ctk.CTkTextbox(frame, height=150, width=480)
        entry_descripcion.pack(pady=(0, 10), padx=30)

        mensaje = ctk.CTkLabel(frame, text="", text_color="green", wraplength=480)
        mensaje.pack(pady=(5, 10))

        def publicar():
            titulo = entry_titulo.get().strip()
            descripcion = entry_descripcion.get("1.0", "end").strip()
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            remitente = self.master.usuario

            if not titulo or not descripcion:
                mensaje.configure(text="Completa todos los campos.", text_color="orange")
                return

            nuevaNoticia = {
                "titulo": titulo,
                "descripcion": descripcion,
                "remitente": remitente,
                "publicado": remitente,
                "fecha": fecha
            }

            def guardar_noticia_final():
                self.datos.setdefault("noticias", []).append(nuevaNoticia)
                guardarCambios(self.datos)
                mensaje.configure(text="✅ Noticia publicada con éxito.", text_color="green")

            # Cancelar clase
            if "cancelar clase" in titulo.lower() or "cancelar clase" in descripcion.lower():
                ventana_cancelar = ctk.CTkToplevel(ventana)
                ventana_cancelar.title("Cancelar Clase")
                ventana_cancelar.geometry("460x260")
                ventana_cancelar.configure(fg_color="#e6f2ff")

                frame_cancelar = ctk.CTkFrame(ventana_cancelar, fg_color="white", corner_radius=15)
                frame_cancelar.pack(padx=20, pady=20, fill="both", expand=True)

                ctk.CTkLabel(frame_cancelar, text="📍 Nombre de la clase (ej: Baile):", font=("Arial", 14), text_color="#003366").pack(pady=(10, 0), anchor="w", padx=20)
                entry_nombre = ctk.CTkEntry(frame_cancelar, width=350)
                entry_nombre.pack(pady=5)

                ctk.CTkLabel(frame_cancelar, text="📅 Fecha a cancelar (YYYY-MM-DD):", font=("Arial", 14), text_color="#003366").pack(pady=(10, 0), anchor="w", padx=20)
                entry_fecha = ctk.CTkEntry(frame_cancelar, width=350)
                entry_fecha.pack(pady=5)

                resultado = ctk.CTkLabel(frame_cancelar, text="", text_color="#004080", wraplength=400)
                resultado.pack(pady=10)

                def cancelar_clase():
                    nombreClase = entry_nombre.get().strip().lower()
                    fecha_cancelar = entry_fecha.get().strip()

                    if not nombreClase or not fecha_cancelar:
                        resultado.configure(text="Completa todos los campos.", text_color="orange")
                        return

                    actividad = next((a for a in self.datos.get("actividades", []) if a["nombreActividad"].lower() == nombreClase), None)
                    if not actividad:
                        resultado.configure(text="❌ Clase no encontrada.", text_color="red")
                        return

                    idActividad = actividad["idActividad"]

                    try:
                        with open("asistenciadatos.json", "r", encoding="utf-8") as f:
                            asistencia = json.load(f)

                        asistencia.setdefault("registros", {})
                        asistencia["registros"].setdefault(idActividad, {}).setdefault("canceladas", []).append(fecha_cancelar)

                        with open("asistenciadatos.json", "w", encoding="utf-8") as f:
                            json.dump(asistencia, f, indent=2, ensure_ascii=False)

                        nuevaNoticia["descripcion"] = f"Se cancela la sesión del día {fecha_cancelar} de {actividad['nombreActividad']}."
                        nuevaNoticia["cancelarSesion"] = {
                            "idActividad": idActividad,
                            "fecha": fecha_cancelar
                        }

                        resultado.configure(text=f"✅ Clase del {fecha_cancelar} cancelada.", text_color="green")
                        ventana_cancelar.after(1500, ventana_cancelar.destroy)
                        guardar_noticia_final()

                    except Exception as e:
                        resultado.configure(text=f"Error: {e}", text_color="red")

                ctk.CTkButton(
                    frame_cancelar, text="✅ Confirmar cancelación", command=cancelar_clase,
                    fg_color="white", text_color="#004080", hover_color="#cce6ff",
                    font=("Arial", 13, "bold"), corner_radius=10, width=220
                ).pack(pady=10)

            else:
                guardar_noticia_final()

        ctk.CTkButton(
            frame, text="📢 Publicar Noticia", command=publicar,
            fg_color="white", text_color="#004080", hover_color="#cce6ff",
            corner_radius=12, font=("Arial", 14, "bold"), width=200, height=40
        ).pack(pady=(10, 20))

    def reactivarActividad(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("Reactivar Actividad")
        ventana.geometry("500x350")
        ventana.configure(fg_color="#e6f2ff")

        fuente = ("Arial", 13, "bold")
        color = "#003366"

        ctk.CTkLabel(ventana, text="Ingresa el nombre de la actividad a reactivar:",
                    font=fuente, text_color=color).pack(pady=(30, 10))

        entry_nombre = ctk.CTkEntry(ventana, width=300, height=30)
        entry_nombre.pack(pady=5)

        mensaje = ctk.CTkLabel(ventana, text="", text_color="green", wraplength=450)
        mensaje.pack(pady=10)

        def reactivar():
            nombre = entry_nombre.get().strip().lower()
            for i, actividad in enumerate(self.datos.get("actividadesFinalizadas", [])):
                if actividad["nombreActividad"].strip().lower() == nombre:
                    actividad["estado"] = "activa"
                    self.datos["actividades"].append(self.datos["actividadesFinalizadas"].pop(i))
                    guardarCambios(self.datos)
                    mensaje.configure(text=f"✅ Actividad '{nombre}' reactivada correctamente.", text_color="green")
                    return
            mensaje.configure(text="❌ Actividad no encontrada entre finalizadas.", text_color="red")

        ctk.CTkButton(ventana, text="Reactivar", command=reactivar,
                    fg_color="#007acc", hover_color="#005fa3", text_color="white",
                    font=fuente, width=200, height=40, corner_radius=15).pack(pady=20)

    def gestionarActividad(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("Gestión de Actividades")
        ventana.geometry("400x200")

        ctk.CTkLabel(ventana, text="¿Qué deseas hacer?", font=("Arial", 16)).pack(pady=15)

        ctk.CTkButton(ventana, text="Finalizar actividad", command=lambda: self.finalizarActividad(ventana)).pack(pady=5)
        ctk.CTkButton(ventana, text="Reactivar actividad", command=lambda: self.reactivarActividad(ventana)).pack(pady=5)

    def finalizarActividad(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("Finalizar Actividad")
        ventana.geometry("500x350")

        ctk.CTkLabel(ventana, text="Ingresa el nombre de la actividad a finalizar:").pack(pady=10)
        entry_nombre = ctk.CTkEntry(ventana)
        entry_nombre.pack(pady=5)

        mensaje = ctk.CTkLabel(ventana, text="", text_color="green", wraplength=450)
        mensaje.pack(pady=10)

        def finalizar():
            nombre = entry_nombre.get().strip().lower()
            for i, actividad in enumerate(self.datos["actividades"]):
                if actividad["nombreActividad"].strip().lower() == nombre:
                    actividad["estado"] = "finalizada"
                    actividad_finalizada = self.datos["actividades"].pop(i)

                    # Asegurar lista de finalizadas
                    if "actividadesFinalizadas" not in self.datos:
                        self.datos["actividadesFinalizadas"] = []

                    self.datos["actividadesFinalizadas"].append(actividad_finalizada)

                    # ID de la actividad
                    id_act = actividad_finalizada["idActividad"]

                    # Actualizar estudiantes: mover a actividadesCompletadas si estaban inscritos
                    for estudiante in self.datos.get("estudiantes", []):
                        inscritas = estudiante.get("actividadesInscritas", [])
                        completadas = estudiante.setdefault("actividadesCompletadas", [])

                        if any(a.get("idActividad") == id_act for a in inscritas):
                            if id_act not in completadas:
                                completadas.append(id_act)

                        # 🧹 Limpieza (opcional): eliminar la actividad de inscritas si ya no se muestra como activa
                        estudiante["actividadesInscritas"] = [
                            a for a in inscritas if a.get("idActividad") != id_act
                        ]

                    guardarCambios(self.datos)

                    mensaje.configure(
                        text=f"Actividad '{nombre}' finalizada y registrada como completada para estudiantes."
                    )
                    return

            mensaje.configure(text="Actividad no encontrada.", text_color="red")

        ctk.CTkButton(ventana, text="Finalizar", command=finalizar).pack(pady=10)

    def editarActividad(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("✏️ Editar Actividad")
        ventana.geometry("650x750")
        ventana.configure(fg_color="#f2f6fc")

        frame_principal = ctk.CTkFrame(ventana, fg_color="#dceeff", corner_radius=20)
        frame_principal.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            frame_principal,
            text="🔎 Ingresa el nombre de la actividad a modificar:",
            font=("Arial", 15, "bold"),
            text_color="#003366"
        ).pack(pady=(20, 10))

        entry_id = ctk.CTkEntry(frame_principal, width=300, height=35, font=("Arial", 13))
        entry_id.pack(pady=5)

        info_text = ctk.CTkLabel(
            frame_principal, text="", anchor="w", justify="left",
            wraplength=550, text_color="#003366", font=("Arial", 13)
        )
        info_text.pack(pady=10)

        edit_frame = ctk.CTkFrame(frame_principal, fg_color="#f5faff", corner_radius=12)
        edit_frame.pack(pady=10, padx=10, fill="both", expand=False)

        entradas = {}
        campos = [
            ("nombreActividad", "Nuevo nombre"),
            ("categoria", "Nueva categoría"),
            ("personaEncargada", "Nuevo encargado"),
            ("detalles", "Nuevos detalles"),
            ("lugar", "Nuevo lugar"),
            ("cuposMaximos", "Nuevos cupos máximos")
        ]

        def cargar_datos():
            info_text.configure(text="")
            for widget in edit_frame.winfo_children():
                widget.destroy()

            nombre_buscar = entry_id.get().strip().lower()
            for actividad in self.datos["actividades"]:
                if nombre_buscar in actividad["nombreActividad"].strip().lower():
                    info_text.configure(
                        text=f"✅ Actividad encontrada: {actividad['nombreActividad']}"
                    )

                    for key, label in campos:
                        ctk.CTkLabel(edit_frame, text=label, font=("Arial", 13, "bold")).pack()
                        entrada = ctk.CTkEntry(edit_frame, width=400, height=30)
                        entrada.insert(0, str(actividad.get(key, "")))
                        entrada.pack(pady=3)
                        entradas[key] = entrada

                    def modificar_horario():
                        horario_win = ctk.CTkToplevel(ventana)
                        horario_win.title("Editar Horario")
                        horario_win.geometry("450x450")
                        horario_win.configure(fg_color="#e6f2ff")

                        ctk.CTkLabel(
                            horario_win, text="Horarios actuales:", 
                            font=("Arial", 16, "bold"), text_color="#003366"
                        ).pack(pady=(10, 5))

                        for idx, h in enumerate(actividad["horario"]):
                            ctk.CTkLabel(
                                horario_win, 
                                text=f"{idx+1}. {h['dia']} {h['inicio']} - {h['fin']}",
                                font=("Arial", 13), text_color="#333333"
                            ).pack()

                        frame_form = ctk.CTkFrame(horario_win, fg_color="transparent")
                        frame_form.pack(pady=10)

                        # Etiqueta y campo: índice
                        ctk.CTkLabel(frame_form, text="Número del horario a modificar:", font=("Arial", 13)).pack()
                        idx_entry = ctk.CTkEntry(frame_form, width=200)
                        idx_entry.pack(pady=4)

                        # Etiqueta y campo: nuevo día
                        ctk.CTkLabel(frame_form, text="Nuevo día:", font=("Arial", 13)).pack()
                        dia = ctk.CTkEntry(frame_form, width=200, placeholder_text="Ej: Lunes")
                        dia.pack(pady=4)

                        # Etiqueta y campo: nueva hora inicio
                        ctk.CTkLabel(frame_form, text="Nueva hora de inicio:", font=("Arial", 13)).pack()
                        hora_inicio = ctk.CTkEntry(frame_form, width=200, placeholder_text="Ej: 08:00")
                        hora_inicio.pack(pady=4)

                        # Etiqueta y campo: nueva hora fin
                        ctk.CTkLabel(frame_form, text="Nueva hora de fin:", font=("Arial", 13)).pack()
                        hora_fin = ctk.CTkEntry(frame_form, width=200, placeholder_text="Ej: 10:00")
                        hora_fin.pack(pady=4)

                        def aplicar():
                            try:
                                idx = int(idx_entry.get()) - 1
                                if 0 <= idx < len(actividad["horario"]):
                                    actividad["horario"][idx] = {
                                        "dia": dia.get().strip().capitalize() or actividad["horario"][idx]["dia"],
                                        "inicio": hora_inicio.get().strip() or actividad["horario"][idx]["inicio"],
                                        "fin": hora_fin.get().strip() or actividad["horario"][idx]["fin"]
                                    }
                                    guardarCambios(self.datos)
                                    info_text.configure(text=info_text.cget("text") + "\n✅ Horario actualizado.")
                                    horario_win.destroy()
                                else:
                                    info_text.configure(text="❌ Número de horario inválido.")
                            except Exception as e:
                                info_text.configure(text=f"❌ Error: {e}")

                        ctk.CTkButton(
                            horario_win, text="Guardar cambios", command=aplicar,
                            fg_color="#0066cc", hover_color="#004c99",
                            text_color="white", font=("Arial", 14, "bold"), width=200, height=40, corner_radius=12
                        ).pack(pady=15)

                    ctk.CTkButton(
                        edit_frame, text="Modificar horario", command=modificar_horario,
                        fg_color="#66b2ff", text_color="white", hover_color="#3399ff",
                        width=200, height=35, corner_radius=10
                    ).pack(pady=10)

                    def guardar():
                        try:
                            for k, entry in entradas.items():
                                valor = entry.get().strip()
                                if k == "cuposMaximos":
                                    actividad[k] = int(valor)
                                else:
                                    actividad[k] = valor or actividad[k]
                            guardarCambios(self.datos)
                            info_text.configure(text="✅ Cambios guardados correctamente.")
                        except Exception as e:
                            info_text.configure(text=f"❌ Error al guardar: {e}")

                    ctk.CTkButton(
                        edit_frame, text="Guardar cambios", command=guardar,
                        fg_color="#009933", text_color="white", hover_color="#007a29",
                        width=200, height=35, corner_radius=10
                    ).pack(pady=10)

                    return

            info_text.configure(text="❌ Actividad no encontrada.")

        ctk.CTkButton(
            frame_principal, text="Buscar", command=cargar_datos,
            fg_color="#0066cc", text_color="white", hover_color="#004c99",
            width=220, height=40, font=("Arial", 14, "bold"), corner_radius=15
        ).pack(pady=15)

    def mostrar_confirmacion_estilizada(nombre_actividad, callback_si, callback_no):
        confirm_win = ctk.CTkToplevel()
        confirm_win.title("Confirmación")
        confirm_win.geometry("400x200")
        confirm_win.configure(fg_color="#f2f2f2")

        frame = ctk.CTkFrame(confirm_win, fg_color="#f2f2f2")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        mensaje = f"¿Estás segura de eliminar '{nombre_actividad}'?"
        ctk.CTkLabel(frame, text=mensaje, font=("Arial", 14, "bold"), text_color="#333333").pack(pady=(10, 20))

        boton_frame = ctk.CTkFrame(frame, fg_color="transparent")
        boton_frame.pack(pady=10)

        def confirmar():
            confirm_win.destroy()
            callback_si()

        def cancelar():
            confirm_win.destroy()
            callback_no()

        ctk.CTkButton(boton_frame, text="Sí, eliminar", command=confirmar,
                    fg_color="#cc0000", hover_color="#990000", text_color="white",
                    font=("Arial", 12, "bold"), width=130, height=35, corner_radius=12).pack(side="left", padx=10)

        ctk.CTkButton(boton_frame, text="Cancelar", command=cancelar,
                    fg_color="#999999", hover_color="#666666", text_color="white",
                    font=("Arial", 12, "bold"), width=130, height=35, corner_radius=12).pack(side="left", padx=10)

    def eliminarActividad(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("Eliminar Actividad")
        ventana.geometry("500x400")
        ventana.configure(fg_color="#f2f2f2")

        ctk.CTkLabel(ventana, text="Ingresa el nombre de la actividad a eliminar:",
                    font=("Arial", 13, "bold"), text_color="#003366").pack(pady=20)

        entry_id = ctk.CTkEntry(ventana, width=300, height=30)
        entry_id.pack(pady=10)

        info_text = ctk.CTkLabel(ventana, text="", anchor="w", justify="left", wraplength=440,
                                font=("Arial", 12), text_color="#333333")
        info_text.pack(pady=15)

        def mostrar_confirmacion_estilizada(nombre_actividad, callback_si, callback_no):
            confirm_win = ctk.CTkToplevel()
            confirm_win.title("Confirmación")
            confirm_win.geometry("400x200")
            confirm_win.configure(fg_color="#f2f2f2")

            frame = ctk.CTkFrame(confirm_win, fg_color="#f2f2f2")
            frame.pack(expand=True, fill="both", padx=20, pady=20)

            mensaje = f"¿Estás segura de eliminar '{nombre_actividad}'?"
            ctk.CTkLabel(frame, text=mensaje, font=("Arial", 14, "bold"), text_color="#333333").pack(pady=(10, 20))

            boton_frame = ctk.CTkFrame(frame, fg_color="transparent")
            boton_frame.pack(pady=10)

            def confirmar():
                confirm_win.destroy()
                callback_si()

            def cancelar():
                confirm_win.destroy()
                callback_no()

            ctk.CTkButton(boton_frame, text="Sí, eliminar", command=confirmar,
                        fg_color="#cc0000", hover_color="#990000", text_color="white",
                        font=("Arial", 12, "bold"), width=130, height=35, corner_radius=12).pack(side="left", padx=10)

            ctk.CTkButton(boton_frame, text="Cancelar", command=cancelar,
                        fg_color="#999999", hover_color="#666666", text_color="white",
                        font=("Arial", 12, "bold"), width=130, height=35, corner_radius=12).pack(side="left", padx=10)

        def eliminar():
            nombre_act = entry_id.get().strip().lower()
            for i, act in enumerate(self.datos["actividades"]):
                if act["nombreActividad"].strip().lower() == nombre_act:
                    def confirmar_si():
                        self.datos["actividades"].pop(i)
                        guardarCambios(self.datos)
                        info_text.configure(text=f"✅ Actividad '{act['nombreActividad']}' eliminada.",
                                            text_color="green")

                    def confirmar_no():
                        info_text.configure(text="❌ Eliminación cancelada.", text_color="orange")

                    mostrar_confirmacion_estilizada(act["nombreActividad"], confirmar_si, confirmar_no)
                    return
            info_text.configure(text="Actividad no encontrada por nombre.", text_color="red")

        ctk.CTkButton(ventana, text="Eliminar Actividad", command=eliminar,
                    fg_color="#007acc", hover_color="#005fa3", text_color="white",
                    font=("Arial", 13, "bold"), width=300, height=40, corner_radius=15).pack(pady=10)


    def crearActividad(self, usuario_docente):
        ventana = ctk.CTkToplevel(self.master)
        scroll_frame = ctk.CTkScrollableFrame(ventana, fg_color="#e6f2ff", width=520, height=720)
        scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)
        ventana.title("Crear Actividad")
        ventana.geometry("550x750")
        ventana.configure(fg_color="#e6f2ff")

        frame = ctk.CTkFrame(scroll_frame, fg_color="#e6f2ff")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        entradas = {}
        horarios = []

        def etiqueta(texto):
            return ctk.CTkLabel(frame, text=texto, text_color="#003366", font=("Arial", 13, "bold"), anchor="w")

        def entrada_box():
            return ctk.CTkEntry(frame, height=30, width=300)

        campos = [
            ("nombre", "Título de la actividad"),
            ("categoria", "Categoría de la actividad"),
            ("personaEncargada", "Persona encargada"),
            ("detalles", "Detalles"),
            ("lugar", "Salón donde se hará la actividad"),
            ("cuposMaximos", "Cantidad máxima de cupos")
        ]

        for clave, texto in campos:
            etiqueta(texto).pack(pady=(10, 0))
            if clave == "categoria":
                entrada = ctk.CTkComboBox(frame, values=["Obligatoria", "Opcional"], width=300, height=30)
                entrada.set("Selecciona")
            elif clave == "personaEncargada":
                entrada = ctk.CTkEntry(frame, height=30, width=300)
                entrada.insert(0, usuario_docente)
                entrada.configure(state="disabled")
            else:
                entrada = entrada_box()
            entrada.pack(pady=5)
            entradas[clave] = entrada

        # Horario
        etiqueta("Día del horario (Ej: Miércoles)").pack(pady=(15, 0))
        dia_entry = entrada_box()
        dia_entry.pack(pady=2)

        etiqueta("Hora de inicio (HH:MM)").pack(pady=(10, 0))
        inicio_entry = entrada_box()
        inicio_entry.pack(pady=2)

        etiqueta("Hora de fin (HH:MM)").pack(pady=(10, 0))
        fin_entry = entrada_box()
        fin_entry.pack(pady=2)

        mensaje_label = ctk.CTkLabel(frame, text="", text_color="red", font=("Arial", 12))
        mensaje_label.pack(pady=10)

        def agregar_horario():
            dia = dia_entry.get().strip().capitalize()
            inicio = inicio_entry.get().strip()
            fin = fin_entry.get().strip()
            dias_validos = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

            if not dia or not inicio or not fin:
                mensaje_label.configure(text="Completa los 3 campos antes de agregar.", text_color="red")
                return

            if dia not in dias_validos:
                mensaje_label.configure(text=f"'{dia}' no es un día válido.", text_color="red")
                return

            try:
                hora_inicio = datetime.strptime(inicio, "%H:%M")
                hora_fin = datetime.strptime(fin, "%H:%M")

                if hora_inicio >= hora_fin:
                    mensaje_label.configure(text="Hora de inicio debe ser menor que la de fin.", text_color="red")
                    return

                for h in horarios:
                    if h["dia"] == dia and h["inicio"] == inicio and h["fin"] == fin:
                        mensaje_label.configure(text="Ese horario ya fue agregado.", text_color="red")
                        return

                horarios.append({"dia": dia, "inicio": inicio, "fin": fin})
                mensaje_label.configure(text=f"✅ Horario agregado: {dia} {inicio}-{fin}", text_color="green")

                dia_entry.delete(0, "end")
                inicio_entry.delete(0, "end")
                fin_entry.delete(0, "end")

            except ValueError:
                mensaje_label.configure(text="Formato de hora inválido. Usa HH:MM", text_color="red")

        def finalizar_creacion():
            try:
                if not horarios:
                    mensaje_label.configure(text="Agrega al menos un horario.", text_color="red")
                    return

                nombre = entradas["nombre"].get().strip()
                categoria = entradas["categoria"].get().strip()
                detalles = entradas["detalles"].get().strip()
                lugar = entradas["lugar"].get().strip()

                try:
                    cuposMaximos = int(entradas["cuposMaximos"].get().strip())
                    if cuposMaximos <= 0:
                        mensaje_label.configure(text="Cupos deben ser mayores a cero.", text_color="red")
                        return
                except ValueError:
                    mensaje_label.configure(text="Cupos debe ser un número.", text_color="red")
                    return

                if not nombre or categoria == "Selecciona" or not detalles or not lugar:
                    mensaje_label.configure(text="Completa todos los campos.", text_color="red")
                    return

                idActividad = nombre.lower().replace(" ", "_") + "_01_2025"

                nuevaActividad = {
                    "nombreActividad": nombre,
                    "idActividad": idActividad,
                    "categoria": categoria,
                    "personaEncargada": usuario_docente,
                    "detalles": detalles,
                    "horario": horarios,
                    "lugar": lugar,
                    "cuposMaximos": cuposMaximos,
                    "estado": "activa",
                    "inscritos": []
                }

                self.datos["actividades"].append(nuevaActividad)
                guardarCambios(self.datos)

                mensaje_label.configure(text="✅ Actividad guardada correctamente.", text_color="green")

                for entrada in entradas.values():
                    if isinstance(entrada, ctk.CTkEntry):
                        entrada.configure(state="normal")
                        entrada.delete(0, "end")
                    elif isinstance(entrada, ctk.CTkComboBox):
                        entrada.set("Selecciona")
                entradas["personaEncargada"].insert(0, usuario_docente)
                entradas["personaEncargada"].configure(state="disabled")
                horarios.clear()

            except Exception as e:
                mensaje_label.configure(text=f"Error: {e}", text_color="red")

        ctk.CTkButton(frame, text="Agregar horario", command=agregar_horario,
                    fg_color="#007acc", hover_color="#005fa3", text_color="white",
                    width=300, height=35, corner_radius=15, font=("Arial", 13, "bold")).pack(pady=(10, 5))

        ctk.CTkButton(frame, text="Crear actividad", command=finalizar_creacion,
                    fg_color="#0066cc", hover_color="#004c99", text_color="white",
                    width=300, height=40, corner_radius=15, font=("Arial", 13, "bold")).pack(pady=15)

    def mostrar_estado_asistencia(self, id_actividad, horario, inscritos):
        # Intenta obtener la sesión, o devuelve una lista vacía si no existe
        sesion = self.asistencia.get("registros", {}).get(id_actividad, {}).get("sesiones", {}).get(horario, [])
        
        # Lista de usuarios que asistieron
        asistieron = [r.get("usuario") for r in sesion if "usuario" in r]

        # Crear ventana nueva
        ventana = ctk.CTkToplevel(self.master)
        ventana.title("Estado de Asistencia")
        ventana.geometry("400x400")

        # Mostrar asistentes
        ctk.CTkLabel(ventana, text="Ya escanearon:").pack()
        if asistieron:
            for u in asistieron:
                ctk.CTkLabel(ventana, text=f"- {u}").pack()
        else:
            ctk.CTkLabel(ventana, text="(Nadie ha escaneado aún)").pack()

        # Mostrar ausentes
        ctk.CTkLabel(ventana, text="\n Aún no han escaneado:").pack()
        ausentes = [u for u in inscritos if u not in asistieron]
        if ausentes:
            for u in ausentes:
                ctk.CTkLabel(ventana, text=f"- {u}").pack()
        else:
            ctk.CTkLabel(ventana, text="(Todos han escaneado)").pack()

    def registrar_asistencia(self, usuario, id_actividad, nombre_actividad, horario):
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")

        dia_hoy = datetime.now().strftime("%A")
        dia_hoy_esp = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
                       "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}.get(dia_hoy, "")

        if not horario.split(":")[0].strip() == dia_hoy_esp:
            ctk.CTkLabel(self.master, text=f"Hoy no hay sesión para el horario '{horario}'.").pack(pady=10)
            return

        if id_actividad not in self.asistencia["registros"]:
            self.asistencia["registros"][id_actividad] = {
                "nombreActividad": nombre_actividad,
                "sesiones": {},
                "canceladas": [],
                "faltas": {}
            }

        # Registrar la asistencia
        sesiones = self.asistencia["registros"][id_actividad]["sesiones"]

        if horario not in sesiones:
            sesiones[horario] = []

        sesiones[horario].append({
            "usuario": usuario,
            "fecha_hora": ahora
        })

        guardar_asistencia(self.asistencia)  # Asegúrate que esta función esté definida
        ctk.CTkLabel(self.master, text="Asistencia registrada exitosamente.").pack(pady=10)

    def generar_reporte_gui(asistencia, id_actividad, nombre_actividad, horario, inscritos):
        ventana = ctk.CTkToplevel()
        ventana.title("Generar Reporte de Asistencia")
        ventana.geometry("620x550")
        ventana.configure(fg_color="#e6f2ff")

        # Título
        ctk.CTkLabel(
            ventana, text="📄 Generar Reporte de Asistencia",
            font=("Arial", 18, "bold"), text_color="#003366"
        ).pack(pady=(20, 10))

        # Subtítulo
        ctk.CTkLabel(
            ventana, text=f"Actividad: {nombre_actividad}", 
            font=("Arial", 14, "bold"), text_color="#003366"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            ventana, text=f"Horario: {horario}", 
            font=("Arial", 13), text_color="#003366"
        ).pack(pady=(0, 15))

        # Caja de texto para mostrar reporte
        textbox = ctk.CTkTextbox(
            ventana, width=550, height=300, 
            fg_color="white", text_color="black", 
            font=("Arial", 12), wrap="word", corner_radius=10
        )
        textbox.pack(pady=10)

        mensaje_label = ctk.CTkLabel(ventana, text="", font=("Arial", 12))
        mensaje_label.pack(pady=5)

        def generar():
            sesiones = asistencia["registros"].get(id_actividad, {}).get("sesiones", {}).get(horario, [])
            asistieron = {r["usuario"]: r["fecha_hora"] for r in sesiones}
            ahora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Reporte_{nombre_actividad.replace(' ', '_')}_{ahora}.txt"

            if not inscritos:
                mensaje_label.configure(text="No hay estudiantes inscritos para esta actividad.", text_color="red")
                return

            try:
                with open(nombre_archivo, "w", encoding="utf-8") as f:
                    f.write("REPORTE DE ASISTENCIA\n")
                    f.write(f"Actividad: {nombre_actividad}\n")
                    f.write(f"Horario: {horario}\n")
                    f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("🟢 PRESENTES:\n")
                    for u in asistieron:
                        f.write(f"- {u} | {asistieron[u]}\n")
                    f.write("\n🔴 AUSENTES:\n")
                    for u in inscritos:
                        if u not in asistieron:
                            f.write(f"- {u}\n")

                # Mostrar contenido en textbox
                with open(nombre_archivo, "r", encoding="utf-8") as f:
                    texto = f.read()
                    textbox.delete("1.0", "end")
                    textbox.insert("1.0", texto)

                mensaje_label.configure(text=f"✅ Reporte guardado como: {nombre_archivo}", text_color="green")
                os.startfile(nombre_archivo)

            except Exception as e:
                mensaje_label.configure(text=f"❌ Error al guardar: {e}", text_color="red")

        # Botón estilizado
        ctk.CTkButton(
            ventana, text="📤 Generar y Guardar Reporte", command=generar,
            fg_color="#007acc", hover_color="#005fa3", text_color="white",
            font=("Arial", 13, "bold"), width=260, height=40, corner_radius=20
        ).pack(pady=15)

    def buscarEstudianteHistorial(self):
        ventana = ctk.CTkToplevel(self.master)
        ventana.title("Buscar Estudiante")
        ventana.geometry("450x500")

        ctk.CTkLabel(ventana, text="Ingresa nombre, carnet o correo del estudiante:").pack(pady=10)
        entry_busqueda = ctk.CTkEntry(ventana, width=300)
        entry_busqueda.pack(pady=5)

        resultado_texto = ctk.CTkTextbox(ventana, height=300, width=400)
        resultado_texto.pack(pady=10)

        def buscar():
            resultado_texto.delete("1.0", "end")
            nombreEstudianteBuscar = entry_busqueda.get().strip().lower()
            
            for estudiante in self.datos.get("estudiantes", []):
                if (nombreEstudianteBuscar in estudiante["usuario"].lower() or
                    nombreEstudianteBuscar in estudiante["carnet"].lower() or
                    nombreEstudianteBuscar in estudiante["correo"].lower()):

                    resultado_texto.insert("end", f"\nPerfil del estudiante: {estudiante['usuario']}\n")
                    resultado_texto.insert("end", f"Carnet: {estudiante['carnet']}\n")
                    resultado_texto.insert("end", f"Correo: {estudiante['correo']}\n")
                    resultado_texto.insert("end", f"Carrera: {estudiante.get('carrera', 'No registrada')}\n")

                    actividades = estudiante.get("actividadesInscritas", [])
                    if not actividades:
                        resultado_texto.insert("end", "\nNo tiene actividades inscritas actualmente.\n")
                        return

                    for a in actividades:
                        actividad = next((act for act in self.datos["actividades"]
                                        if act["idActividad"] == a["idActividad"]), None)
                        if actividad:
                            sesiones = self.asistencia.get("registros", {}).get(actividad["idActividad"], {}).get("sesiones", {})
                            total = sum(1 for lista in sesiones.values()
                                        for r in lista if r["usuario"] == estudiante["usuario"])
                            fechas = [r["fecha_hora"].split()[0] for lista in sesiones.values()
                                    for r in lista if r["usuario"] == estudiante["usuario"]]

                            resultado_texto.insert("end", f"\nActividad: {actividad['nombreActividad']}\n")
                            resultado_texto.insert("end", f"Estado: {actividad.get('estado', 'Desconocido')}\n")
                            resultado_texto.insert("end", f"Asistencias registradas: {total}\n")
                            if fechas:
                                resultado_texto.insert("end", f"Fechas de asistencia: {', '.join(fechas)}\n")
                    return

            resultado_texto.insert("end", "\nEstudiante no encontrado. Verifica la información.")

        ctk.CTkButton(ventana, text="Buscar", command=buscar).pack(pady=10)
    
    def Reporte_semanal(self):
        ventana = ctk.CTkToplevel(self.master)
        ventana.title("Generar Reporte Semanal")
        ventana.geometry("450x400")

        # Entradas de fecha
        ctk.CTkLabel(ventana, text="Fecha de inicio (YYYY-MM-DD):").pack(pady=5)
        entry_inicio = ctk.CTkEntry(ventana)
        entry_inicio.pack(pady=5)

        ctk.CTkLabel(ventana, text="Fecha final (YYYY-MM-DD):").pack(pady=5)
        entry_final = ctk.CTkEntry(ventana)
        entry_final.pack(pady=5)

        #Área para mostrar resultados
        resultado_label = ctk.CTkLabel(ventana, text="", anchor="w", justify="left", wraplength=450)
        resultado_label.pack(pady=10)

        def generar():
            fecha_inicio = entry_inicio.get().strip()
            fecha_final = entry_final.get().strip()

            # Validar formato de fecha
            try:
                inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                fin = datetime.strptime(fecha_final, "%Y-%m-%d")
            except ValueError:
                resultado_label.configure(text="Formato incorrecto de fecha. Usa YYYY-MM-DD.")
                return
            
            if inicio > fin:
                resultado_label.configure(text="La fecha de inicio no puede ser posterior a la final.")
                return

            reporte = f"Reporte Semanal de Asistencia\nDesde: {fecha_inicio} Hasta: {fecha_final}\n\n"
            actividades_encontradas = False 

            for actividad in self.datos.get("actividades", []):
                id_act = actividad.get("idActividad")
                nombre = actividad.get("nombreActividad")
                inscritos = actividad.get("inscritos", [])
                if not inscritos:
                    continue
                
                sesiones = self.asistencia.get("registros", {}).get(id_act, {}).get("sesiones", {})
                linea = f"🔷 Actividad: {nombre} ({id_act})\n"
                asistencias = []

                for usuario in inscritos:
                    total = 0
                    for lista in sesiones.values():
                        for r in lista:
                            if r["usuario"] == usuario:
                                try:
                                    fecha_r = datetime.strptime(r["fecha_hora"].split()[0], "%Y-%m-%d")
                                    if inicio <= fecha_r <= fin:
                                        total += 1
                                except:
                                    continue
                    if total > 0:
                        asistencias.append(f"- {usuario}: {total} asistencias")

                if asistencias:
                    actividades_encontradas = True
                    linea += "\n".join(asistencias) + "\n\n"
                    reporte += linea

            if not actividades_encontradas:
                resultado_label.configure(text="No hay asistencias en ese rango de fechas.")
                return

            nombre_archivo = f"ReporteSemanal_{fecha_inicio}_a_{fecha_final}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(reporte)

            resultado_label.configure(text=f"Reporte generado como: {nombre_archivo}")

         # Botón para generar el reporte
        ctk.CTkButton(ventana, text="Generar Reporte", command=generar).pack(pady=10)

class MenuDocente(ctk.CTkToplevel):
    def __init__(self, master, tipoUsuario, usuario, datos, asistencia):
        super().__init__(master)
        self.master = master
        self.tipoUsuario = tipoUsuario
        self.usuario = usuario
        self.datos = datos
        self.asistencia = asistencia
        self.title("Menú Docente")
        self.geometry("700x700")
        self.configure(fg_color="#e6f2ff")  # Fondo celeste claro
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        self.funciones_docente = None  # Se asigna luego

        self.frame_contenedor = ctk.CTkFrame(self, fg_color="#d0e7ff", corner_radius=20)
        self.frame_contenedor.pack(padx=30, pady=30, fill="both", expand=True)

        # Contenedor de bienvenida
        bienvenida_frame = ctk.CTkFrame(self.frame_contenedor, fg_color="transparent")
        bienvenida_frame.pack(pady=15)

        ctk.CTkLabel(
            bienvenida_frame,
            text=f"Bienvenido, {usuario}",
            font=("Arial", 22, "bold"),
            text_color="#003366"
        ).pack(side="left", padx=10)

        self.funciones_docente = DocenteFunciones(self, self.datos, self.asistencia, self.usuario)

        ctk.CTkButton(
            bienvenida_frame,
            text="🧑‍🏫",
            width=40, height=40,
            corner_radius=20,
            fg_color="#0066cc", hover_color="#004c99",
            text_color="white", font=("Arial", 18, "bold"),
            command=self.funciones_docente.mostrar_perfil_docente
        ).pack(side="left")

        # Contenedor para el menú
        self.frame_menu = ctk.CTkFrame(self.frame_contenedor, fg_color="transparent")
        self.frame_menu.pack(pady=10)

        # Botones de opciones
        opciones = [
            ("1. Generar actividad cocurricular", self.opcion_1),
            ("2. Generar reporte semanal", self.Reporte_semanal),
            ("3. Finalizar / Reactivar actividad", lambda: self.funciones_docente.gestionarActividad(self)),
            ("4. Publicar noticia", lambda: self.funciones_docente.publicarNoticia(self)),
            ("5. Historial estudiantil", self.buscarEstudianteHistorial),
            ("6. Generar código QR", lambda: self.funciones_docente.generarCodigoQR(self)),
            ("7. Reportar error", lambda: reportarErrorVentana(self, self.datos, self.usuario))
        ]

        for texto, comando in opciones:
            ctk.CTkButton(
                self.frame_menu,
                text=texto,
                command=comando,
                fg_color="white", text_color="#003366",
                hover_color="#b3d9ff",
                corner_radius=15, width=300, height=40,
                font=("Arial", 14, "bold")
            ).pack(pady=6)

        # Botón de cerrar sesión
        ctk.CTkButton(
            self.frame_contenedor,
            text="Cerrar sesión",
            command=self.cerrar_aplicacion,
            fg_color="#0066cc", text_color="white",
            hover_color="#004c99",
            corner_radius=12, width=300, height=45,
            font=("Arial", 15, "bold")
        ).pack(pady=(20, 10))

    def cerrar_aplicacion(self):
        self.destroy()
        self.master.deiconify()

    def opcion_1(self):
        self.funciones_docente.generarOEditarActividad(self)

    def Reporte_semanal(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Generar Reporte Semanal")
        ventana.geometry("540x520")
        ventana.configure(fg_color="#e6f2ff")

        # Estilo común
        fuente_label = ("Arial", 13, "bold")
        color_texto = "#003366"

        ctk.CTkLabel(ventana, text="Fecha de inicio (YYYY-MM-DD):", font=fuente_label, text_color=color_texto).pack(pady=(15, 5))
        entry_inicio = ctk.CTkEntry(ventana, width=300, height=30)
        entry_inicio.pack()

        ctk.CTkLabel(ventana, text="Fecha final (YYYY-MM-DD):", font=fuente_label, text_color=color_texto).pack(pady=(15, 5))
        entry_final = ctk.CTkEntry(ventana, width=300, height=30)
        entry_final.pack()

        resultado = ctk.CTkTextbox(ventana, width=460, height=160)
        resultado.configure(state="normal")
        resultado.pack(pady=20)

        def generar():
            fecha_inicio = entry_inicio.get()
            fecha_final = entry_final.get()

            try:
                inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                fin = datetime.strptime(fecha_final, "%Y-%m-%d")
            except ValueError:
                resultado.configure(state="normal")
                resultado.delete("1.0", "end")
                resultado.insert("end", "❌ Formato incorrecto de fecha\n")
                resultado.configure(state="disabled")
                return

            reporte = "\n📋 Reporte Semanal de Asistencia\n\n"

            for actividad in self.datos.get("actividades", []):
                id_act = actividad.get("idActividad")
                nombre = actividad.get("nombreActividad")
                inscritos = actividad.get("inscritos", [])
                if not inscritos:
                    continue
                reporte += f"📌 Actividad: {nombre} ({id_act})\nEstudiantes:\n"
                sesiones = self.asistencia.get("registros", {}).get(id_act, {}).get("sesiones", {})

                for usuario in inscritos:
                    total = 0
                    for lista in sesiones.values():
                        for r in lista:
                            if r["usuario"] == usuario:
                                try:
                                    fecha_r = datetime.strptime(r["fecha_hora"].split()[0], "%Y-%m-%d")
                                    if inicio <= fecha_r <= fin:
                                        total += 1
                                except:
                                    continue
                    reporte += f"  • {usuario}: {total} asistencias entre {fecha_inicio} y {fecha_final}\n"
                reporte += "\n"

            nombre_archivo = f"ReporteSemanal_{fecha_inicio}_a_{fecha_final}.txt"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(reporte)

            resultado.configure(state="normal")
            resultado.delete("1.0", "end")
            resultado.insert("end", f"✅ Reporte generado y guardado como:\n{nombre_archivo}")
            resultado.configure(state="disabled")

            os.startfile(nombre_archivo)

        ctk.CTkButton(
            ventana, text="Generar", command=generar,
            fg_color="#007acc", hover_color="#005fa3", text_color="white",
            font=("Arial", 13, "bold"), width=300, height=40, corner_radius=15
        ).pack(pady=10)

    def finalizarActividad(self, parent):
        ventana = ctk.CTkToplevel(parent)
        ventana.title("Finalizar Actividad")
        ventana.geometry("500x350")

    def buscarEstudianteHistorial(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Buscar Estudiante")
        ventana.geometry("500x500")

        ctk.CTkLabel(ventana, text="Ingresa nombre, carnet o correo del estudiante:").pack(pady=10)
        entry_busqueda = ctk.CTkEntry(ventana, width=350)
        entry_busqueda.pack(pady=5)

        resultado_texto = ctk.CTkTextbox(ventana, height=350, width=460)
        resultado_texto.pack(pady=10)

        def buscar():
            resultado_texto.delete("1.0", "end")
            nombreEstudianteBuscar = entry_busqueda.get().strip().lower()

            for estudiante in self.datos.get("estudiantes", []):
                if (nombreEstudianteBuscar in estudiante["usuario"].lower() or
                    nombreEstudianteBuscar in estudiante["carnet"].lower() or
                    nombreEstudianteBuscar in estudiante["correo"].lower()):

                    resultado_texto.insert("end", f"\n👤 Perfil del estudiante: {estudiante['usuario']}\n")
                    resultado_texto.insert("end", f"Carnet: {estudiante['carnet']}\n")
                    resultado_texto.insert("end", f"Correo: {estudiante['correo']}\n")
                    resultado_texto.insert("end", f"Carrera: {estudiante.get('carrera', 'No registrada')}\n")

                    actividades = estudiante.get("actividadesInscritas", [])
                    if not actividades:
                        resultado_texto.insert("end", "\nNo tiene actividades inscritas actualmente.\n")
                        return

                    for a in actividades:
                        actividad = next((act for act in self.datos["actividades"]
                                        if act["idActividad"] == a["idActividad"]), None)
                        if actividad:
                            sesiones = self.asistencia.get("registros", {}).get(actividad["idActividad"], {}).get("sesiones", {})
                            total = sum(1 for lista in sesiones.values()
                                        for r in lista if r["usuario"] == estudiante["usuario"])
                            fechas = [r["fecha_hora"].split()[0] for lista in sesiones.values()
                                    for r in lista if r["usuario"] == estudiante["usuario"]]

                            resultado_texto.insert("end", f"\nActividad: {actividad['nombreActividad']}\n")
                            resultado_texto.insert("end", f"Estado: {actividad.get('estado', 'Desconocido')}\n")
                            resultado_texto.insert("end", f"Asistencias registradas: {total}\n")
                            if fechas:
                                resultado_texto.insert("end", f"Fechas de asistencia: {', '.join(fechas)}\n")
                    return

            resultado_texto.insert("end", "\nEstudiante no encontrado. Verifica la información.")

        ctk.CTkButton(ventana, text="Buscar", command=buscar).pack(pady=10)

def editar_usuario_gui(root, datos):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Editar Usuario")
    ventana.geometry("500x600")

    resultado_label = ctk.CTkLabel(ventana, text="")
    resultado_label.pack(pady=5)

    tipos = ["Alumno", "Docente", "Administrador"]
    tipo_var = ctk.StringVar(value="Alumno")
    tipo_menu = ctk.CTkOptionMenu(ventana, values=tipos, variable=tipo_var)
    tipo_menu.pack(pady=10)

    usuarios_var = ctk.StringVar()
    usuarios_menu = ctk.CTkOptionMenu(ventana, values=["Selecciona un tipo primero"], variable=usuarios_var)
    usuarios_menu.pack(pady=10)

    def actualizar_usuarios_menu(tipo):
        grupo = {"Alumno": "estudiantes", "Docente": "maestros", "Administrador": "administrador"}[tipo]
        lista = [u["usuario"] for u in datos.get(grupo, [])]
        if lista:
            usuarios_menu.configure(values=lista)
            usuarios_var.set(lista[0])
        else:
            usuarios_menu.configure(values=["(sin usuarios disponibles)"])
            usuarios_var.set("(sin usuarios disponibles)")

    tipo_menu.configure(command=actualizar_usuarios_menu)
    actualizar_usuarios_menu("Alumno")

    campos_frame = ctk.CTkScrollableFrame(ventana, height=300)
    campos_frame.pack(pady=10, fill="both", expand=True)

    def buscar_y_mostrar():
        tipo = tipo_var.get()
        usuario_nombre = usuarios_var.get()
        grupo = {"Alumno": "estudiantes", "Docente": "maestros", "Administrador": "administrador"}.get(tipo)

        if not grupo:
            resultado_label.configure(text="Tipo de usuario no válido.", text_color="red")
            return

        usuario = next((u for u in datos[grupo] if u["usuario"] == usuario_nombre), None)
        if not usuario:
            resultado_label.configure(text="Usuario no encontrado.", text_color="red")
            return

        resultado_label.configure(text="Usuario encontrado. Edita los campos.", text_color="green")

        for widget in campos_frame.winfo_children():
            widget.destroy()

        entradas = {}

        for clave, valor in usuario.items():
            # Ocultar campos que no deben editarse directamente
            if clave in ["actividadesInscritas", "intereses", "notificaciones", "idEstudiante"]:
                continue
            if isinstance(valor, (list, dict, bool)):
                continue

            ctk.CTkLabel(campos_frame, text=f"{clave}:").pack()
            entrada = ctk.CTkEntry(campos_frame)
            entrada.insert(0, str(valor))
            entrada.pack()
            entradas[clave] = entrada

        def guardar_cambios():
            for clave, entrada in entradas.items():
                nuevo_valor = entrada.get().strip()
                usuario[clave] = nuevo_valor

            # Generar automáticamente el idEstudiante desde carnet
            if "carnet" in entradas:
                carnet_val = entradas["carnet"].get().strip()
                if carnet_val.isdigit() and len(carnet_val) >= 6:
                    usuario["idEstudiante"] = "KEY_" + carnet_val[-6:]

            guardarCambios(datos)
            resultado_label.configure(text="Cambios guardados correctamente.", text_color="green")

        ctk.CTkButton(campos_frame, text="Guardar Cambios", command=guardar_cambios).pack(pady=10)

    ctk.CTkButton(ventana, text="Buscar Usuario", command=buscar_y_mostrar).pack(pady=10)

def eliminar_usuario_gui(root, datos):
    asistencia = cargar_asistencia()
    admin_data = cargarAdminData()

    ventana = ctk.CTkToplevel(root)
    ventana.title("Eliminar Usuario")
    ventana.geometry("500x400")
    ventana.configure(fg_color="#e6f2ff")

    frame = ctk.CTkFrame(ventana, fg_color="#e6f2ff")
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(frame, text="Eliminar Usuario", font=("Arial", 20, "bold"), text_color="#003366").pack(pady=(5, 10))

    resultado_label = ctk.CTkLabel(frame, text="", font=("Arial", 12))
    resultado_label.pack(pady=5)

    tipos = ["Alumno", "Docente", "Administrador"]
    tipo_var = ctk.StringVar(value="Alumno")
    tipo_menu = ctk.CTkOptionMenu(frame, values=tipos, variable=tipo_var, width=300)
    tipo_menu.pack(pady=10)

    usuarios_var = ctk.StringVar()
    usuarios_menu = ctk.CTkOptionMenu(frame, values=["Selecciona un tipo primero"], variable=usuarios_var, width=300)
    usuarios_menu.pack(pady=10)

    def actualizar_usuarios_menu(tipo):
        grupo = {"Alumno": "estudiantes", "Docente": "maestros", "Administrador": "administrador"}[tipo]
        lista = [u["usuario"] for u in datos.get(grupo, [])]
        if lista:
            usuarios_menu.configure(values=lista)
            usuarios_var.set(lista[0])
        else:
            usuarios_menu.configure(values=["(sin usuarios disponibles)"])
            usuarios_var.set("(sin usuarios disponibles)")

    tipo_menu.configure(command=actualizar_usuarios_menu)
    actualizar_usuarios_menu("Alumno")

    def eliminar():
        tipo = tipo_var.get()
        usuario_nombre = usuarios_var.get()

        grupo = {"Alumno": "estudiantes", "Docente": "maestros", "Administrador": "administrador"}.get(tipo)
        if not grupo:
            resultado_label.configure(text="Tipo de usuario no válido.", text_color="red")
            return

        usuario = next((u for u in datos[grupo] if u["usuario"] == usuario_nombre), None)
        if not usuario:
            resultado_label.configure(text="Usuario no encontrado.", text_color="red")
            return

        confirm_win = ctk.CTkToplevel(ventana)
        confirm_win.title("Confirmación")
        confirm_win.geometry("420x200")
        confirm_win.configure(fg_color="#fff0f0")

        ctk.CTkLabel(
            confirm_win,
            text=f"¿Estás seguro de eliminar a '{usuario_nombre}'?",
            font=("Arial", 14, "bold"),
            text_color="black",
            wraplength=380,
            justify="center"
        ).pack(pady=25)

        def confirmar_si():
            confirm_win.destroy()
            datos[grupo].remove(usuario)

            if tipo == "Alumno":
                for actividad in datos.get("actividades", []):
                    if "inscritos" in actividad and usuario_nombre in actividad["inscritos"]:
                        actividad["inscritos"].remove(usuario_nombre)

            if tipo == "Docente":
                for actividad in datos.get("actividades", []):
                    if actividad.get("personaEncargada") == usuario_nombre:
                        actividad["personaEncargada"] = "Sin encargado"

            for idActividad, registro in asistencia["registros"].items():
                for fecha in list(registro.get("sesiones", {})):
                    registro["sesiones"][fecha] = [
                        r for r in registro["sesiones"][fecha] if r["usuario"] != usuario_nombre
                    ]
                registro.get("faltas", {}).pop(usuario_nombre, None)

            admin_data["historialAcciones"] = [
                a for a in admin_data.get("historialAcciones", []) if a["usuario"] != usuario_nombre
            ]
            for error in admin_data.get("erroresReportados", []):
                if error["usuario"] == usuario_nombre:
                    error["usuario"] = f"{usuario_nombre} (eliminado)"

            guardarCambios(datos)
            guardarAsistencia(asistencia)
            guardarAdminData(admin_data)

            resultado_label.configure(
                text=f"✅ Usuario '{usuario_nombre}' eliminado con éxito.",
                text_color="green"
            )

        def confirmar_no():
            confirm_win.destroy()

        ctk.CTkButton(confirm_win, text="Sí, eliminar", command=confirmar_si,
                      fg_color="#cc0000", hover_color="#990000", text_color="white",
                      font=("Arial", 12, "bold"), width=150, height=35).pack(pady=(5, 10))
        ctk.CTkButton(confirm_win, text="Cancelar", command=confirmar_no,
                      fg_color="#dddddd", text_color="black",
                      font=("Arial", 12), width=150, height=35).pack()

    ctk.CTkButton(
        frame,
        text="Eliminar Usuario",
        command=eliminar,
        fg_color="#d9534f", hover_color="#c9302c",
        text_color="white", font=("Arial", 13, "bold"),
        width=300, height=40, corner_radius=15
    ).pack(pady=20)

def modificar_porcentaje_gui(root, admin_data):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Modificar Porcentaje de Advertencia")
    ventana.geometry("350x200")

    actual = admin_data["configuracion"].get("porcentajeAdvertencia", 25)
    resultado_label = ctk.CTkLabel(ventana, text=f"Porcentaje actual: {actual}%")
    resultado_label.pack(pady=10)

    nuevo_entry = ctk.CTkEntry(ventana, placeholder_text="Nuevo porcentaje (1-100)")
    nuevo_entry.pack(pady=10)

    resultado_guardado = ctk.CTkLabel(ventana, text="")
    resultado_guardado.pack(pady=5)

    def actualizar():
        try:
            nuevo = int(nuevo_entry.get().strip())
            if 0 < nuevo <= 100:
                admin_data["configuracion"]["porcentajeAdvertencia"] = nuevo
                guardarAdminData(admin_data)
                resultado_guardado.configure(text=f"Porcentaje actualizado a {nuevo}%.", text_color="green")
            else:
                resultado_guardado.configure(text="Debe estar entre 1 y 100.", text_color="red")
        except ValueError:
            resultado_guardado.configure(text="Debe ser un número válido.", text_color="red")

    ctk.CTkButton(ventana, text="Actualizar", command=actualizar).pack(pady=10)

def mostrar_texto_en_scroll(titulo, contenido):
    ventana = ctk.CTkToplevel()
    ventana.title(titulo)
    ventana.geometry("600x400")

    scroll_frame = ctk.CTkScrollableFrame(ventana, width=580, height=350)
    scroll_frame.pack(pady=10)

    texto = ctk.CTkLabel(scroll_frame, text=contenido, justify="left", anchor="w", wraplength=550)
    texto.pack(padx=10, pady=10)

def mostrar_historial_acciones_gui(root):
    adminData = cargarAdminData()
    historial = adminData.get("historialAcciones", [])

    ventana = ctk.CTkToplevel(root)
    ventana.title("Historial de Acciones")
    ventana.geometry("600x400")

    ctk.CTkLabel(ventana, text="Historial de acciones registradas", font=("Arial", 16)).pack(pady=10)

    scroll_frame = ctk.CTkScrollableFrame(ventana, width=560, height=300)
    scroll_frame.pack(pady=10)

    if not historial:
        ctk.CTkLabel(scroll_frame, text="No hay acciones registradas.").pack(pady=10)
    else:
        for h in historial:
            texto = f"{h['fechaHora']} | {h['usuario']} ({h['rol']}): {h['accion']}"
            ctk.CTkLabel(scroll_frame, text=texto, anchor="w", justify="left").pack(anchor="w", padx=10)

def crear_usuario_gui(root, datos):
    ventana = ctk.CTkToplevel(root)
    ventana.title("Crear Usuario")
    ventana.geometry("400x600")

    ctk.CTkLabel(ventana, text="Crear nuevo usuario", font=("Arial", 16)).pack(pady=10)

    roles = ["Alumno", "Docente", "Administrador"]
    campo_rol = ctk.CTkOptionMenu(ventana, values=roles)
    campo_rol.set("Alumno")
    campo_rol.pack(pady=5)

    # ✅ Frame que contendrá los campos de entrada
    campos_frame = ctk.CTkFrame(ventana)
    campos_frame.pack(pady=10, fill="both", expand=True)

    entradas = {}
    mensaje_label = ctk.CTkLabel(ventana, text="")
    boton_crear = ctk.CTkButton(ventana, text="Crear Usuario")

    def crear():
        rol = campo_rol.get()
        grupo = {"Alumno": "estudiantes", "Docente": "maestros", "Administrador": "administrador"}[rol]

        # Recolectar campos
        usuario = entradas.get("usuario").get().strip()
        contrasena = entradas.get("contrasena").get().strip()  # Nota: esto lo renombramos a "contrasena" abajo
        correo = entradas.get("correo").get().strip()

        if not usuario or not contrasena or not correo:
            mensaje_label.configure(text="Todos los campos son obligatorios.", text_color="red")
            return  # 👈 evita seguir si hay campos vacíos

        if any(u["usuario"] == usuario for u in datos[grupo]):
            mensaje_label.configure(text="El usuario ya existe.", text_color="orange")
            return
        
        # Construcción base del usuario
        nuevo_usuario = {
            "tipoUsuario": rol,
            "usuario": usuario,
            "contrasena": contrasena,
            "correo": correo,
        }

        # Campos adicionales por tipo de usuario
        if rol == "Alumno":
            carnet = entradas.get("carnet").get().strip()
            carrera = entradas.get("carrera").get().strip()
            if not carnet.startswith("KEY_") or not carnet[4:].isdigit() or len(carnet[4:]) != 6:
                mensaje_label.configure(text="Carnet debe ser: KEY_ seguido de 6 dígitos", text_color="red")
                return
            nuevo_usuario.update({
                "carnet": carnet,
                "idEstudiante": carnet[-6:],
                "carrera": carrera,
                "notificaciones": False,
                "actividadesInscritas": []
            })

        elif rol == "Docente":
            nuevo_usuario["asignaciones"] = []

        elif rol == "Administrador":
            nuevo_usuario["nombre"] = entradas.get("nombre").get().strip()

        # Guardar
        datos[grupo].append(nuevo_usuario)
        guardarCambios(datos)
        mensaje_label.configure(text=f"{rol} creado correctamente.", text_color="green")

        # ✅ Limpiar entradas SOLO si se creó correctamente
        for entrada in entradas.values():
            entrada.delete(0, "end")

    def mostrar_campos():
        for widget in campos_frame.winfo_children():
            widget.destroy()

        entradas.clear()
        tipo = campo_rol.get()

        campos = ["usuario", "contrasena", "correo"]
        if tipo == "Alumno":
            campos += ["carnet", "carrera"]
        elif tipo == "Administrador":
            campos += ["nombre"]

        for campo in campos:
            ctk.CTkLabel(campos_frame, text=f"{campo.capitalize()}:").pack(pady=2)
            entrada = ctk.CTkEntry(campos_frame)
            entrada.pack(pady=2)
            entradas[campo] = entrada

        mensaje_label.pack(pady=5)
        boton_crear.configure(command=crear)
        boton_crear.pack(pady=10)

    campo_rol.configure(command=lambda _: mostrar_campos())
    mostrar_campos()

def registrarAccionAdmin(adminData, usuario, rol, accion):
    entrada = {
        "usuario": usuario,
        "rol": rol,
        "accion": accion,
        "fechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    adminData.setdefault("historialAcciones", []).append(entrada)
    guardarAdminData(adminData)

def exportar_base_datos_txt(datos, parent):
    try:
        archivo = "BaseDatosExportada.txt"
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("===== BASE DE DATOS - SISTEMA DE ASISTENCIA COCURRICULAR =====\n\n")

            # Estudiantes
            f.write(">>> ESTUDIANTES:\n")
            for estudiante in datos.get("estudiantes", []):
                f.write(f"- Usuario: {estudiante.get('usuario', '')}\n")
                f.write(f"  Nombre: {estudiante.get('nombre', '')}\n")
                f.write(f"  Correo: {estudiante.get('correo', '')}\n")
                f.write(f"  Intereses: {', '.join(estudiante.get('intereses', []))}\n")
                f.write(f"  Advertencias: {estudiante.get('advertencias', 0)}\n")
                f.write("  Actividades inscritas:\n")
                for a in estudiante.get("actividadesInscritas", []):
                    f.write(f"    - {a.get('nombreActividad')} ({a.get('idActividad')})\n")
                f.write("-" * 50 + "\n")

            # Docentes
            f.write("\n>>> DOCENTES:\n")
            for maestro in datos.get("maestros", []):
                f.write(f"- Usuario: {maestro.get('usuario', '')}\n")
                f.write(f"  Nombre: {maestro.get('nombre', '')}\n")
                f.write(f"  Correo: {maestro.get('correo', '')}\n")
                f.write("-" * 50 + "\n")

            # Administrador
            f.write("\n>>> ADMINISTRADOR:\n")
            for admin in datos.get("administrador", []):
                f.write(f"- Usuario: {admin.get('usuario', '')}\n")
                f.write(f"  Nombre: {admin.get('nombre', '')}\n")
                f.write(f"  Correo: {admin.get('correo', '')}\n")
                f.write("-" * 50 + "\n")

            # Actividades
            f.write("\n>>> ACTIVIDADES:\n")
            for actividad in datos.get("actividades", []):
                f.write(f"- Nombre: {actividad.get('nombreActividad')}\n")
                f.write(f"  ID: {actividad.get('idActividad')}\n")
                f.write(f"  Categoría: {actividad.get('categoria')}\n")
                f.write(f"  Encargado: {actividad.get('personaEncargada')}\n")
                f.write(f"  Detalles: {actividad.get('detalles')}\n")
                f.write(f"  Lugar: {actividad.get('lugar')}\n")
                f.write(f"  Cupos: {actividad.get('cuposMaximos')}\n")
                f.write(f"  Estado: {actividad.get('estado')}\n")
                f.write("  Horario:\n")
                for h in actividad.get("horario", []):
                    f.write(f"    - {h['dia']}: {h['inicio']} a {h['fin']}\n")
                f.write("  Inscritos:\n")
                for inscrito in actividad.get("inscritos", []):
                    f.write(f"    - {inscrito}\n")
                f.write("-" * 50 + "\n")

        # Abrir automáticamente
        os.startfile(archivo)  # Solo en Windows

    except Exception as e:
        ventana_error = ctk.CTkToplevel(parent)
        ventana_error.title("Error")
        ctk.CTkLabel(ventana_error, text=f"Error al exportar base de datos: {e}", text_color="red").pack(pady=10)

class MenuAdministrador(ctk.CTkToplevel):
    def __init__(self, master, tipoUsuario, usuario, datos, adminData):
        super().__init__(master)
        self.master = master
        self.tipoUsuario = tipoUsuario
        self.usuario = usuario
        self.datos = datos
        self.adminData = adminData

        self.title("Menú Administrador")
        self.geometry("500x600")
        self.configure(fg_color="#e6f2ff")

        self.frame_contenedor = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.frame_contenedor.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(
            self.frame_contenedor,
            text=f"Bienvenido/a {usuario}",
            font=("Arial", 22, "bold"),
            text_color="#003366"
        ).pack(pady=(10, 20))

        self.resultado_label = ctk.CTkLabel(self.frame_contenedor, text="")
        self.resultado_label.pack(pady=5)

        # Opciones y botones
        opciones = [
            ("1. Gestión de usuarios", self.menu_gestion_usuarios),
            ("2. Historial de acciones", self.mostrar_historial),
            ("9. Exportar base de datos", lambda: exportar_base_datos_txt(self.datos, self)),
            ("4. Visualizar errores", self.mostrar_errores),
            ("5. Modificar % advertencia", self.modificar_porcentaje),
            ("6. Cerrar sesión", self.cerrar_sesion),
        ]

        for texto, comando in opciones:
            ctk.CTkButton(
                self.frame_contenedor,
                text=texto,
                command=comando,
                fg_color="#0066cc",       # Fondo azul
                text_color="white",       # Texto blanco
                hover_color="#004c99",    # Hover azul oscuro
                corner_radius=15,
                width=300,
                height=40,
                font=("Arial", 14, "bold")
            ).pack(pady=8)

            
    def menu_gestion_usuarios(self):
        subventana = ctk.CTkToplevel(self)
        subventana.title("Gestión de Usuarios")
        subventana.geometry("400x300")
        ctk.CTkLabel(subventana, text="Gestión de usuarios:").pack(pady=10)

        def accion_crear():
            subventana.destroy()
            crear_usuario_gui(self, self.datos)
            registrarAccionAdmin(self.adminData, self.usuario, self.tipoUsuario, "Creó un nuevo usuario")

        def accion_editar():
            subventana.destroy()
            editar_usuario_gui(self, self.datos)
            registrarAccionAdmin(self.adminData, self.usuario, self.tipoUsuario, "Editó un usuario")

        def accion_eliminar():
            subventana.destroy()
            eliminar_usuario_gui(self, self.datos)
            registrarAccionAdmin(self.adminData, self.usuario, self.tipoUsuario, "Eliminó un usuario")

        ctk.CTkButton(subventana, text="Crear Usuario", command=accion_crear).pack(pady=5)
        ctk.CTkButton(subventana, text="Editar Usuario", command=accion_editar).pack(pady=5)
        ctk.CTkButton(subventana, text="Eliminar Usuario", command=accion_eliminar).pack(pady=5)
        ctk.CTkButton(subventana, text="Regresar", command=subventana.destroy).pack(pady=10)

    def mostrar_historial(self):
        historial = self.adminData.get("historialAcciones", [])
        texto = "\n".join([
            f"{h['fechaHora']} | {h['usuario']} ({h['rol']}): {h['accion']}"
            for h in historial
        ]) if historial else "No hay acciones registradas."
        mostrar_texto_en_scroll("Historial de Acciones", texto)

    def mostrar_errores(self):
        errores = self.adminData.get("erroresReportados", [])
        texto = "\n".join([
            f"{e['fecha']} | {e['usuario']}: {e['titulo']} — {e['descripcion']}"
            for e in errores
        ]) if errores else "No hay errores registrados."
        mostrar_texto_en_scroll("Errores Reportados", texto)

    def modificar_porcentaje(self):
        modificar_porcentaje_gui(self, self.adminData)

    def cerrar_sesion(self):
        self.destroy()
        self.master.deiconify()

    # Exportar base de datos
    def exportar_datos(self):
        try:
            with open("adminData_exportado.txt", "w", encoding="utf-8") as archivo:
                archivo.write("=== HISTORIAL DE ACCIONES ===\n")
                for accion in self.adminData.get("historialAcciones", []):
                    archivo.write(f"- Usuario: {accion['usuario']} | Rol: {accion['rol']} | Acción: {accion['accion']} | Fecha: {accion['fechaHora']}\n")
                archivo.write("\n=== ERRORES REPORTADOS ===\n")
                for error in self.adminData.get("erroresReportados", []):
                    archivo.write(f"- Usuario: {error['usuario']} | Título: {error['titulo']} | Descripción: {error['descripcion']} | Fecha: {error['fecha']}\n")
                archivo.write("\n=== CONFIGURACIÓN ===\n")
                config = self.adminData.get("configuracion", {})
                archivo.write(f"- Tolerancia de asistencia: {config.get('toleranciaAsistencia', 'N/A')} minutos\n")
                archivo.write(f"- Porcentaje de advertencia: {config.get('porcentajeAdvertencia', 'N/A')}%\n")
            self.resultado_label.configure(text="Datos exportados a adminData_exportado.txt", text_color="green")
        except Exception as e:
            self.resultado_label.configure(text=f"Error al exportar: {e}", text_color="red")

        # Botones principales con self
        ctk.CTkButton(self, text="1. Gestión de usuarios", command=self.menu_gestion_usuarios).pack(pady=5)
        ctk.CTkButton(self, text="2. Historial de acciones", command=self.mostrar_historial).pack(pady=5)
        ctk.CTkButton(self, text="9. Exportar base de datos", command=self.exportar_datos).pack(pady=5)
        ctk.CTkButton(self, text="4. Visualizar errores", command=self.mostrar_errores).pack(pady=5)
        ctk.CTkButton(self, text="5. Modificar % advertencia", command=self.modificar_porcentaje).pack(pady=5)
        ctk.CTkButton(self, text="6. Cerrar sesión", command=self.cerrar_sesion).pack(pady=20)

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Asistencia Cocurricular - KeyHive")
        self.geometry("600x400")
        self.datos = cargar_datos()

        # Título (siempre se muestra)
        ctk.CTkLabel(self, text="Gestión Cocurricular Key", font=("Arial", 24, "bold")).pack(pady=(0, 15))


        # Título fijo debajo (siempre aparece)
        ctk.CTkLabel(self, text="Gestión Cocurricular Key", font=("Arial", 24, "bold")).pack(pady=10)


        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Usuario", width=300)
        self.usuario_entry.pack(pady=10)

        self.contrasena_entry = ctk.CTkEntry(self, placeholder_text="Contrasena", show="*", width=300)
        self.contrasena_entry.pack(pady=10)

        # Menú desplegable de rol
        self.rol_var = ctk.StringVar(value="Alumno")
        self.rol_dropdown = ctk.CTkOptionMenu(self, values=["Alumno", "Docente", "Administrador"], variable=self.rol_var)
        self.rol_dropdown.pack(pady=10)

        # Botón iniciar sesión
        ctk.CTkButton(self, text="Iniciar sesión", command=self.validar_login).pack(pady=20)

        # Mensaje de error si ocurre
        self.mensaje_label = ctk.CTkLabel(self, text="", text_color="red")
        self.mensaje_label.pack()

        # Frase motivacional
        ctk.CTkLabel(self, text="“Pequeños logros construyen grandes futuros.”", font=("Arial", 12, "italic")).pack(pady=30)

    def validar_login(self):
            usuario = self.usuario_entry.get()
            contrasena = self.contrasena_entry.get()
            rol = self.rol_var.get()

            grupo = {
                "Alumno": "estudiantes",
                "Docente": "maestros",
                "Administrador": "administrador"
            }[rol]

            lista = self.datos.get(grupo, [])
            usuario_encontrado = next((u for u in lista if u["usuario"] == usuario and u["contrasena"] == contrasena), None)

            if usuario_encontrado:
                self.mensaje_label.configure(text="")
                self.withdraw()  # Oculta login

                if rol == "Alumno":
                    AlumnoApp(self, usuario)
                elif rol == "Docente":
                    asistencia = cargar_asistencia()
                    ventana = MenuDocente(self, rol, usuario, self.datos, asistencia)
                    ventana.funciones_docente = DocenteFunciones(ventana, self.datos, asistencia, usuario)
                elif rol == "Administrador":
                    adminData = cargarAdminData()  # Carga adminData
                    ventana = MenuAdministrador(self, rol, usuario, self.datos, adminData)
                    ventana.grab_set()
                else:
                    self.mensaje_label.configure(text="Credenciales inválidas. Intenta de nuevo.")


    def login(self):
        usuario = self.usuario_entry.get().strip()
        contrasena = self.contra_entry.get().strip()
        tipoUsuario = self.tipo_usuario.get()

        datos = cargar_datos()
        grupo = {
            "Alumno": "estudiantes",
            "Docente": "maestros",
            "Administrador": "administrador"
        }.get(tipoUsuario)

        usuarioValido = next((u for u in datos[grupo]
                            if u["usuario"] == usuario and u["contrasena"] == contrasena), None)

        if not usuarioValido:
            self.mensaje.configure(text="Usuario o contraseña incorrectos.")
        else:
            self.withdraw()  # Oculta el login

            if tipoUsuario == "Alumno":
                AlumnoApp(self, usuario)
            elif tipoUsuario == "Docente":
                asistencia = cargar_asistencia()
                menu = MenuDocente(self, tipoUsuario, usuario, datos, asistencia)
                menu.funciones_docente = DocenteFunciones(menu, datos, asistencia, usuario)
            elif tipoUsuario == "Administrador":
                MenuAdministrador(self, tipoUsuario, usuario)


    def abrir_ventana_alumno(self, usuario):
        self.withdraw()  # Oculta la ventana de login
        alumno_ventana = AlumnoApp(usuario, master=self)
        alumno_ventana.mainloop()
        self.deiconify()  # Vuelve a mostrar el login si se cierra la ventana del alumno

def verificarAdvertenciaAsistencia(usuario, idActividad, datos, asistencia, mostrar_ventana=None):
    admin_data = cargarAdminData()
    umbral = admin_data.get("configuracion", {}).get("porcentajeAdvertencia", 80)

    registro = asistencia["registros"].get(idActividad, {})
    canceladas = registro.get("canceladas", [])
    sesiones = registro.get("sesiones", {})

    total_asistencias = sum(
        1 for lista in sesiones.values()
        for reg in lista if reg["usuario"] == usuario
    )

    faltasLista = registro.get("faltas", {}).get(usuario, [])
    faltasValidas = [f for f in faltasLista if f not in canceladas]
    faltasTotales = len(faltasValidas)
    total = total_asistencias + faltasTotales

    if total == 0:
        return False

    porcentaje = (total_asistencias / total) * 100
    advertencias = registro.setdefault("advertenciasEnviadas", {})
    yaEnviado = advertencias.get(usuario, False)

    if porcentaje < umbral and not yaEnviado:
        estudiante = next((e for e in datos["estudiantes"] if e["usuario"] == usuario), None)
        actividadInfo = next((a for a in datos["actividades"] if a["idActividad"] == idActividad), None)
        nombre = actividadInfo.get("nombreActividad", "Desconocida") if actividadInfo else "Desconocida"

        if estudiante:
            mensajeAdvertencia = (
                f"Hola, {usuario},\n\n"
                f"Tu asistencia en la actividad '{nombre}' es del {porcentaje:.0f}%. "
                f"Esto es menor al {umbral}% requerido para acreditar el curso.\n"
                "Te recomendamos asistir a las próximas sesiones para no perder la acreditación.\n\n"
                "Saludos,\n"
                "Asistente de Actividades Cocurriculares"
            )

            try:
                enviarCorreoOutlook(
                    destinatario=estudiante["correo"],
                    asunto="Advertencia de asistencia insuficiente",
                    cuerpo=mensajeAdvertencia
                )
            except Exception as e:
                print(f"Error enviando correo a estudiante {usuario}: {e}")

            if mostrar_ventana:
                mostrar_popup(mostrar_ventana, f"{usuario} tiene asistencia menor al {umbral}% en '{nombre}'", "Advertencia")

        if actividadInfo:
            nombreMaestro = actividadInfo.get("personaEncargado")
            maestro = next((m for m in datos["maestros"] if m["usuario"] == nombreMaestro), None)

            if maestro:
                mensajeMaestro = (
                    f"Hola, {nombreMaestro},\n\n"
                    f"El estudiante {usuario} no ha asistido al menos al {umbral}%, con un {porcentaje:.0f}% de asistencia en la actividad '{nombre}'.\n"
                    "Atentamente,\n"
                    "Asistente de Actividades Cocurriculares"
                )
                try:
                    enviarCorreoOutlook(
                        destinatario=maestro["correo"],
                        asunto=f"Advertencia: Asistencia baja de {usuario}",
                        cuerpo=mensajeMaestro
                    )
                except Exception as e:
                    print(f"Error enviando correo a maestro {nombreMaestro}: {e}")

        advertencias[usuario] = True
        guardarAsistencia(asistencia)
        return True

    return False

# ───── Paso 4 ─────
def registrar_asistencia(usuario, id_actividad, nombre_actividad, horario, asistencia, ventana_padre):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    dia_hoy = datetime.now().strftime("%A")
    dia_hoy_esp = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }[dia_hoy]

    if not horario.startswith(dia_hoy_esp):
        mostrar_popup(ventana_padre, f"Hoy no hay sesión para el horario '{horario}'.", "Día incorrecto")
        return

    if id_actividad not in asistencia["registros"]:
        asistencia["registros"][id_actividad] = {
            "nombreActividad": nombre_actividad,
            "sesiones": {},
            "canceladas": [],
            "faltas": {}
        }

    if fecha_hoy in asistencia["registros"][id_actividad].get("canceladas", []):
        mostrar_popup(ventana_padre, f"La sesión de hoy ({fecha_hoy}) fue cancelada.", "Sesión cancelada")
        return

    sesiones = asistencia["registros"][id_actividad]["sesiones"]
    if horario not in sesiones:
        sesiones[horario] = []

    ya_registrado = any(r["usuario"] == usuario and r["fecha_hora"].startswith(fecha_hoy) for r in sesiones[horario])
    if ya_registrado:
        mostrar_popup(ventana_padre, f"Ya registraste tu asistencia hoy en '{nombre_actividad}'.", "Asistencia duplicada")
        return

    sesiones[horario].append({
        "usuario": usuario,
        "fecha_hora": ahora
    })

    with open(BD_ASISTENCIA, "w", encoding="utf-8") as f:
        json.dump(asistencia, f, indent=2, ensure_ascii=False)

    mostrar_popup(ventana_padre, f"✅ Asistencia registrada para '{nombre_actividad}' a las {ahora}.", "Asistencia registrada")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    evitar_error_focus()  # Evita el error de foco automáticamente
    app = LoginApp()
    app.mainloop()