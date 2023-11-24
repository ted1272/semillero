from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify, session
from conection import get_db_connection
import datetime
from proteger import proteger_ruta
import locale

locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')

arqueocajero = Blueprint('arqueocajero', __name__)

mydb = get_db_connection()

@arqueocajero.route('/arqueocajero')
@proteger_ruta
def listar_arqueo():
    try:
        cur = mydb.cursor()
        idempleado = session.get('idempleado', None)

        if idempleado is not None:
            s = "SELECT * FROM arqueos WHERE idempleado = %s"
            cur.execute(s, (idempleado,))
            list_users = cur.fetchall()
            cur.close()
            
            list_users_formatted = [(user[0], locale.currency(user[1], grouping=True), user[2], user[3]) for user in list_users]

            return render_template('cajero/arqueocajero.html', list_users=list_users_formatted)

    except Exception as ex:
        flash(f"Error: {str(ex)}", 'error')
        return redirect(url_for('arqueocajero.listar_arqueo'))

@arqueocajero.route('/agregar_arqueocajero', methods=['POST'])
def agregar_arqueo():
    try:
        if request.method == 'POST':
            cur = mydb.cursor()
            idempleado = session.get('idempleado', None)

            if idempleado is not None:
                monto = request.form['monto']
                apertura = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cierra = None  

                cur.execute("INSERT INTO arqueos (monto, apertura, cierre, idempleado) VALUES (%s, %s, %s, %s)", (monto, apertura, cierra, idempleado))
                mydb.commit()
                
                # Obtener el ID del arqueo recién insertado
                id_arqueo = cur.lastrowid

                # Almacenar el idarqueo en la sesión
                session['idarqueo_actual'] = id_arqueo

                return redirect(url_for('arqueocajero.listar_arqueo'))   
        
        return render_template('cajero/arqueocajero.html')
    except Exception as ex:
       flash(f"Error: {str(ex)}", 'error')
       return redirect(url_for('arqueocajero.listar_arqueo'))



