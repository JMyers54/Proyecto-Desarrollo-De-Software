from DAL.Infrastructure.ConexionDB import ConexionDB   
from werkzeug.security import generate_password_hash, check_password_hash 

class AdminRepository():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.db = ConexionDB

    def IniciarSesionAdmin(self, cedula, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM admin WHERE CEDULA = %s", (cedula,))
                resultado = cursor.fetchone()
            conexion.CerrarConnection()
            if resultado is None:
                return False, "La cédula no está registrada."
            if check_password_hash(resultado[0], contra):
                return True, ""
            return False, "Contraseña incorrecta."
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"

    def verificarUsuario(self, Cedula, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM admin WHERE CEDULA = %s", (Cedula,))
                resultado = cursor.fetchone()
            conexion.CerrarConnection()
            if resultado is None:
                return False
            return check_password_hash(resultado[0], contra)
        except Exception as e:
            return False
    
    def ObtenerNombreAdmin(self, Cedula):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT NOMBRE, APELLIDO FROM admin WHERE CEDULA = %s", (Cedula,))
                fila = cursor.fetchone()
            conexion.CerrarConnection()
            if fila:
                return f"{fila[0]} {fila[1]}"
            return "Administrador"
        except Exception as e:
            return "Administrador"