from DAL.Repository.EmpleadoRepository import EmpleadoRepository
class ServicesEmpleado():
    def __init__(self, modelo):
        self.modelo = modelo
        self.empleado_repo = EmpleadoRepository(None, modelo)

    def listar_empleados(self):
        try:
            exito = self.empleado_repo.mostrar_empleados()
            if exito:
                return exito
            else:
                return False, "No se pudo listar los empleados"
        except Exception as e:
            raise e
        finally:
            self.modelo.CerrarConnection()
