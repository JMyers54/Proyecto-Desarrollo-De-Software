from DAL.Repository.ClienteRepository import ClienteRepository
class ServicesCliente():
    def __init__(self, modelo):
        self.modelo = modelo
        self.cliente_repo = ClienteRepository(None, modelo)

    def listar_clientes(self):
            try:
                exito = self.cliente_repo.mostrar_clientes()
                if exito:
                    return exito
                else:
                    return False, "No se pudo listar los clientes"
            except Exception as e:
                return False, f"Error en el servicio: {str(e)}"