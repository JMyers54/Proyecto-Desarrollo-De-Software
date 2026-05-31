from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from DAL.Repository.AdminRepository import AdminRepository
from DAL.Repository.EmpleadoRepository import EmpleadoRepository
from DAL.Repository.ClienteRepository import ClienteRepository
from DAL.Repository.VehiculoRepository import VehiculoRepository
from DAL.Infrastructure.ConexionDB import ConexionDB
from Application.Services.ServicesVehiculos import ServicesVehiculos
from Application.Services.ServicesCliente import ServicesCliente
from Application.Services.ServicesEmpleado import ServicesEmpleado
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__, template_folder='Presentation/templates', static_folder='Presentation/static')   
app.secret_key = 'your_secret_key_here'  # Cambia esto por una clave secreta segura

modelo = ConexionDB()
admin_repo = AdminRepository(None, modelo)
empleado_repo = EmpleadoRepository(None, modelo)
cliente_repo = ClienteRepository(None, modelo)
vehiculo_repo = VehiculoRepository(None, modelo)
vehiculo_service = ServicesVehiculos(modelo)
empleado_service = ServicesEmpleado(modelo)
cliente_service = ServicesCliente(modelo)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('seleccionar_rol.html')

@app.route('/login/<rol>', methods=['GET', 'POST'])
def login_rol(rol):
    if request.method == 'POST':
        id_user = request.form['id']
        contra = request.form['contra']
        
        if rol == 'admin':
            success, message = admin_repo.IniciarSesionAdmin(id_user, contra)
            if success:
                session['admin'] = id_user
                return redirect(url_for('admin'))
        elif rol == 'empleado':
            success, message = empleado_repo.verificarEmpleado(id_user, contra)
            if success:
                session['empleado'] = id_user
                return redirect(url_for('empleado'))
        elif rol == 'cliente':
            success, message = cliente_repo.verificarCliente(id_user, contra)
            if success:
                session['cliente'] = id_user
                return redirect(url_for('cliente'))
        else:
            message = "Rol no válido."
        
        flash(message)
        return redirect(url_for('login_rol', rol=rol))
    
    return render_template('login.html', rol=rol)

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/empleado')
def empleado():
    if 'empleado' not in session:
        return redirect(url_for('login'))
    return render_template('empleado.html')

@app.route('/cliente')
def cliente():
    if 'cliente' not in session:
        return redirect(url_for('login'))
    return render_template('cliente.html')

@app.route('/registrar_empleado')
def registrar_form():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('registerEmpleado.html')

@app.route('/registrar_empleado', methods=['POST'])
def registrar():
    if 'admin' not in session:
        return redirect(url_for('login'))
    IdEmpleado = request.form['IdEmpleado']
    Cedula = request.form['Cedula']
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    Telefono = request.form['Telefono']
    Email = request.form['Email']
    Contra = request.form['Contra']
    success, message = empleado_repo.RegistrarEmpleado(IdEmpleado, Cedula, Nombre, Apellido, Telefono, Email, Contra)
    flash(message)
    if success:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('registrar_form'))

@app.route("/registrar_cliente")
def registrar_cliente():
    if "empleado" not in session:
        return redirect(url_for("login"))
    return render_template("registerCliente.html")

@app.route("/registrar_cliente", methods=["POST"])
def registrar_clien():
    if "empleado" not in session:
        return redirect(url_for("login"))
    IdCliente = request.form['IdCliente']
    Cedula = request.form['Cedula']
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    Telefono = request.form['Telefono']
    Email = request.form['Email']
    Contra = request.form['Contra']
    success, message = cliente_repo.RegistrarCliente(IdCliente,Cedula,Nombre,Apellido,Telefono,Email,Contra)
    flash(message)
    if success:
        return redirect(url_for("empleado"))
    else: 
        return redirect(url_for("registrar_cliente"))

