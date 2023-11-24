from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from conection import get_db_connection
from proteger import proteger_ruta
from flask_session import Session

# Obtener la conexión y el cursor
mydb = get_db_connection()
cur = mydb.cursor()

# Crear el Blueprint
empleado_bp = Blueprint('empleado', __name__)



# Listar empleados
@empleado_bp.route('/empleado')
@proteger_ruta
def listar_empleado():
    try:
        mostrar = "SELECT * FROM empleados ORDER BY idempleado ASC"
        cur.execute(mostrar)
        list_users = cur.fetchall()
        return render_template('empleado.html', list_users=list_users)
    except Exception as ex:
        return jsonify({'mensaje': f"Error al listar empleados: {str(ex)}"}), 500

# Agregar empleado
@empleado_bp.route('/agregar_empleado', methods=['POST'])
def agregar_empleado():
    try:
        if request.method == 'POST':
            nombreempleado = request.form['nombreempleado']
            cargo = request.form['cargo']
            correo = request.form['correo']
            usuario = request.form['usuario']
            clave = request.form['clave']
            
            cur.execute("INSERT INTO empleados (nombreempleado, cargo, correo, usuario, clave) VALUES (%s, %s, %s, %s, %s)", (nombreempleado, cargo, correo, usuario, clave))
            mydb.commit()
            return redirect(url_for('empleado.listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error al agregar empleado: {str(ex)}"}), 500

# Editar empleado
@empleado_bp.route('/editar_empleado/<id>')
def get_empleado(id):
    try:
        cur.execute('SELECT * FROM empleados WHERE idempleado=%s', (int(float(id)),))
        data = cur.fetchall()
        return render_template('edit_empleado.html', empleado=data[0])
    except Exception as ex:
        return jsonify({'mensaje': f"Error al obtener empleado: {str(ex)}"}), 500

# Actualizar empleado
@empleado_bp.route('/actualizar_empleado/<id>', methods=["POST"])
def update_empleado(id):
    try:
        if request.method == 'POST':
            nombreempleado = request.form['nombreempleado']
            cargo = request.form['cargo']
            correo = request.form['correo']
            usuario = request.form['usuario']
            clave = request.form['clave']
            
            cur.execute("""UPDATE empleados SET nombreempleado=%s, cargo=%s, correo=%s, usuario=%s, clave=%s WHERE idempleado=%s""", (nombreempleado, cargo, correo, usuario, clave, id))
            mydb.commit()
            return redirect(url_for('empleado.listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error al actualizar empleado: {str(ex)}"}), 500

# Eliminar empleado
@empleado_bp.route('/eliminar_empleado/<int:idempleado>')
def eliminar_empleado(idempleado):
    try:
        cur.execute("DELETE FROM empleados WHERE idempleado = %s", (idempleado,))
        mydb.commit()
        return redirect(url_for('empleado.listar_empleado'))
    except Exception as ex:
        return jsonify({'mensaje': f"Error al eliminar empleado: {str(ex)}"}), 500


