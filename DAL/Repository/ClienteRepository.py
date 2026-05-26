from DAL.Infrastructure.ConexionDB import ConexionDB

class ClienteRepository():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

    def RegistrarCliente(self,IdCliente,Cedula,Nombre,Apellido,Telefono,Email,Contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO CLIENTES (ID_CLIENTE,CEDULA,NOMBRE,APELLIDO,TELEFONO,EMAIL,CONTRA) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            datos =(IdCliente,Cedula,Nombre,Apellido,Telefono,Email,Contra)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Cliente registrado con éxito"
        except Exception as e:
            return False, f"Error al registrar cliente: {e}"

    def verificarCliente(self, id, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT Contra FROM clientes WHERE ID_CLIENTE = %s", (id,))
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
        

    def obtener_clientes(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Id_Cliente, Cedula, Nombre, Apellido, Region, Telefono, Email FROM clientes
        """)
        return cursor.fetchall()
    
    def alquilar_vehiculo(conn, id_cliente, id_vehiculo, fecha_inicio, fecha_fin):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alquileres (Id_Cliente, Id_Vehiculo, Fecha_Inicio, Fecha_Fin)
            VALUES (%s, %s, %s, %s)
        """, (id_cliente, id_vehiculo, fecha_inicio, fecha_fin))
        conn.commit()

    def mostrar_clientes(self):
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
