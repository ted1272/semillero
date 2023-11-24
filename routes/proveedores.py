from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from proteger import proteger_ruta
from flask_session import Session
from conection import get_db_connection

proveedores_bp = Blueprint('proveedores', __name__)


mydb = get_db_connection()


@proveedores_bp.route('/proveedores')
@proteger_ruta
def proveedores():
    try:    
        cur = mydb.cursor()
        s="SELECT* FROM proveedores ORDER BY idproveedores ASC"
        cur.execute(s)
        list_users=cur.fetchall()
        return render_template('proveedores.html' ,list_users=list_users  )
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


@proveedores_bp.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    try:  
        if request.method == 'POST':
            nombrepro = request.form['nombre']
            nit = request.form['nit']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO proveedores (nombrepro, nit, direccion, telefono) VALUES (%s, %s, %s, %s)", (nombrepro, nit, direccion, telefono))
            mydb.commit()
            cursor.close()
        return redirect(url_for('proveedores.proveedores'))  
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Editar un proveedor
@proveedores_bp.route('/editar_proveedores/<id>')
def get_contact(id):
    try:  
        cur = mydb.cursor()
        cur.execute('SELECT*FROM proveedores WHERE idproveedores=%s', (int(float(id)),))
        data=cur.fetchall()
        return render_template('edit_proveedores.html', proveedores=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

@proveedores_bp.route('/actualizar/<id>', methods=["POST"])
def update_contact(id):
    try: 
        if request.method == 'POST':
            nombrepro = request.form['nombre']
            nit = request.form['nit']
            direccion = request.form['direccion']
            telefono = request.form['telefono']
            cur = mydb.cursor()
            cur.execute("""UPDATE proveedores SET nombrepro=%s, nit=%s, direccion=%s, telefono=%s  WHERE idproveedores=%s""", (nombrepro, nit, direccion, telefono, id))
            mydb.commit()
            return redirect(url_for('proveedores.proveedores'))  # Cambia 'proveedores' a 'proveedores.proveedores'
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500


# Eliminar un proveedor
@proveedores_bp.route('/eliminar_proveedores/<string:id>')
def delete_contact(id):
    try:
        cur = mydb.cursor()
        cur.execute('DELETE FROM proveedores WHERE idproveedores = %s', (id,))
        cur.close()
        return redirect(url_for('proveedores.proveedores'))  # Cambia 'proveedores' a 'proveedores.proveedores'
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500