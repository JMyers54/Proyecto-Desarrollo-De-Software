from DAL.Infrastructure.ConexionDB import ConexionDB
from werkzeug.security import generate_password_hash, check_password_hash

class EmpleadoRepository():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

    def RegistrarEmpleado(self, Cedula, Nombre, Apellido, Telefono, Email, Contra):
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                cursor = db.cursor()

                cursor.execute("SELECT COALESCE(MAX(IDEMPLEADO), 0) FROM EMPLEADO")
                ultimo = int(cursor.fetchone()[0])
                IdEmpleado = ultimo + 1

                contra_hash = generate_password_hash(Contra)

                sql = "INSERT INTO EMPLEADO (IDEMPLEADO,CEDULA,NOMBRE,APELLIDO,TELEFONO,EMAIL,CONTRA) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                datos = (IdEmpleado, Cedula, Nombre, Apellido, Telefono, Email, contra_hash)
                cursor.execute(sql, datos)
                db.commit()
                cursor.close()
                conexion.CerrarConnection()
                return True, "Empleado registrado con éxito"
            except Exception as e:
                return False, f"Error al registrar empleado: {e}"

    def verificarEmpleado(self, Cedula, contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT CONTRA FROM empleado WHERE CEDULA = %s", (Cedula,))
                resultado = cursor.fetchone()
            conexion.CerrarConnection()
            if resultado is None:
                return False, "La cédula no está registrada."
            if check_password_hash(resultado[0], contra):
                return True, ""
            return False, "Contraseña incorrecta."
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"


    def obtener_empleado(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT IdEmpleado, Cedula, Nombre, Apellido, Region, Telefono, Email FROM empleado
        """)
        return cursor.fetchall()

    def mostrar_empleados(self):
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

    def ObtenerEstadisticasAsesor(self, id_empleado):
            """Devuelve el total de carros alquilados y el total de clientes únicos atendidos"""
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                cursor = db.cursor()
                
                # 1. Cuántos carros ha alquilado bajo su asesoría
                sql_carros = "SELECT COUNT(*) FROM ALQUILERES WHERE ID_EMPLEADO = %s"
                cursor.execute(sql_carros, (id_empleado,))
                total_carros = cursor.fetchone()[0]
                
                # 2. Cuántos clientes únicos han alquilado con él
                sql_clientes = "SELECT COUNT(DISTINCT ID_CLIENTE) FROM ALQUILERES WHERE ID_EMPLEADO = %s"
                cursor.execute(sql_clientes, (id_empleado,))
                total_clientes = cursor.fetchone()[0]
                
                cursor.close()
                conexion.CerrarConnection()
                
                return {
                    'total_carros': total_carros,
                    'total_clientes': total_clientes
                }
            except Exception as e:
                print("Error en estadísticas del asesor:", e)
                return {'total_carros': 0, 'total_clientes': 0}

    def ObtenerHistorialAlquileres(self, id_empleado):
        """Devuelve las filas detalladas para armar la tabla del historial"""
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            
            # Consulta con JOINs para traer los nombres reales del cliente y los datos del carro
            sql = """
                SELECT 
                    A.ID_ALQUILER,
                    C.NOMBRE AS NOMBRE_CLIENTE,
                    C.APELLIDO AS APELLIDO_CLIENTE,
                    V.MARCA,
                    V.MODELO,
                    A.FECHA_INICIO,
                    A.FECHA_FIN,
                    A.TOTAL
                FROM ALQUILERES A
                INNER JOIN CLIENTES C ON A.ID_CLIENTE = C.ID_CLIENTE
                INNER JOIN VEHICULOS V ON A.ID_VEHICULO = V.ID_VEHICULO
                WHERE A.ID_EMPLEADO = %s
                ORDER BY A.FECHA_INICIO DESC
            """
            cursor.execute(sql, (id_empleado,))
            historial = cursor.fetchall()
            
            cursor.close()
            conexion.CerrarConnection()
            return historial
        except Exception as e:
            print("Error al obtener historial:", e)
            return []

    def obtener_asesores_disponibles(self):
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                cursor = db.cursor()
                sql = "SELECT IdEmpleado, Nombre, Apellido FROM empleado ORDER BY Nombre ASC"
                cursor.execute(sql)
                asesores = cursor.fetchall()
                cursor.close()
                conexion.CerrarConnection()
                return asesores
            except Exception as e:
                print("\n" + "!"*40)
                print(f"ERROR CRÍTICO EN EMPLEADOREPOSITORY: {e}")
                print("!"*40 + "\n")
                return []
    
    def ObtenerNombreEmpleado(self, Cedula):
        """Devuelve el nombre completo del empleado logueado"""
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            cursor.execute("SELECT NOMBRE, APELLIDO FROM EMPLEADO WHERE CEDULA = %s", (Cedula,))
            res = cursor.fetchone()
            cursor.close()
            conexion.CerrarConnection()
            return f"{res[0]} {res[1]}" if res else "Asesor"
        except Exception as e:
            print("Error al obtener nombre del empleado:", e)
            return "Asesor"

    def RegistrarDevolucion(self, id_alquiler):
            """Paso 6: Borrado directo y liberación del vehículo en cascada manual"""
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                cursor = db.cursor()
                
                # 1. Primero sacamos el ID del vehículo antes de borrar la fila del alquiler
                cursor.execute("SELECT ID_VEHICULO FROM ALQUILERES WHERE ID_ALQUILER = %s", (id_alquiler,))
                resultado = cursor.fetchone()
                
                if resultado:
                    id_vehiculo = resultado[0]
                    print(f"--> [DEBUG]: Encontrado Alquiler #{id_alquiler}. Vehículo a liberar: {id_vehiculo}")
                    
                    # 2. Borramos el alquiler
                    cursor.execute("DELETE FROM ALQUILERES WHERE ID_ALQUILER = %s", (id_alquiler,))
                    
                    # 3. Colocamos el carro disponible
                    cursor.execute("UPDATE VEHICULOS SET ESTADO = 'Disponible' WHERE ID_VEHICULO = %s", (id_vehiculo,))
                    
                    db.commit()
                    print("--> [DEBUG]: Commit realizado con éxito en la base de datos.")
                    
                    cursor.close()
                    conexion.CerrarConnection()
                    return True, "Devolución procesada."
                else:
                    print(f"--> [DEBUG]: No se encontró ningún alquiler con el ID {id_alquiler}")
                    
                cursor.close()
                conexion.CerrarConnection()
                return False, "No se encontró el alquiler."
            except Exception as e:
                print("--> [ERROR CRÍTICO EN DEVOLUCIÓN]:", e)
                return False, f"Error: {e}"