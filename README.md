
Proyecto: Control de Asistencia a Actividades Co-curriculares - KeyHive

Grupo conformado por: Joceline Ayala, Rebeca Castro, Edwin Hernández, Gustavo Cardona y Daniella Campos

Descripción
Este proyecto fue desarrollado con el propósito de mejorar la gestión de asistencia en actividades co-curriculares dentro del entorno educativo, es decir, Key Institute. A través de una interfaz intuitiva y moderna, la cual permite a los maestros llevar un control claro, ordenado y digitalizado de los participantes que asisten a actividades organizadas fuera del currículo tradicional.

Objetivo
El principal objetivo de este sistema es facilitar y optimizar el registro de asistencia de estudiantes, haciendo uso de tecnologías accesibles como archivos locales. De esta manera:

- Se reduce el uso de papel y procesos manuales.
- Se garantiza una mayor precisión en el registro.
- Se fomenta el compromiso del estudiante con las actividades extracurriculares.
- Se mejora la organización y seguimiento por parte del personal docente o administrativo.

Este proyecto está pensado especialmente para instituciones educativas que desean modernizar sus procesos y fomentar la participación estudiantil de una forma clara y eficiente.

Instrucciones para Ejecutar

1. Requisitos

Antes de ejecutar el programa, asegurarse de tener Python 3.x instalado. Luego, instalar las dependencias necesarias con el siguiente comando:

pip install customtkinter qrcode opencv-python


2. Archivos principales del proyecto

- iniciosesionv2.py: archivo principal para ejecutar el sistema.
- BaseDatos.json: contiene la base de datos de usuarios registrados.
- AsistenciaDatos.json: guarda los registros de asistencia por actividad.
- AdminData.json: gestiona las credenciales y datos del administrador.

3. Ejecución - Instrucciones

Desde la terminal, ubícate en la carpeta del proyecto y ejecuta:

python iniciosesionv2.py

Esto abrirá una interfaz gráfica amigable donde se podrá:

- Iniciar sesión como estudiante, docente o administrador

- Escanear códigos QR para registrar asistencia

- Inscribirse o gestionar actividades

- Visualizar y exportar reportes semanales

- Publicar noticias o cancelar sesiones

- Visualizar historial y advertencias


Librerías utilizadas

- customtkinter: para crear una interfaz gráfica moderna y personalizable.
- qrcode: para la generación de códigos QR únicos por usuario.
- opencv-python (cv2): para escanear los QR con la cámara.
- smtplib y email.message: para el envío automático de reportes por correo electrónico.
- json: para la gestión local de bases de datos.

Consideraciones adicionales

- Se necesita una cámara activa para escanear los códigos QR.
- El envío de correos requiere conexión a Internet y una cuenta de envío configurada en el código.
- Los reportes se generan automáticamente en formato .txt y se almacenan localmente.
- Las credenciales de administrador deben estar definidas en AdminData.json.

Este proyecto demuestra cómo la tecnología puede ser una aliada poderosa para modernizar procesos dentro del ámbito educativo, promoviendo así un entorno más organizado, eficiente y comprometido con el desarrollo integral del estudiante.