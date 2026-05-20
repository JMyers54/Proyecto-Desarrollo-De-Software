from Models.ClaseEmpleado import Empleado
class Cliente(Empleado):
    def __init__(self, IdCliente, Cedula, NombreCliente, ApellidoCliente, Region, Telefono, Email, LicenciaDeConducir):
        self.__IdCliente = IdCliente
        self.__Cedula = Cedula
        self.__NombreCliente = NombreCliente
        self.__ApellidoCliente = ApellidoCliente
        self.__Region = Region
        self.__Telefono = Telefono
        self.__Email = Email
        self.__LicenciaDeConducir = LicenciaDeConducir
    
    @property
    def IdCLiente(self):
        return self.__IdCliente
    @property
    def Cedula(self):
        return super().Cedula
    @property
    def Nombre(self):
        return self.__NombreCliente
    @property
    def Apellido(self):
        return self.__ApellidoCliente
    @property
    def Region(self):
        return self.__Region
    @property
    def Telefono(self):
        return super().Telefono
    @property
    def Email(self):
        return super().Email
    @property
    def LicenciaDeConducir(self):
        return self.__LicenciaDeConducir