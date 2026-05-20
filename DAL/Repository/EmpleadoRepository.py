from DAL.Infrastructure.ConexionDB import ConexionDB

class EmpleadoRepository():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

    def RegistrarEmpleado(self,IdEmpleado,Cedula,Nombre,Apellido,Telefono,Email,Contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO EMPLEADO (IDEMPLEADO,CEDULA,NOMBRE,APELLIDO,TELEFONO,EMAIL,CONTRA) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            datos =(IdEmpleado,Cedula,Nombre,Apellido,Telefono,Email,Contra)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "empleado registrado con éxito"
        except Exception as e:
            return False, f"Error al registrar empleado: {e}"

    def verificarEmpleado(self, id, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contra FROM empleado WHERE IDEMPLEADO = %s", (id,))
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

    def obtener_empleado(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT IdEmpleado, Cedula, Nombre, Apellido, Region, Telefono, Email FROM empleado
        """)
        return cursor.fetchall()