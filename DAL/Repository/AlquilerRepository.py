from DAL.Infrastructure.ConexionDB import ConexionDB
class Alquiler():
    def __init__(self):
        pass

    def alquilar_vehiculo(conn, id_cliente, id_vehiculo, fecha_inicio, fecha_fin):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO ALQUILER (ID_CLIENTE, ID_VEHICULO, FECHA_INICIO, FECHA_FIN, TOTAL) VALUES (%s, %s, %s, %s)"
            sql = "ALTER TABLE VEHICULO MODIFY ESTADO WHERE ID"
            datos = (id_cliente, id_vehiculo, fecha_inicio, fecha_fin)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehículo alquilado con éxito"
        except Exception as e:
            return False, f"Error al alquilar el Vehículo: {e}"