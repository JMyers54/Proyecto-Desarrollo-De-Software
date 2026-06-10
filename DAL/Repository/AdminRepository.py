from DAL.Infrastructure.ConexionDB import ConexionDB   
from werkzeug.security import generate_password_hash, check_password_hash 

class AdminRepository():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.db = ConexionDB

    def IniciarSesionAdmin(self, id, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM admin WHERE id_admin = %s", (id,))
                resultado = cursor.fetchone()
            conexion.CerrarConnection()
            if resultado is None:
                return False, "El id no está registrado."
            if check_password_hash(resultado[0], contra):
                return True, ""
            return False, "Contraseña incorrecta."
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"

    def verificarUsuario(self, IdAdmin, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM admin WHERE id_admin = %s", (IdAdmin,))
                resultado = cursor.fetchone()
            conexion.CerrarConnection()
            if resultado is None:
                return False
            return check_password_hash(resultado[0], contra)
        except Exception as e:
            return False
    
    def ObtenerNombreAdmin(self, id_admin):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT NOMBRE, APELLIDO FROM admin WHERE ID_ADMIN = %s", (id_admin,))
                fila = cursor.fetchone()
            conexion.CerrarConnection()
            if fila:
                return f"{fila[0]} {fila[1]}"
            return "Administrador"
        except Exception as e:
            return "Administrador"