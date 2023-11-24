from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify, url_for


from flask_caching import Cache

from routes.productos import productos_bp
from routes.proveedores import proveedores_bp
from routes.empleado import empleado_bp
from routes.clientes import cliente_bp
from routes.arqueo import arqueo_bp
from routes.ventas import ventas_bp
from routes.cajavendedor import cajavendedor_bp
from routes.gastos import gastos_bp
from routes.caja import caja_bp
from routes.accesos import accesos_bp
from routes.arqueocajero import arqueocajero
from routes.cajacajero import cajacajero_bp
from routes.gastoscajero import gastoscajero


import json
from conection import get_db_connection
from proteger import proteger_ruta

from routes.accesos import accesos_bp
import json
from conection import get_db_connection
from proteger import proteger_ruta

app = Flask(__name__)
app.secret_key = 'semillero'
cache = Cache(app)

# Configuración de la caché
app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)

mydb = get_db_connection()

app.register_blueprint(productos_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(empleado_bp)
app.register_blueprint(arqueo_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(gastos_bp)
app.register_blueprint(arqueocajero)
app.register_blueprint(gastoscajero)
app.register_blueprint(accesos_bp)
app.register_blueprint(caja_bp)
app.register_blueprint(cajacajero_bp)
app.register_blueprint(cajavendedor_bp)

def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salir')
def salir():
    session.pop('logueado', None)
    session.pop('username', None)
    
    return redirect(url_for('index'))

@app.route('/login')
def login():
    cache.clear()
    return render_template('login.html')

@app.route('/caja')
@proteger_ruta
def caja():
    return render_template('caja.html')


@app.route('/hacer_login', methods=["POST", "GET"])
def hacer_login():
    try:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            correo = request.form['username']
            password = request.form['password']
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM empleados WHERE usuario = %s AND clave = %s', (correo, password))
            account = mycursor.fetchone()

            if account:
                account_dict = dict(zip(mycursor.column_names, account))
                id_empleado = account[0]
                nombre_empleado = account[1]
                session['logueado'] = True
                session['username'] = correo
                session['cargo'] = account_dict['cargo']
                session['idempleado'] = id_empleado
                session['nombre_empleado'] = nombre_empleado
                if session['cargo'] == "administrador":
                    return redirect(url_for('ventas.listar_empleado'))
                elif session['cargo'] == "vendedor":
                    return redirect(url_for('cajavendedor.cajavendedor'))
                elif session['cargo'] == "cajero": 
                    return redirect(url_for('arqueocajero.listar_arqueo', idempleado = id_empleado))
            else:
                flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
                
        else:
           
            flash('Falta el nombre de usuario o la contraseña.', 'error')
    except Exception as ex:
        flash(f"Error: {str(ex)}", 'error')
    
        return render_template('login.html')

def paginanoencontrada(error):
    return "<h1>La página que intenta encontrar no existe<h1>", 404

if __name__ == "__main__":
    app.register_error_handler(404, paginanoencontrada)
    app.run(debug=True, port=5000)
   