from Models.ClaseAdmin import Admin

class Empleado(Admin):
    def __init__(self, IdEmpleado, Cedula, NombreEmpleado, Apellido, Telefono, Email, Contra ):
        self.__idEmpleado = IdEmpleado
        self.__Cedula = Cedula
        self.__NombreEmpleado = NombreEmpleado
        self.__Apellido = Apellido
        self.__Telefono = Telefono
        self.__Email = Email
        self.__Contra = Contra

    @property
    def IdEmpleado(self):
        return self.__IdEmpleado
    @property
    def Cedula(self):
        return super().Cedula
    @property
    def Nombre(self):
        return self.__NombreEmpleado
    @property
    def Apellido(self):
        return super().Apellido
    @property
    def Telefono(self):
        return super().Telefono
    @property
    def Email(self):
        return super().Email
    @property
    def Contra(self):
        return super().Contra