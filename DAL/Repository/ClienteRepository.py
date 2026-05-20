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
