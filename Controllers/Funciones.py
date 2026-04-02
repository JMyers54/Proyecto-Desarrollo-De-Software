from Models.ConexionDB import ConexionDB

class Funciones():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

    def IniciarSesionAdmin(self, id,contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM admin WHERE id_admin = %s",(id,))
                resultado = cursor.fetchone()
            
            conexion.CerrarConnection()
            if resultado is None:
                return False, "El id no esta registrado."
            if resultado[0] == contra:
                return True, ""
            else:
                return False, "Contraseña Incorrecta."
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"
        
    def RegistrarEmpleado(self,IdEmpleado,Cedula,Nombre,Apellido,Telefono,Email,Contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO EMPLEADO (ID_EMPLEADO,CEDULA,NOMBRE,APELLIDO,TELEFONO,EMAIL,CONTRA) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            datos =(IdEmpleado,Cedula,Nombre,Apellido,Telefono,Email,Contra)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "empleado registrado con éxito"
        except Exception as e:
            return False, f"Error al registrar empleado: {e}"

    def agregarVehiculo(self, id, marca, modelo, año, tipo, precio_diario, estado, imagen):
        pass

    def verificarEmpleado(self, id, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contra FROM empleado WHERE ID_EMPLEADO = %s", (id,))
                resultado = cursor.fetchone()
            
            conexion.CerrarConnection()
            if resultado is None:
                return False, "El id no está registrado."
            if resultado[0] == contra:
                return True, ""
            else:
                return False, "Contraseña Incorrecta."
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"

    def verificarCliente(self, id, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contra FROM cliente WHERE ID_CLIENTE = %s", (id,))
                resultado = cursor.fetchone()
            
            conexion.CerrarConnection()
            if resultado is None:
                return False, "El id no está registrado."
            if resultado[0] == contra:
                return True, ""
            else:
                return False, "Contraseña Incorrecta."
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"