@app.route("/registro_vehiculo", methods=["GET", "POST"])
def registro_vehiculo():
    if "admin" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        Marca = request.form["Marca"]
        Modelo = request.form["Modelo"]
        Año = request.form["Año"]
        Tipo = request.form["Tipo"]
        Precio_diario = request.form["Precio_diario"]
        Estado = request.form["Estado"]
        archivo_foto = request.files.get("Imagen")
        nombre_final_imagen = "default.jpg"
        if archivo_foto and archivo_foto.filename != "":
            nombre_final_imagen = secure_filename(archivo_foto.filename)
            carpeta_uploads = os.path.join(app.root_path,"static","uploads")
            os.makedirs(carpeta_uploads, exist_ok=True)
            ruta_imagen = os.path.join(carpeta_uploads,nombre_final_imagen)
            archivo_foto.save(ruta_imagen)
        success, message = vehiculo_repo.RegistroVehiculos( Marca, Modelo, Año, Tipo, Precio_diario, Estado, nombre_final_imagen)
        flash(message)
        if success:
            return redirect(url_for("admin"))
        return redirect(url_for("registro_vehiculo"))
    return render_template("registerVehiculo.html")

@app.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('empleado', None)
    session.pop('cliente', None)
    return redirect(url_for('index'))

# Vista de inventario para empleados y clientes
@app.route('/inventario')
def vista_inventario():
    return render_template('Inventario.html')

@app.route('/api/vehiculos')
def api_vehiculos():
    try:
        return jsonify(vehiculo_service.listar_vehiculos())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clientes')
def vista_clientes():
    return render_template('clientes.html')
@app.route('/api/clientes')
def api_clientes():
    try:
        return jsonify(cliente_service.listar_clientes())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/empleados')
def vista_empleados():
    return render_template('empleados.html')

@app.route('/api/empleados')
def api_empleados():
    try:
        return jsonify(empleado_service.listar_empleados())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================================================================
# NUEVAS RUTAS CORREGIDAS PARA LA EDICIÓN Y ELIMINACIÓN DE VEHÍCULOS
@app.route('/api/vehiculos/actualizar/<idVehiculo>', methods=['GET'])
def form_actualizar_vehiculo(idVehiculo):
    if "admin" not in session:
        return redirect(url_for("login"))
    todos = vehiculo_service.listar_vehiculos()
    carro = next((c for c in todos if str(c.get('id') or c.get('IdVehiculo')) == str(idVehiculo)), None)#coincidencias en el iD
    if not carro:
        flash("Vehículo no encontrado.")
        return redirect(url_for("vista_inventario"))
    return render_template("ActualizarVehiculo.html", carro=carro)    # Renderiza la interfaz oscura que acabamos de crear pasándole el objeto 'carro'

@app.route('/api/vehiculos/guardar/<idVehiculo>', methods=['POST'])
def guardar_actualizacion_vehiculo(idVehiculo):
    if 'admin' not in session:
        return redirect(url_for("login"))

    marca = request.form.get('marca')
    modelo = request.form.get('modelo')
    año = request.form.get('año')
    color = request.form.get('color')
    tipo = request.form.get('tipo')
    precio_diario = request.form.get('precio')
    estado = request.form.get('estado')
    km = request.form.get('km')
    combustible = request.form.get('combustible')
    transmision = request.form.get('transmision')
    motor = request.form.get('motor')
    observaciones = request.form.get('observaciones')
    ok, message = vehiculo_repo.ActualizarVehiculo(idVehiculo,marca,modelo,año, color,tipo,precio_diario,estado,km,combustible,transmision,motor,observaciones)
    flash(message)
    return redirect(url_for("vista_inventario"))

@app.route('/api/vehiculos/eliminar/<idVehiculo>', methods=['POST'])# 3. ELIMINAR VEHÍCULO ASÍNCRONAMENTE (LLAMADO POR EL FETCH DE JAVASCRIPT)
def eliminar_vehiculo_api(idVehiculo):
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401
    ok, message = vehiculo_service.eliminaVehiculo(idVehiculo)
    if ok:
        return jsonify({"message": message}), 200
    return jsonify({"error": message}), 500

