from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from conection import get_db_connection
from datetime import datetime, date

cajavendedor_bp = Blueprint('cajavendedor', __name__)

mydb = get_db_connection()
def proteger_ruta(func):
    def wrapper(*args, **kwargs):
        if 'logueado' in session and session['logueado']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrapper.__name__ = func.__name__
    return wrapper


def arqueo():
    cur = mydb.cursor()

    cur.execute("SELECT idarqueo FROM arqueos ORDER BY idarqueo DESC LIMIT 1")
    arqueo = cur.fetchone()

    if arqueo:
        id_arqueo = arqueo[0]
        return id_arqueo
    else:
        return "No se encontró ningún registro de arqueo"

def obtener_clientes():
    cur = mydb.cursor()
    cur.execute("SELECT idcliente, nombrecliente FROM clientes")
    clientes = cur.fetchall()
    cur.close()
    return clientes


@cajavendedor_bp.route('/cajavendedor', methods=['GET'])
@proteger_ruta
def cajavendedor():
    cur = mydb.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    cur.close()

    clientes = obtener_clientes()  
    total_carrito = suma()  
    carrito = mostrarcarrito()  

    render_result = render_template('vendedor/cajavendedor.html', productos=productos, clientes=clientes, total_carrito=total_carrito, carrito=carrito)

    return render_result

@cajavendedor_bp.route('/clienteht_vendedor', methods=['POST'])
@proteger_ruta
def clienteht():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        cliente_nombre = request.form.get('cliente_nombre')

        session['cliente_id'] = cliente_id
        session['cliente_nombre'] = cliente_nombre
        
    return redirect(url_for('cajavendedor.cajavendedor'))


@cajavendedor_bp.route('/agregar_cajavendedor', methods=['POST'])
@proteger_ruta
def agregar_cajavendedor():
    try:
        if request.method == 'POST':
            id_producto = request.form['idproducto']
            nombre = request.form['nombre']
            fecha_hora = datetime.now()
            precio1 = request.form['precio']
            cantidad = request.form['cantidad']
            precio = float(precio1) * int(cantidad)
            id_empleado = session.get('idempleado') 
            nombre_empleado = session.get('nombre_empleado')
            id_aqueo = arqueo()
            cliente_id = session.get('cliente_id')
            cliente_nombre = session.get('cliente_nombre')
            print(id_empleado)
            print(nombre_empleado)
            cur = mydb.cursor()
            cur.execute("INSERT INTO carrito (idproducto, nombre, hora, valor, cantidad, idempleado, empleado ,idaqueo,idcliente, nombrecliente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (id_producto, nombre, fecha_hora, precio, cantidad, id_empleado, nombre_empleado ,id_aqueo ,cliente_id ,cliente_nombre))
            mydb.commit()
            cur.close()
            return redirect(url_for('cajavendedor.cajavendedor'))
    except Exception as e:
        print(f"Error en la ruta /agregar_cajavendedor: {str(e)}")
        return jsonify({'mensaje': f"Error: {str(e)}"}), 500

@cajavendedor_bp.route('/mostrarsuma', methods=['POST'])
@proteger_ruta
def suma():
    cliente_id = session.get('cliente_id')
    cur = mydb.cursor()
    cur.execute("SELECT SUM(valor) FROM carrito WHERE idcliente= %s", (cliente_id,))
    total_valor = cur.fetchone()[0] 
    cur.close()

    return total_valor

@cajavendedor_bp.route('/eliminar_carrito/<int:idcarrito>')
def eliminar_carrito(idcarrito):
    try:
        cur = mydb.cursor()
        cur.execute("DELETE FROM carrito WHERE idcarrito = %s", (idcarrito,))
        mydb.commit()
        cur.close()
        return redirect(url_for('vendedor/cajavendedor.cajavendedor'))  
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {str(ex)}"}), 500



@cajavendedor_bp.route('/mostrarcarrito', methods=['POST'])
@proteger_ruta
def mostrarcarrito():
    cliente_id = session.get('cliente_id')
    cur = mydb.cursor()
    cur.execute("SELECT * FROM carrito WHERE idcliente=%s ", (cliente_id,)) 
    carrito = cur.fetchall()
    cur.close()

    return carrito

@cajavendedor_bp.route('/convertir_venta_cajavendedor', methods=['POST'])
@proteger_ruta
def convertir_venta_cajavendedor():
    cliente_id = session.get('cliente_id')
    horafinal = datetime.now()
    data = request.get_json()  
    medio_pago = data.get('medioPago')
    
    cur = mydb.cursor()
    cur.execute("SELECT idproducto, hora, valor, cantidad, idempleado, idaqueo, idcliente FROM carrito WHERE idcliente=%s ", (cliente_id,))
    carrito = cur.fetchall()
    cur.close()

    cur = mydb.cursor()
    cur.execute("SELECT idproducto, cantidad FROM carrito WHERE idcliente=%s ", (cliente_id,))
    productos_en_carrito = cur.fetchall()

   
    cantidades_vendidas = {}

    for producto in productos_en_carrito:
        id_producto = producto[0]
        cantidad_vendida = producto[1]
        cantidades_vendidas[id_producto] = cantidad_vendida

    datos_venta = []
    for producto in carrito:
        id_producto = producto[0]
        hora = producto[1]  
        valor = producto[2]  
        cantidad = producto[3]
        id_empleado = producto[4]
        id_arqueo = producto[5]
        id_cliente = producto[6]

        datos_venta.append((medio_pago, valor, hora, horafinal, id_producto, id_empleado, id_arqueo, id_cliente))

    cur = mydb.cursor()
    for dato in datos_venta:
        cur.execute("INSERT INTO ventas (pago, valor, horainicial, horafinal, idproducto, idempleado, idarqueo, idcliente) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", dato)
    
    for id_producto, cantidad_vendida in cantidades_vendidas.items():
        cur.execute("UPDATE productos SET cantidad = cantidad - %s WHERE idproducto = %s", (cantidad_vendida, id_producto))
    
    cur.execute("DELETE FROM carrito WHERE idcliente=%s", (cliente_id,))
    
    mydb.commit()
    cur.close()

    return render_template('vendedor/cajavendedor.html')

