from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

app = Flask(__name__)

# Configura tu servidor SMTP (por ejemplo, Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'tucorreo@gmail.com'  # Tu correo electrónico
SENDER_PASSWORD = 'tupassword'  # La contraseña de tu correo electrónico
RECEIVER_EMAIL = 'correo@restaurante.com'  # Correo donde recibirás las reservas

def enviar_correo(nombre, fecha, hora, personas):
    try:
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = 'Nueva Reserva en Restaurante Vitoria'

        # Cuerpo del mensaje
        cuerpo = f"""
        Nueva reserva:
        
        Nombre: {nombre}
        Fecha: {fecha}
        Hora: {hora}
        Personas: {personas}
        """
        
        msg.attach(MIMEText(cuerpo, 'plain'))

        # Enviar el correo
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Establecer la conexión segura
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reservar', methods=['POST'])
def reservar():
    nombre = request.form['nombre']
    fecha = request.form['fecha']
    hora = request.form['hora']
    personas = request.form['personas']
    
    # Validación básica
    try:
        fecha_hora_reserva = datetime.strptime(f'{fecha} {hora}', '%Y-%m-%d %H:%M')
    except ValueError:
        return "Fecha u hora incorrecta, intenta de nuevo", 400
    
    # Enviar la reserva por correo
    enviar_correo(nombre, fecha, hora, personas)
    
    # Redirigir a una página de confirmación
    return render_template('reserva_confirmada.html', nombre=nombre, fecha=fecha, hora=hora, personas=personas)

if __name__ == '__main__':
    app.run(debug=True)
