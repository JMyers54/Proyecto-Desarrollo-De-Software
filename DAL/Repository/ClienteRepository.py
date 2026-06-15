from DAL.Infrastructure.ConexionDB import ConexionDB
from werkzeug.security import generate_password_hash, check_password_hash

class ClienteRepository():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo

    def RegistrarCliente(self, Cedula, Nombre, Apellido, Telefono, Email, Contra, NumLicencia, FechaVencimientoLicencia):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            cursor.execute("SELECT COALESCE(MAX(ID_CLIENTE), 0) FROM CLIENTES")
            ultimo = int(cursor.fetchone()[0])
            IdCliente = ultimo + 1
            contra_hash = generate_password_hash(Contra)
            sql = "INSERT INTO CLIENTES (ID_CLIENTE,CEDULA,NOMBRE,APELLIDO,TELEFONO,EMAIL,CONTRA,NUM_LICENCIA,FECHA_VENCIMIENTO_LICENCIA) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            datos = (IdCliente, Cedula, Nombre, Apellido, Telefono, Email, contra_hash, NumLicencia, FechaVencimientoLicencia)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Cliente registrado con éxito"
        except Exception as e:
            return False, f"Error al registrar cliente: {e}"

    def verificarCliente(self, cedula, contra):
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                with db.cursor() as cursor:
                    # Cambiamos la consulta para buscar por CEDULA en la tabla clientes
                    cursor.execute("SELECT CONTRA FROM clientes WHERE CEDULA = %s", (cedula,))
                    resultado = cursor.fetchone()
                conexion.CerrarConnection()
                
                if resultado is None:
                    return False, "La cédula no está registrada."
                
                if check_password_hash(resultado[0], contra):
                    return True, ""
                
                return False, "Contraseña incorrecta."
            except Exception as e:
                return False, f"Error al iniciar sesión: {e}"
    def obtener_clientes(conn):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Id_Cliente, Cedula, Nombre, Apellido, Region, Telefono, Email FROM clientes
        """)
        return cursor.fetchall()
    
    def alquilar_vehiculo(self, id_cliente, id_vehiculo, fecha_inicio, fecha_fin, total):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = """
            INSERT INTO ALQUILERES (ID_CLIENTE, ID_VEHICULO, FECHA_INICIO, FECHA_FIN, TOTAL) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (id_cliente,id_vehiculo,fecha_inicio, fecha_fin,total))
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def mostrar_clientes(self):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            conn = conexion.getConnection()
            cursor = conn.cursor()
            
            # Traemos las columnas exactas que pintas en el HTML
            cursor.execute("SELECT ID_CLIENTE, CEDULA, NOMBRE, APELLIDO, TELEFONO, EMAIL FROM CLIENTES")
            filas = cursor.fetchall()
            
            cursor.close()
            conexion.CerrarConnection()
            
            # Mapeamos con las claves exactas que busca tu plantilla Jinja2
            return [
                {
                    "id":       f[0],
                    "cedula":   str(f[1]),
                    "nombre":   f[2],
                    "apellido": f[3],
                    "telefono": f[4],
                    "email":    f[5]
                }
                for f in filas
            ]
        except Exception as e:
            print("Error al mostrar clientes:", e)
            return []

    def contar_alquileres_cliente(self, id_cliente):
        conexion = ConexionDB()
        conexion.CrearConnection()
        db = conexion.getConnection()
        cursor = db.cursor()
        sql = """SELECT COUNT(*)FROM ALQUILERES WHERE ID_CLIENTE = %s"""
        cursor.execute(sql, (id_cliente,))
        cantidad = cursor.fetchone()[0]
        cursor.close()
        conexion.CerrarConnection()
        return cantidad
    def ObtenerHistorialCliente(self, id_cliente):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = """
                SELECT 
                    A.ID_ALQUILER,
                    V.MARCA,
                    V.MODELO,
                    A.FECHA_INICIO,
                    A.FECHA_FIN,
                    A.TOTAL,
                    E.NOMBRE,
                    E.APELLIDO
                FROM ALQUILERES A
                INNER JOIN VEHICULOS V ON A.ID_VEHICULO = V.ID_VEHICULO
                INNER JOIN EMPLEADO E ON A.ID_EMPLEADO = E.IDEMPLEADO
                WHERE A.ID_CLIENTE = %s
                ORDER BY A.FECHA_INICIO DESC
            """
            cursor.execute(sql, (id_cliente,))
            filas = cursor.fetchall()
            cursor.close()
            conexion.CerrarConnection()
            return [
                {
                    "id_alquiler": f[0],
                    "marca":       f[1],
                    "modelo":      f[2],
                    "fecha_inicio": str(f[3]),
                    "fecha_fin":   str(f[4]),
                    "total":       float(f[5]),
                    "asesor":      f[6] + " " + f[7]
                }
                for f in filas
            ]
        except Exception as e:
            print("Error historial cliente:", e)
            return []
    
    def CancelarAlquiler(self, id_alquiler, id_cliente):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            # Verificar que el alquiler pertenece al cliente y que no ha iniciado
            cursor.execute("""
                SELECT FECHA_INICIO FROM ALQUILERES 
                WHERE ID_ALQUILER = %s AND ID_CLIENTE = %s
            """, (id_alquiler, id_cliente))
            fila = cursor.fetchone()
            if not fila:
                return False, "Alquiler no encontrado"
            from datetime import date
            if fila[0] <= date.today():
                return False, "No se puede cancelar: el alquiler ya inició o es hoy"
            cursor.execute("DELETE FROM ALQUILERES WHERE ID_ALQUILER = %s", (id_alquiler,))
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Alquiler cancelado correctamente"
        except Exception as e:
            return False, f"Error al cancelar: {e}"

    def ObtenerDatosDashboard(self, fecha_inicio=None, fecha_fin=None):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()

            filtro = ""
            params = []
            if fecha_inicio and fecha_fin:
                filtro = "WHERE A.FECHA_INICIO BETWEEN %s AND %s"
                params = [fecha_inicio, fecha_fin]

            # Vehículo más alquilado
            cursor.execute(f"""
                SELECT V.MARCA, V.MODELO, COUNT(*) as total
                FROM ALQUILERES A
                INNER JOIN VEHICULOS V ON A.ID_VEHICULO = V.ID_VEHICULO
                {filtro}
                GROUP BY A.ID_VEHICULO, V.MARCA, V.MODELO
                ORDER BY total DESC LIMIT 5
            """, params)
            vehiculos = [{"nombre": f"{f[0]} {f[1]}", "total": f[2]} for f in cursor.fetchall()]

            # Clientes frecuentes
            cursor.execute(f"""
                SELECT C.NOMBRE, C.APELLIDO, COUNT(*) as total
                FROM ALQUILERES A
                INNER JOIN CLIENTES C ON A.ID_CLIENTE = C.ID_CLIENTE
                {filtro}
                GROUP BY A.ID_CLIENTE, C.NOMBRE, C.APELLIDO
                ORDER BY total DESC LIMIT 5
            """, params)
            clientes = [{"nombre": f"{f[0]} {f[1]}", "total": f[2]} for f in cursor.fetchall()]

            # Asesor que más alquiló
            cursor.execute(f"""
                SELECT E.NOMBRE, E.APELLIDO, COUNT(*) as total
                FROM ALQUILERES A
                INNER JOIN EMPLEADO E ON A.ID_EMPLEADO = E.IDEMPLEADO
                {filtro}
                GROUP BY A.ID_EMPLEADO, E.NOMBRE, E.APELLIDO
                ORDER BY total DESC LIMIT 5
            """, params)
            asesores = [{"nombre": f"{f[0]} {f[1]}", "total": f[2]} for f in cursor.fetchall()]

            cursor.close()
            conexion.CerrarConnection()
            return {"vehiculos": vehiculos, "clientes": clientes, "asesores": asesores}
        except Exception as e:
            print("Error dashboard:", e)
            return {"vehiculos": [], "clientes": [], "asesores": []}
    
    def ObtenerNombreCliente(self, Cedula):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            with db.cursor() as cursor:
                cursor.execute("SELECT NOMBRE, APELLIDO FROM CLIENTES WHERE CEDULA = %s", (Cedula,))
                fila = cursor.fetchone()
            conexion.CerrarConnection()
            if fila:
                return f"{fila[0]} {fila[1]}"
            return "Cliente"
        except Exception as e:
            return "Cliente"