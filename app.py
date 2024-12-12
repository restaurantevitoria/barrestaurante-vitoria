from flask import Flask, render_template, request

app = Flask(__name__)

# Página principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para recibir mensajes del formulario
@app.route("/submit", methods=["POST"])
def submit():
    nombre = request.form.get("nombre")
    mensaje = request.form.get("mensaje")
    return f"Gracias, {nombre}. Hemos recibido tu mensaje: {mensaje}"

if __name__ == "__main__":
    app.run(debug=True)
