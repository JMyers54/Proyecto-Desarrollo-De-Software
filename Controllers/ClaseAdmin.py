class Admin():
    def __init__(self, id, Cedula, Nombre, Apellido, Telefono, Email, Usuario, Contraseña):
        self.__id = id
        self.__Cedula = Cedula
        self.__Nombre = Nombre
        self.__Apellido = Apellido
        self.__Telefono = Telefono
        self.__Email = Email
        self.__Usuario = Usuario
        self.__Contra = Contraseña
    
    @property
    def id(self):
        return self.__id
    @property
    def Cedula(self):
        return self.__Cedula
    @property
    def Nombre(self):
        return self.__Nombre
    @property
    def Apellido(self):
        return self.__Apellido
    @property
    def Telefono(self):
        return self.__Telefono
    @property
    def Email(self):
        return self.__Email
    @property
    def Usuario(self):
        return self.__Usuario
    @property
    def Contraseña(self):
        return self.__Contra