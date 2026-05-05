from DAL.Infrastructure.ConexionDB import ConexionDB    

class VehiculoRepository():
    def __init__(self,vista,modelo):
        self.vista = vista
        self.modelo = modelo

    def RegistroVehiculos(self, IdVehiculo, Marca, Modelo, Año, Tipo, Precio_diario, Estado):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "INSERT INTO VEHICULOS (ID_VEHICULOS,MARCA,MODELO,AÑO,TIPO,PRECIO_POR_DIA,ESTADO) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            datos =(IdVehiculo,Marca,Modelo,Año,Tipo,Precio_diario,Estado)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehiculo registrado"
        except Exception as e:
            return False, f"Error al registrar el Vehiculo {e}"

    def eliminarVehiculo(self, idVehiculo):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()
            cursor = db.cursor()
            sql = "DELETE FROM VEHICULOS WHERE ID_VEHICULOS = %s"
            datos = (idVehiculo)
            cursor.execute(sql, datos)
            db.commit()
            cursor.close()
            conexion.CerrarConnection()
            return True, "Vehiculo eliminado"
        except Exception as e:
            return False, f"Error al eliminar el vehiculo: {e}"