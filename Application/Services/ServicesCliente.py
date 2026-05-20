from DAL.Infrastructure.ConexionDB import ConexionDB
class ServicesCliente():
    def __init__(self, modelo):
        self.modelo = modelo
    def listar_clientes(self):
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                conn = conexion.getConnection()
                cursor = conn.cursor()
                cursor.execute("SELECT Id_Cliente, Cedula, Nombre, Apellido, Region, Telefono, Email FROM clientes")
                filas = cursor.fetchall()
                return [
                    {
                        "id":     f[0],
                        "cedula": str(f[1]),
                        "nombre": f[2],
                        "apellido": f[3],
                        "region": f[4],
                        "telefono": f[5],
                        "email": f[6]
                    }
                    for f in filas
                ]
            except Exception as e:
                raise e
            finally:
                self.modelo.CerrarConnection()