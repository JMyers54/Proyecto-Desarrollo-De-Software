from DAL.Infrastructure.ConexionDB import ConexionDB    

class VehiculoRepository():
    def __init__(self,vista,modelo):
        self.vista = vista
        self.modelo = modelo

    def RegistroVehiculos(self,Marca, Modelo, Año, Tipo, Precio_diario, Estado, nombre_imagen):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO VEHICULOS (MARCA, MODELO, AÑO, TIPO, PRECIO_POR_DIA, ESTADO, IMAGEN) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            datos = (Marca, Modelo, Año, Tipo, Precio_diario, Estado, nombre_imagen)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehículo registrado con éxito"
        except Exception as e:
            return False, f"Error al registrar el Vehículo: {e}"

    def EliminarVehiculo(self, idvehiculo):
            print(f"Eliminando vehiculo con id: {idvehiculo}")
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                cursor = db.cursor()

                # RN-05: verificar alquileres activos
                cursor.execute("""
                    SELECT COUNT(*) FROM ALQUILERES 
                    WHERE ID_VEHICULO = %s AND FECHA_FIN >= CURDATE()
                """, (idvehiculo,))
                activos = cursor.fetchone()[0]
                if activos > 0:
                    cursor.close()
                    conexion.CerrarConnection()
                    return False, f"No se puede eliminar: el vehículo tiene {activos} alquiler(es) activo(s)"

                sql = "DELETE FROM VEHICULOS WHERE ID_VEHICULO = %s"
                cursor.execute(sql, (idvehiculo,))
                db.commit()
                cursor.close()
                conexion.CerrarConnection()
                return True, "Vehículo eliminado"
            except Exception as e:
                return False, f"Error al eliminar el Vehículo {e}"

    def ActualizarVehiculo(conn,idVehiculo,marca,modelo,año,color,tipo,precio_diario,estado,km,combustible,transmision,motor,observaciones):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = """UPDATE VEHICULOS SET MARCA=%s,MODELO=%s,AÑO=%s,COLOR=%s,TIPO=%s,PRECIO_POR_DIA=%s,ESTADO=%s,KM=%s,COMBUSTIBLE=%s,TRANSMISION=%s,MOTOR=%s,OBSERVACIONES=%s WHERE ID_VEHICULO=%s"""
            datos = (marca,modelo,año,color,tipo,precio_diario,estado,km,combustible,transmision,motor,observaciones,idVehiculo)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehículo modificado"
        except Exception as e:
            print("ERROR:", e)
            return False, f"Error al modificar el vehículo: {e}"

    def obtener_vehiculos(conn):
        cursor = conn.cursor()
        cursor.execute("""SELECT IdVehiculo, Marca, Modelo, Año, Tipo, Precio_diario, Estado FROM Vehiculos""")
        return cursor.fetchall()

    def AlquilaVehiculo(self, id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, total):
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                cursor = db.cursor()
                sql = """
                    INSERT INTO ALQUILERES (ID_CLIENTE, ID_VEHICULO, ID_EMPLEADO, FECHA_INICIO, FECHA_FIN, TOTAL) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (id_cliente, id_vehiculo, id_empleado, fecha_inicio, fecha_fin, total))
                db.commit()
                cursor.close()
                conexion.CerrarConnection()
                return True
            except Exception as e:
                print("ERROR AL GUARDAR ALQUILER:", e)
                return False

    def mostrar_vehiculos(self):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            conn = conexion.getConnection()
            cursor = conn.cursor()
            cursor.execute("""SELECT Id_Vehiculo,Marca,Modelo,Año,Tipo,Precio_Por_Dia,Estado,Color,Km,Combustible,Transmision,Motor,Observaciones FROM Vehiculos""")
            filas = cursor.fetchall()
            return [
                {
                    "id": int(f[0]),
                    "placa": str(f[0]),
                    "marca": f[1],
                    "modelo": f[2],
                    "año": f[3],
                    "tipo": f[4],
                    "precio": float(f[5]),
                    "estado": f[6],
                    "color": f[7],
                    "km": f[8],
                    "combustible": f[9],
                    "transmision": f[10],
                    "motor": f[11],
                    "obs": f[12]
                }
                for f in filas
            ]
        except Exception as e:
            raise e
        finally:
            self.modelo.CerrarConnection()

    def obtener_todos_los_vehiculos(self):
        db = ConexionDB()
        db.CrearConnection()
        conexion = db.getConnection()
        cursor = conexion.cursor(dictionary=True) # CON CONFIGURACIÓN DE DICCIONARIO:
        cursor.execute("SELECT ID_VEHICULO, MARCA, MODELO, AÑO, TIPO, PRECIO_POR_DIA, ESTADO, IMAGEN FROM vehiculos")
        lista_carros = cursor.fetchall()
        cursor.close()
        db.CerrarConnection()
        return lista_carros

    def VerificarDisponibilidad(self, idVehiculo, fecha_inicio, fecha_fin):
            try:
                conexion = ConexionDB()
                conexion.CrearConnection()
                db = conexion.getConnection()
                cursor = db.cursor()
                # LÓGICA INFALIBLE PARA FECHAS CONSECUTIVAS:
                # Un vehículo NO está disponible si el rango solicitado se solapa con uno existente.
                # Se cruzan si: la fecha_inicio solicitada es MENOR o IGUAL a la FECHA_FIN existente
                # Y la fecha_fin solicitada es MAYOR o IGUAL a la FECHA_INICIO existente.
                sql = """SELECT COUNT(*) FROM ALQUILERES WHERE ID_VEHICULO = %s AND (%s <= FECHA_FIN AND %s >= FECHA_INICIO)"""
                # Pasamos los parámetros en el orden exacto de la consulta:
                cursor.execute(sql, (idVehiculo, fecha_inicio, fecha_fin))
                resultado = cursor.fetchone()[0]
                cursor.close()
                conexion.CerrarConnection()
                return resultado
            except Exception as e:
                print("ERROR EN VERIFICAR_DISPONIBILIDAD:", e)
                return 0

    def ObtenerVehiculoPorId(self, idVehiculo):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "SELECT Marca, Modelo, Precio_Por_Dia FROM Vehiculos WHERE Id_Vehiculo = %s"
            cursor.execute(sql, (idVehiculo,))
            vehiculo = cursor.fetchone()
            cursor.close()
            conexion.CerrarConnection()
            return vehiculo
        except Exception as e:
            print("Error:", e)
            return None
        
    def ObtenerFechasOcupadas(self, idVehiculo):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("""
                SELECT DATE_FORMAT(FECHA_INICIO, '%Y-%m-%d') AS FECHA_INICIO,
                    DATE_FORMAT(FECHA_FIN, '%Y-%m-%d')    AS FECHA_FIN
                FROM ALQUILERES 
                WHERE ID_VEHICULO = %s
            """, (idVehiculo,))
            resultado = cursor.fetchall()
            cursor.close()
            conexion.CerrarConnection()
            return resultado
        except Exception as e:
            return []