from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify, Response
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
from datetime import datetime, date, timedelta


app = Flask(__name__, template_folder='Presentation/templates', static_folder='Presentation/static')   
app.secret_key = 'your_secret_key_here'  # Cambia esto por una clave secreta segura
app.permanent_session_lifetime = timedelta(minutes=30)  # Sesión expira después de 30 minutos de inactividad

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
    lista_carros = vehiculo_repo.obtener_todos_los_vehiculos()
    return render_template('index.html', vehiculos=lista_carros)

@app.route('/login')
def login():
    lista_carros = vehiculo_repo.obtener_todos_los_vehiculos()
    return render_template('seleccionar_rol.html', vehiculos=lista_carros)

@app.route('/login/<rol>', methods=['GET', 'POST'])
def login_rol(rol):
    if request.method == 'POST':
        id_user = request.form['id']
        contra = request.form['contra']
        
        if rol == 'admin':
            success, message = admin_repo.IniciarSesionAdmin(id_user, contra)
            if success:
                session.permanent = True  # La sesión se mantendrá activa según el tiempo definido en app.permanent_session_lifetime
                session['admin'] = id_user
                return redirect(url_for('admin'))
        elif rol == 'empleado':
            success, message = empleado_repo.verificarEmpleado(id_user, contra)
            if success:
                session.permanent = True  # La sesión se mantendrá activa según el tiempo definido en app.permanent_session_lifetime
                session['empleado'] = id_user
                return redirect(url_for('empleado'))
        elif rol == 'cliente':
            success, message = cliente_repo.verificarCliente(id_user, contra)
            if success:
                session.permanent = True  # La sesión se mantendrá activa según el tiempo definido en app.permanent_session_lifetime
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
    id_admin = session.get('admin')
    nombre = admin_repo.ObtenerNombreAdmin(id_admin)
    return render_template('admin.html', nombre=nombre)

@app.route('/empleado')
def empleado():
    if 'empleado' not in session:
        return redirect(url_for('login'))
        
    id_empleado = session.get('empleado')
    # Usamos los métodos del repositorio
    nombre_empleado = empleado_repo.ObtenerNombreEmpleado(id_empleado)
    alquileres_asignados = empleado_repo.ObtenerHistorialAlquileres(id_empleado)
    
    return render_template('empleado.html', nombre=nombre_empleado, alquileres=alquileres_asignados)

# === PASO 6: RUTA PARA PROCESAR LA DEVOLUCIÓN (RN-01) ===
@app.route('/devolucion/<int:id_alquiler>')
def registrar_devolucion(id_alquiler):
    if 'empleado' not in session:
        return redirect(url_for('login'))
        
    exito, mensaje = empleado_repo.RegistrarDevolucion(id_alquiler)
    flash(mensaje) # Por si manejas mensajes flash en tu interfaz
    return redirect(url_for('empleado'))

@app.route('/cliente')
def cliente():
    if 'cliente' not in session:
        return redirect(url_for('login'))
    id_cliente = session.get('cliente')
    nombre = cliente_repo.ObtenerNombreCliente(id_cliente)
    alquileres_activos = cliente_repo.contar_alquileres_cliente(id_cliente)
    # 1. Traemos todas las reservas de este cliente desde tu repositorio real
    reservas_cliente = cliente_repo.ObtenerHistorialCliente(id_cliente)
    # 2. Le pasamos las reservas y la fecha de hoy (en formato texto ISO: YYYY-MM-DD) al HTML
    return render_template('cliente.html', 
                            nombre=nombre, 
                            alquileres_activos=alquileres_activos, 
                            reservas=reservas_cliente, 
                            hoy=date.today().isoformat())

@app.route('/registrar_empleado')
def registrar_form():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('registerEmpleado.html')

@app.route('/registrar_empleado', methods=['POST'])
def registrar():
    if 'admin' not in session:
        return redirect(url_for('login'))
    Cedula = request.form['Cedula']
    Nombre = request.form['Nombre']
    Apellido = request.form['Apellido']
    Telefono = request.form['Telefono']
    Email = request.form['Email']
    Contra = request.form['Contra']
    success, message = empleado_repo.RegistrarEmpleado(Cedula, Nombre, Apellido, Telefono, Email, Contra)
    flash(message)
    if success:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('registrar_form'))

