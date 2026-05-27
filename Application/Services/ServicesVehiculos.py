from DAL.Infrastructure.ConexionDB import ConexionDB
from DAL.Repository.VehiculoRepository import VehiculoRepository

ESTADOS_VALIDOS = ["Disponible", "Alquilado", "Mantenimiento"]
class ServicesVehiculos():
    def __init__(self, modelo):
        self.modelo = modelo
        self.vehiculo_repo = VehiculoRepository(None, modelo)
    
    def alquilar_vehiculo(self, id_vehiculo):
        try:
            exito = self.vehiculo_repo.alquilar(id_vehiculo)
            if exito:
                return True, "Vehículo alquilado correctamente"
            else:
                return False, "No se pudo actualizar el estado"
        except Exception as e:
            return False, f"Error en el servicio: {str(e)}"

    def eliminaVehiculo(self, idVehiculo):
        try:
            exito = self.vehiculo_repo.EliminarVehiculo(idVehiculo)
            if exito:
                return True, "Vehículo eliminado correctamente"
            else:
                return False, "No se pudo eliminar el vehículo"
        except Exception as e:
            return False, f"Error en el servicio: {str(e)}"

    def listar_vehiculos(self):
        try:
            exito = self.vehiculo_repo.mostrar_vehiculos()
            if exito:
                return exito
            else:
                return False, "No se pudo listar los vehículos"
        except Exception as e:
            return False, f"Error en el servicio: {str(e)}"
    
    def ActualizarVehiculo(self, idVehiculo, marca, modelo, año, tipo, PrecioDiario, estado):
        if estado not in ESTADOS_VALIDOS:
            return False, f"Estado inválido. Los estados válidos son: {', '.join(ESTADOS_VALIDOS)}"
        try:
            exito = self.vehiculo_repo.ActualizarVehiculo(idVehiculo, marca, modelo, año, tipo, PrecioDiario, estado)
            if exito:
                return True, "Vehículo actualizado correctamente"
            else:
                return False, "No se pudo actualizar el vehículo"
        except Exception as e:
            return False, f"Error en el servicio: {str(e)}"