from flask import Blueprint, request, redirect, url_for, jsonify, render_template
from conection import get_db_connection
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mydb = get_db_connection()
accesos_bp = Blueprint('crearaccesos', __name__)

# Función para generar contraseña
def generar_contrasena(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena

# Función para enviar el correo
def enviar_correo(correo, contrasena):
    smtp_server = 'smtp.gmail.com'  # Servidor SMTP de Gmail
    smtp_port = 587  # Puerto de Gmail
    smtp_user = 'crmbusinesscontrol@gmail.com'  
    smtp_pass = 'mohg blwy uifr kota'  #Contraseña generada para aplicaciones

    # Mensaje del correo
    subject = 'BusinessControl - Contraseña generada'
    message = f'Gracis por registrarse a nuestro aplicativo Tu nueva contraseña es: {contrasena}      .Podras ingresar dando clic en el siguiente enlace: '

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = correo
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Conexión al servidor SMTP y envíar el correo
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, correo, msg.as_string())

@accesos_bp.route('/accesos', methods=['POST'])
def accesos():
    try:
        if request.method == 'POST':
            nombreempleado = request.form['nombreempleado']
            cargo = request.form['cargo']
            correo = request.form['correo']
            usuario = request.form['usuario']
            # Contraseña aleatoria de 6 caracteres
            clave = generar_contrasena(6)
            cur = mydb.cursor()
            cur.execute("INSERT INTO empleados (nombreempleado, cargo, correo, usuario, clave) VALUES (%s, %s, %s, %s, %s)", (nombreempleado, cargo, correo, usuario, clave))
            mydb.commit()
            # Envia la contraseña al correo ingresado por el usuario
            enviar_correo(correo, clave)
            cur.close()

            return render_template('login.html')
    except Exception as ex:
        return jsonify({'mensaje': f"Error al enviar credenciales {str(ex)}"}), 500

