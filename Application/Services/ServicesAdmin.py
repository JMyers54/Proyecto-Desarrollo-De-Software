
class ServicesAdmin():
    def __init__(self):
        pass

    def agregarVehiculo(self, IdVehiculo, Marca, Modelo, Año, Tipo, Precio_diario, Estado):
        from DAL.Repository.VehiculoRepository import VehiculoRepository
        vehiculo_repo = VehiculoRepository(None,None)
        return vehiculo_repo.RegistroVehiculos(IdVehiculo, Marca, Modelo, Año, Tipo, Precio_diario, Estado)