def RegistrarCliente(self, Cedula, Nombre, Apellido, Telefono, Email, Contra, NumLicencia, FechaVencimientoLicencia):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()

            # Generar ID único automático
            cursor.execute("SELECT COUNT(*) FROM CLIENTES")
            total = cursor.fetchone()[0]
            IdCliente = f"CL-{total + 1:03d}"   # CL-001, CL-002, ...

            sql = """INSERT INTO CLIENTES 
                        (ID_CLIENTE, CEDULA, NOMBRE, APELLIDO, TELEFONO, EMAIL, CONTRA, NUM_LICENCIA, FECHA_VENCIMIENTO_LICENCIA) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            datos = (IdCliente, Cedula, Nombre, Apellido, Telefono, Email, Contra, NumLicencia, FechaVencimientoLicencia)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Cliente registrado con éxito"
        except Exception as e:
            return False, f"Error al registrar cliente: {e}"


# ── ROUTES (reemplaza los 4 routes en app.py) ─────────────────────────────────

@app.route("/registrar_cliente")
def registrar_cliente():
    if "empleado" not in session:
        return redirect(url_for("login"))
    return render_template("registerCliente.html")

@app.route("/registrar_cliente", methods=["POST"])
def registrar_clien():
    if "empleado" not in session:
        return redirect(url_for("login"))
    Cedula      = request.form['Cedula']
    Nombre      = request.form['Nombre']
    Apellido    = request.form['Apellido']
    Telefono    = request.form['Telefono']
    Email       = request.form['Email']
    Contra      = request.form['Contra']
    NumLicencia              = request.form['NumLicencia']
    FechaVencimientoLicencia = request.form['FechaVencimientoLicencia']

    success, message = cliente_repo.RegistrarCliente(
        Cedula, Nombre, Apellido, Telefono, Email, Contra,
        NumLicencia, FechaVencimientoLicencia
    )
    flash(message)
    if success:
        return redirect(url_for("empleado"))
    else:
        return redirect(url_for("registrar_cliente"))

@app.route("/se_registrar_cliente")
def cliente_se_registra():
    return render_template("ClienteSeRegistra.html")   # sin verificar sesión: aún no tiene

@app.route("/se_registrar_cliente", methods=["POST"])
def cliente_registra():
    Cedula      = request.form['Cedula']
    Nombre      = request.form['Nombre']
    Apellido    = request.form['Apellido']
    Telefono    = request.form['Telefono']
    Email       = request.form['Email']
    Contra      = request.form['Contra']
    NumLicencia              = request.form['NumLicencia']
    FechaVencimientoLicencia = request.form['FechaVencimientoLicencia']

    success, message = cliente_repo.RegistrarCliente(
        Cedula, Nombre, Apellido, Telefono, Email, Contra,
        NumLicencia, FechaVencimientoLicencia
    )
    flash(message)
    if success:
        return redirect(url_for("login_rol", rol="cliente"))   # va a hacer login con sus datos
    else:
        return redirect(url_for("cliente_se_registra"))

@app.route("/registro_vehiculo", methods=["GET", "POST"])
def registro_vehiculo():
    if "admin" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        Marca = request.form["Marca"]
        Placa = request.form["Placa"]
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
        success, message = vehiculo_repo.RegistroVehiculos( Marca, Placa, Modelo, Año, Tipo, Precio_diario, Estado, nombre_final_imagen)
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

@app.route('/empleado/inventario')
def vista_inventario_empleado():
    return render_template('InventarioEmpleado.html')

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

# =========================================================================
# RUTAS DE ALQUILER CORREGIDAS
# =========================================================================

@app.route('/alquilar/Inventario', methods=['GET'])
def vista_alquilar(): 
    lista_carros = vehiculo_repo.obtener_todos_los_vehiculos()  
    return render_template('alquilarVehiculo.html', vehiculos=lista_carros, fecha_hoy=date.today().isoformat())

@app.route('/no_disponible')
def form_no_disponible():
    return render_template('no_disponible.html')

@app.route('/alquilar/<int:idVehiculo>', methods=['GET', 'POST'])
def VehiculoDisponible(idVehiculo):
    vehiculo = vehiculo_repo.ObtenerVehiculoPorId(idVehiculo)
    lista_empleados = empleado_repo.obtener_asesores_disponibles()
    return render_template('FormAlquilar.html', 
                            idVehiculo=idVehiculo, 
                            vehiculo=vehiculo, 
                            lista_empleados=lista_empleados)

@app.route('/api/vehiculos/<int:idVehiculo>/fechas_ocupadas')
def fechas_ocupadas(idVehiculo):
    rangos = vehiculo_repo.ObtenerFechasOcupadas(idVehiculo)
    return jsonify(rangos)

@app.route('/verificar_disponibilidad/<int:idVehiculo>', methods=['POST'])
def verificar_disponibilidad(idVehiculo):
    if 'cliente' not in session:
        flash("Debes iniciar sesión como cliente para poder alquilar un vehículo.")
        return redirect(url_for('login'))
        
    id_cliente = session.get('cliente')
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    
    # IMPORTANTE: Recargar los datos del vehículo y asesores por si hay que redibujar la página por un error
    vehiculo = vehiculo_repo.ObtenerVehiculoPorId(idVehiculo)
    lista_asesores = empleado_repo.obtener_asesores_disponibles()
    
    # 1. Validar orden de las fechas
    if fecha_inicio > fecha_fin:
        flash("La fecha de inicio no puede ser posterior a la fecha de fin.")
        return render_template('FormAlquilar.html', idVehiculo=idVehiculo, vehiculo=vehiculo, lista_empleados=lista_asesores)
        
    # 2. Verificar disponibilidad real en la base de datos
    coincidencias = vehiculo_repo.VerificarDisponibilidad(idVehiculo, fecha_inicio, fecha_fin)
    if coincidencias > 0:
        flash("El vehículo no está disponible para las fechas seleccionadas. Por favor, elige otro rango.")
        return render_template('FormAlquilar.html', idVehiculo=idVehiculo, vehiculo=vehiculo, lista_empleados=lista_asesores)
        
    # 3. Si todo está correcto, proceder al cálculo del precio total
    if not vehiculo:
        flash("El vehículo seleccionado no existe.")
        return redirect(url_for('vista_alquilar'))
        
    try:
        precio_dia = float(vehiculo[2]) if isinstance(vehiculo, (tuple, list)) else float(vehiculo.get('Precio_diario', 0))
    except Exception:
        flash("Error al procesar el precio del vehículo.")
        return redirect(url_for('vista_alquilar'))
        
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dias = (fin - inicio).days + 1
    total = dias * precio_dia
    
    # Control local de la alerta del descuento para evitar que flote en cualquier parte
    tiene_descuento = False
    cantidad_alquileres = cliente_repo.contar_alquileres_cliente(id_cliente)
    if cantidad_alquileres > 0 and cantidad_alquileres % 5 == 0:  # Cada 5 alquileres, el próximo tiene descuento
        total = total * 0.90
        tiene_descuento = True
        # Eliminamos el flash genérico para evitar que se pinte de manera global y rompa la experiencia
    
    # Avanza a la pantalla de confirmación final enviando los parámetros exactos que el HTML necesita
    return render_template('FormAlquilar.html', 
                           idVehiculo=idVehiculo, 
                           vehiculo=vehiculo, 
                           fecha_inicio=fecha_inicio, 
                           fecha_fin=fecha_fin, 
                           dias=dias, 
                           total=total, 
                           lista_empleados=lista_asesores,
                           tiene_descuento=tiene_descuento)
@app.route('/confirmar_alquiler/<int:idVehiculo>', methods=['POST'])
def confirmar_alquiler(idVehiculo):
    print(dict(request.form))
    if 'cliente' not in session:
        return "No autorizado. Inicie sesión.", 401
        
    id_cliente = session.get('cliente')
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    id_empleado = request.form['IdEmpleado']

    print(f"id_cliente: {id_cliente}")
    print(f"id_empleado: {id_empleado}")
    print(f"fecha_inicio: {fecha_inicio}")
    print(f"fecha_fin: {fecha_fin}")
    print(f"idVehiculo: {idVehiculo}")
    # Volvemos a validar disponibilidad de última hora antes de guardar
    disponible = vehiculo_repo.VerificarDisponibilidad(idVehiculo, fecha_inicio, fecha_fin)
    if disponible > 0:
        flash("Lo sentimos, el vehículo ya no se encuentra disponible.")
        return redirect(url_for('VehiculoDisponible', idVehiculo=idVehiculo))
    
    # SEGURIDAD CRÍTICA: Recalcular el total en el servidor para evitar manipulaciones en el HTML
    vehiculo = vehiculo_repo.ObtenerVehiculoPorId(idVehiculo)
    if not vehiculo:
        flash("Error: El vehículo ya no existe.")
        return redirect(url_for('vista_alquilar'))
        
    try:
        precio_dia = float(vehiculo[2]) if isinstance(vehiculo, (tuple, list)) else float(vehiculo.get('Precio_diario', 0))
    except Exception:
        flash("Error interno al procesar el costo.")
        return redirect(url_for('vista_alquilar'))
        
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    dias = (fin - inicio).days + 1
    total_servidor = dias * precio_dia
    
    # Aplicar el descuento en el backend también
    cantidad_alquileres = cliente_repo.contar_alquileres_cliente(id_cliente)
    if cantidad_alquileres > 0 and cantidad_alquileres % 5 == 0:
        total_servidor = total_servidor * 0.90
        
    # Guardamos DEFINITIVAMENTE con el precio verificado por el servidor
    exito = vehiculo_repo.AlquilaVehiculo(id_cliente, idVehiculo, id_empleado, fecha_inicio, fecha_fin, total_servidor)
    
    if exito:
        flash("¡Alquiler registrado con éxito!")
    else:
        flash("Error interno al registrar el alquiler en la base de datos.")
        
    return redirect(url_for('vista_alquilar'))

@app.route('/api/empleado/estadisticas/<id_empleado>')
def api_estadisticas_empleado(id_empleado):
    stats = empleado_repo.ObtenerEstadisticasAsesor(id_empleado)
    return jsonify(stats)

@app.route('/api/cliente/historial/<id_cliente>')
def api_historial_cliente(id_cliente):
    historial = cliente_repo.ObtenerHistorialCliente(id_cliente)
    return jsonify(historial)

@app.route('/historial_cliente')
def historial_cliente():
    if 'cliente' not in session:
        return redirect(url_for('login'))
    from datetime import date
    id_cliente = session.get('cliente')
    historial = cliente_repo.ObtenerHistorialCliente(id_cliente)
    return render_template('HistorialCliente.html', historial=historial, hoy=str(date.today()))

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/api/dashboard')
def api_dashboard():
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    datos = cliente_repo.ObtenerDatosDashboard(fecha_inicio, fecha_fin)
    return jsonify(datos)

@app.route('/backup')
def backup():
    if 'admin' not in session:
        return redirect(url_for('login'))
    try:
        modelo.CrearConnection()
        conn = modelo.getConnection()
        cursor = conn.cursor()

        sql_backup = "-- Backup ALQUILER_VEHICULOS\n\n"

        tablas = ['ADMIN', 'EMPLEADO', 'CLIENTES', 'VEHICULOS', 'ALQUILERES']

        for tabla in tablas:
            sql_backup += f"-- Tabla: {tabla}\n"
            cursor.execute(f"SELECT * FROM {tabla}")
            filas = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]

            for fila in filas:
                valores = []
                for v in fila:
                    if v is None:
                        valores.append("NULL")
                    elif isinstance(v, str):
                        valores.append(f"'{v.replace(chr(39), chr(39)+chr(39))}'")
                    else:
                        valores.append(str(v))
                sql_backup += f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({', '.join(valores)});\n"
            sql_backup += "\n"

        cursor.close()
        modelo.CerrarConnection()

        return Response(
            sql_backup,
            mimetype='text/plain',
            headers={'Content-Disposition': 'attachment; filename=backup.sql'}
        )
    except Exception as e:
        flash(f"Error al generar backup: {e}")
        return redirect(url_for('admin'))

@app.route('/cancelar_alquiler/<int:id_alquiler>', methods=['POST'])
def cancelar_alquiler(id_alquiler):
    if 'cliente' not in session:
        return redirect(url_for('login'))
        
    id_cliente = session.get('cliente')
    # Tu lógica de repositorio
    success, message = cliente_repo.CancelarAlquiler(id_alquiler, id_cliente)
    
    # Categoría 'exito' o 'error' para filtrar en el HTML
    categoria = 'exito' if success else 'error'
    flash(message, categoria)
    
    return redirect(url_for('historial_cliente'))

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/editar_alquiler/<int:id_alquiler>', methods=['POST'])
def editar_alquiler(id_alquiler):
    if 'cliente' not in session:
        return redirect(url_for('login'))
        
    id_cliente = session.get('cliente')
    nueva_fecha_inicio = request.form.get('fecha_inicio')
    nueva_fecha_fin = request.form.get('fecha_fin')
    
    if nueva_fecha_inicio and nueva_fecha_fin:
        f_inicio = datetime.strptime(nueva_fecha_inicio, '%Y-%m-%d')
        f_fin = datetime.strptime(nueva_fecha_fin, '%Y-%m-%d')

        fecha_hoy = datetime.combine(date.today(), datetime.min.time()) # Hoy a las 00:00
        if f_inicio < fecha_hoy:
            flash('Error: No puedes seleccionar una fecha de inicio anterior a hoy.')
            return redirect(url_for('historial_cliente'))
        
        if f_inicio > f_fin:
            flash('Error: La fecha de inicio no puede ser posterior a la fecha de fin.')
            return redirect(url_for('historial_cliente'))
            
    try:
        # Nos conectamos a la base de datos usando tu infraestructura ConexionDB
        modelo.CrearConnection()
        conn = modelo.getConnection()
        cursor = conn.cursor()
        
        # Actualizamos las fechas del alquiler asegurando que pertenezca al cliente en sesión
        sql = """
            UPDATE ALQUILERES 
            SET FECHA_INICIO = %s, FECHA_FIN = %s 
            WHERE ID_ALQUILER = %s AND ID_CLIENTE = %s
        """
        cursor.execute(sql, (nueva_fecha_inicio, nueva_fecha_fin, id_alquiler, id_cliente))
        conn.commit()
        
        cursor.close()
        modelo.CerrarConnection()
        
        flash('¡Reserva modificada con éxito!')
    except Exception as e:
        flash(f'Error al modificar la reserva: {e}')
        
    return redirect(url_for('historial_cliente'))
if __name__ == '__main__':
    app.run(debug=True)
