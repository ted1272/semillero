from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
import json
from flask_session import Session

cliente_bp = Blueprint('cliente', __name__)


mydb = get_db_connection()

def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

#Client vista
@cliente_bp.route('/cliente')
@proteger_ruta
def listar_cliente():
    
        cur = mydb.cursor()
        cur.execute("SELECT * FROM clientes")
        cliente = cur.fetchall()
        cur.close()
        return render_template('clientes.html', cliente=cliente)
   

#Agregar cliente 
@cliente_bp.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    try:
        if request.method == 'POST':
            nombrecliente = request.form['nombre']
            telefonoc = request.form['telefono']
            direccionc = request.form['direccion']
            mydb.commit()
            cur = mydb.cursor()
            cur.execute("INSERT INTO clientes (nombrecliente, telefono, direccion) VALUES (%s, %s, %s)", (nombrecliente, telefonoc, direccionc))
            mydb.commit()
            cur.close()
        return redirect(url_for('cliente.listar_cliente'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


#----------------------------------------------------------------------------------------------
@cliente_bp.route('/editar_cliente/<idcliente>')
def get_cliente(idcliente):
    try:
        cur = mydb.cursor()
        cur.execute('SELECT * FROM clientes WHERE idcliente=%s', (int(float(idcliente)),))
        data = cur.fetchall()
        cur.close()
        if data:
            return render_template('edit_cliente.html', cliente=data[0])
        else:
            return jsonify({'mensaje': "Cliente no encontrado"}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@cliente_bp.route('/actualizar_cliente/<id>', methods=["POST"])
def update_cliente(id):
    try:
        if request.method == 'POST':
            nombrecliente = request.form['nombre']
            telefono = request.form['telefono']
            direccion = request.form['direccion']
            cur = mydb.cursor()
            cur.execute("""UPDATE clientes SET nombrecliente=%s, telefono=%s, direccion=%s WHERE idcliente=%s""",
                        (nombrecliente, telefono, direccion, id))
            mydb.commit()
            cur.close()
            return redirect(url_for('cliente.listar_cliente'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@cliente_bp.route('/eliminar_cliente/<int:idcliente>')
def eliminar_cliente(idcliente):
    try:
        cur = mydb.cursor()
        cur.execute("DELETE FROM clientes WHERE idcliente = %s", (idcliente,))
        mydb.commit()
        cur.close()
        return redirect(url_for('cliente.listar_cliente'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500