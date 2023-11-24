from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify, session
from conection import get_db_connection
import datetime
from proteger import proteger_ruta
from flask_caching import Cache
import locale

locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')


arqueo_bp = Blueprint('arqueo', __name__)

# Obtener la conexión de la base de datos y el cursor
mydb = get_db_connection()


# Mostrar la tabla de arqueo
@arqueo_bp.route('/arqueo')
@proteger_ruta
def listar_arqueo():
    try:
        cur = mydb.cursor()
        idempleado = session.get('idempleado', None)
        if idempleado is not None:
            s = "SELECT arqueos.idarqueo, arqueos.monto,arqueos.apertura,arqueos.cierre, empleados.nombreempleado FROM arqueos INNER JOIN empleados ON arqueos.idempleado = empleados.idempleado;"
            cur.execute(s)
            list_users = cur.fetchall()
            cur.close()
            list_users_formatted = [(user[0], locale.currency(user[1], grouping=True), user[2], user[3], user[4]) for user in list_users]
            return render_template('arqueo.html', list_users=list_users_formatted)
    except Exception as ex:
        flash(f"Error: {str(ex)}", 'error')
        return redirect(url_for('listar_arqueo'))

# Agregar Caja
@arqueo_bp.route('/agregar_arqueo', methods=['POST'])
def agregar_arqueo():
    try:
        if request.method == 'POST':
            cur = mydb.cursor()
            idempleado = session.get('idempleado', None)

            if idempleado is not None:
                monto = request.form['monto']
                # Capturar la fecha y hora actual al momento de la apertura
                apertura = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cierra = None  # Establecer como None inicialmente, ya que se registrará al momento del cierre
                
        
                cur.execute("INSERT INTO arqueos (monto, apertura, cierre, idempleado) VALUES (%s, %s, %s, %s)", (monto, apertura, cierra, idempleado))
                mydb.commit()
                cur.close()
                 # Obtener el ID del arqueo recién insertado
                id_arqueo = cur.lastrowid

                # Almacenar el idarqueo en la sesión
                session['idarqueo_actual'] = id_arqueo
                return redirect(url_for('arqueo.listar_arqueo'))
        return render_template('arqueo.html')  
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
    
@arqueo_bp.route('/editar_arqueo/<id>')
def get_contact(id):
    try:  
        cur = mydb.cursor()
        cur.execute('SELECT*FROM arqueos WHERE idarqueo=%s',  (int(float(id)),))
        data=cur.fetchall()
        return render_template('edit_arqueo.html', arqueo=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
@arqueo_bp.route('/actualizar_arqueo/<int:idarqueo>', methods=['POST'])
def actualizar_arqueo(idarqueo):
    try:
        if request.method == 'POST':
            cur = mydb.cursor()
            monto = request.form['monto']
            # Capturar la fecha y hora actual al momento del cierre
            cierra = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            idempleado = request.form['idempleado']

            cur.execute("UPDATE arqueos SET monto=%s, cierra=%s, idempleado=%s WHERE idarqueo=%s", (monto, cierra, idempleado, idarqueo))
            mydb.commit()
            cur.close()
        return redirect(url_for('arqueo.listar_arqueo'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500

#Eliminar arqueo
@arqueo_bp.route('/eliminar_arqueo/<int:idarqueo>')
def eliminar_arqueo(idarqueo):
    try:
        cur = mydb.cursor()
        cur.execute("DELETE FROM arqueos WHERE idarqueo = %s", (idarqueo,))
        mydb.commit()
        cur.close()
        return redirect(url_for('arqueo.listar_arqueo'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500
