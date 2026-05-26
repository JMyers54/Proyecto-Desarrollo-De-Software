from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from DAL.Repository.AdminRepository import AdminRepository
from DAL.Repository.EmpleadoRepository import EmpleadoRepository
from DAL.Repository.ClienteRepository import ClienteRepository
from DAL.Repository.VehiculoRepository import VehiculoRepository
from DAL.Infrastructure.ConexionDB import ConexionDB
from Application.Services.ServicesVehiculos import ServicesVehiculos
from Application.Services.ServicesCliente import ServicesCliente
from Application.Services.ServicesEmpleado import ServicesEmpleado
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

# selección de rol para inicio de sesión
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

#incio de sesión para admin
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')

#Inicio de sesión para empleados
@app.route('/empleado')
def empleado():
    if 'empleado' not in session:
        return redirect(url_for('login'))
    return render_template('empleado.html')

#Inicio de sesión para clientes
@app.route('/cliente')
def cliente():
    if 'cliente' not in session:
        return redirect(url_for('login'))
    return render_template('cliente.html')

#Registro de empleado solo para admin
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

#Registro de cliente solo para empleados
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
    

#Registro de vehiculo solo para admin
@app.route("/registro_vehiculo")
def registro_vehiculo():
    if "admin" not in session:
        return redirect(url_for("login"))
    return render_template("registerVehiculo.html")

@app.route("/registro_vehiculo", methods=["POST"])
def registrar_vehiculo_post():
    if "admin" not in session:
        return redirect(url_for("login"))
    IdVehiculo = request.form['IdVehiculo']
    Marca = request.form['Marca']
    Modelo = request.form['Modelo']
    Año = request.form['Año']
    Tipo = request.form['Tipo']
    Precio_diario = request.form['Precio_diario']
    Estado = request.form['Estado']
    success, message = vehiculo_repo.RegistroVehiculos(IdVehiculo, Marca, Modelo, Año, Tipo, Precio_diario, Estado)
    flash(message)
    if success:
        return redirect(url_for("admin"))
    else: 
        return redirect(url_for("registro_vehiculo"))
    
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
#Alquiler de vehículos para clientes
@app.route('/alquilar')
def vista_alquilar():
    return render_template('AlquilarVehiculo.html')

@app.route('/api/vehiculos/actualizar', methods=['POST'])
def actualizar_vehiculo():
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401
    data = request.get_json(force=True)
    ok, message = vehiculo_repo.ActualizarVehiculo(
        data['idVehiculo'], data['marca'], data['modelo'], 
        data['año'], data['tipo'], data['precio_diario'], data['estado']
    )
    if ok:
        return jsonify({"message": message})
    return jsonify({"error": message}), 500

@app.route('/api/vehiculos/eliminar', methods=['POST'])
def eliminar_vehiculo():
    if 'admin' not in session:
        return jsonify({"error": "No autorizado"}), 401
    data = request.get_json(force=True)
    ok, message = vehiculo_repo.EliminarVehiculo(
        data['idVehiculo']
    )
    if ok:
        return jsonify({"message": message})
    return jsonify({"error": message}), 500
if __name__ == '__main__':
    app.run(debug=True)