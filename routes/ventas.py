from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from proteger import proteger_ruta
from flask_session import Session
from conection import get_db_connection

ventas_bp = Blueprint('ventas', __name__)


mydb = get_db_connection()
cur = mydb.cursor()

def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper

# --------------------------------------------TABLA DE VENTAS-------------------------------------------------

@ventas_bp.route('/ventas')
@proteger_ruta
def listar_empleado():
    try:
        
        s = "SELECT v.idventa, p.nombreproducto, p.precio, v.pago, c.nombrecliente, e.nombreempleado, v.horainicial FROM ventas v inner JOIN empleados e ON v.idempleado = e.idempleado INNER JOIN clientes c ON v.idcliente = c.idcliente INNER JOIN productos p ON v.idproducto = p.idproducto ORDER BY v.horainicial DESC"
        cur.execute(s)
        list_users = cur.fetchall()
        return render_template('ventas.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500