@app.route('/alquilar/Inventario', methods=['GET'])
def vista_alquilar(): 
    lista_carros = vehiculo_repo.obtener_todos_los_vehiculos()  
    return render_template('alquilarVehiculo.html', vehiculos=lista_carros)#le damos la lista al html

@app.route('/no_disponible')
def form_no_disponible():
    return render_template('no_disponible.html')

@app.route('/alquilar/<int:idVehiculo>')
def VehiculoDisponible(idVehiculo):
    vehiculo = vehiculo_repo.ObtenerVehiculoPorId(idVehiculo)
    return render_template('FormAlquilar.html', idVehiculo=idVehiculo, vehiculo=vehiculo)

@app.route('/verificar_disponibilidad/<int:idVehiculo>', methods=['POST'])
def verificar_disponibilidad(idVehiculo):
    # 1. Asegurar que haya un cliente en sesión utilizando la clave correcta del login
    if 'cliente' not in session:
        flash("Debes iniciar sesión como cliente para poder alquilar un vehículo.")
        return redirect(url_for('login'))
        
    id_cliente = session.get('cliente')
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    
    # 2. Validar disponibilidad en el rango de fechas
    disponible = vehiculo_repo.VerificarDisponibilidad(idVehiculo, fecha_inicio, fecha_fin)
    if disponible > 0:
        return redirect(url_for('form_no_disponible'))
        
    # 3. Obtener el vehículo para conocer su precio por día
    vehiculo = vehiculo_repo.ObtenerVehiculoPorId(idVehiculo)
    if not vehiculo:
        flash("El vehículo seleccionado no existe.")
        return redirect(url_for('vista_alquilar'))
        
    precio_dia = float(vehiculo[2])
    
    # 4. Calcular la cantidad de días del alquiler
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dias = (fin - inicio).days + 1
    
    # Calcular el total base inicial
    total = dias * precio_dia
    
    # 5. REGLA DE NEGOCIO: Aplicar descuento del 10% si tiene 5 o más alquileres anteriores
    cantidad_alquileres = cliente_repo.contar_alquileres_cliente(id_cliente)
    if cantidad_alquileres >= 5:
        total = total * 0.90  # Aplica el 10% de descuento reduciendo el monto al 90%
        flash("¡Felicidades! Se ha aplicado un 10% de descuento automático por ser cliente frecuente.")
        
    # 6. Guardar el alquiler con el total ya rebajado y actualizar el estado del carro
    cliente_repo.alquilar_vehiculo(id_cliente, idVehiculo, fecha_inicio, fecha_fin, total)
    vehiculo_repo.AlquilaVehiculo(idVehiculo)
    
    return redirect(url_for('VehiculoDisponible', idVehiculo=idVehiculo))


@app.route('/confirmar_alquiler/<int:idVehiculo>', methods=['POST'])
def confirmar_alquiler(idVehiculo):
    # 1. Asegurar la sesión del cliente
    if 'cliente' not in session:
        return "No autorizado. Inicie sesión.", 401
        
    id_cliente = session.get('cliente')
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    
    # 2. Obtener precio diario del vehículo
    vehiculo = vehiculo_repo.ObtenerVehiculoPorId(idVehiculo)
    if not vehiculo:
        return "Vehículo no encontrado", 404
        
    precio_dia = float(vehiculo[2])
    
    # 3. Calcular los días y el monto total base
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dias = (fin - inicio).days + 1
    total = dias * precio_dia
    
    # 4. REGLA DE NEGOCIO: Validar historial para el beneficio del 10%
    cantidad_alquileres = cliente_repo.contar_alquileres_cliente(id_cliente)
    if cantidad_alquileres >= 5:
        total = total * 0.90
        
    # 5. Persistir datos en la base de datos
    cliente_repo.alquilar_vehiculo(id_cliente, idVehiculo, fecha_inicio, fecha_fin, total)
    vehiculo_repo.AlquilaVehiculo(idVehiculo)
    
    return "Alquiler registrado correctamente"

if __name__ == '__main__':
    app.run(debug=True)
