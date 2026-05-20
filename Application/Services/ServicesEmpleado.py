from DAL.Infrastructure.ConexionDB import ConexionDB
class ServicesEmpleado():
    def __init__(self, modelo):
        self.modelo = modelo

    def listar_empleados(self):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            conn = conexion.getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT IdEmpleado, Cedula, Nombre, Apellido,Region,Telefono, Email FROM empleado")
            filas = cursor.fetchall()
            return [
                {
                    "id":     f[0],
                    "cedula": str(f[1]),
                    "nombre": f[2],
                    "apellido": f[3],
                    "region": str(f[4]),
                    "telefono": f[5],
                    "email": f[6],
                }
                for f in filas
            ]
        except Exception as e:
            raise e
        finally:
            self.modelo.CerrarConnection()
