from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
import json
from flask_session import Session

mydb = get_db_connection()

productos_bp = Blueprint('productos', __name__)


def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

@productos_bp.route('/productos', methods =['GET'])
@proteger_ruta
def listar_productos():
    try:
        cur = mydb.cursor()
        cur.execute("SELECT * FROM productos ORDER BY idproducto ASC")
        list_users = cur.fetchall()
        return render_template('principalaplicativo.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Agregar producto
@productos_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        if request.method == 'POST':
            nombreproducto = request.form['nombreproducto']
            precio = request.form['precio']
            codigo = request.form['codigo']
            stock = request.form['stock']
            idproveedores = request.form['idproveedores'] 
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO productos (nombreproducto, precio, codigo, cantidad, idproveedores) VALUES (%s, %s, %s, %s, %s)", (nombreproducto, precio,stock, codigo,idproveedores))
            mydb.commit()
            cursor.close()
        return redirect(url_for('productos.listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Editar producto
@productos_bp.route('/editar_producto/<id>')
def get_producto(id):
    try:
        cur = mydb.cursor()
        cur.execute('SELECT*FROM productos WHERE idproducto=%s', (int(float(id)),))
        data=cur.fetchall()
        
        return render_template('edit_producto.html', producto=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@productos_bp.route('/actualizar_producto/<id>', methods=["POST"])
def update_producto(id):
    try:
        if request.method== 'POST':
            nombreproducto=request.form['nombreproducto']
            precio=request.form['precio']
            codigo=request.form['codigo']
            stock = request.form['stock']
            idproveedores = request.form['idproveedores']
            cur = mydb.cursor()
            cur.execute(""" UPDATE productos SET nombreproducto=%s, precio=%s, codigo=%s, cantidad=%s, idproveedores=%s  WHERE idproducto=%s""", (nombreproducto,precio,codigo,stock,idproveedores, id))
            mydb.commit()
            return redirect(url_for('productos.listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Eliminar producto
@productos_bp.route('/eliminar_producto/<int:idproducto>')
def eliminar_producto(idproducto):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM ventas WHERE idproducto = %s", (idproducto,))
        cursor.execute("DELETE FROM productos WHERE idproducto = %s", (idproducto,))
        mydb.commit()
        
        return redirect(url_for('productos.listar_productos'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500



