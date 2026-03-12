
class Vehiculo():
    def __init__(self, id, marca, modelo, año, tipo, precio_diario, estado, imagen):
        self.__id = id
        self.__marca = marca
        self.__modelo = modelo
        self.__año = año
        self.__tipo = tipo
        self.__precio_diario = precio_diario
        self.__estado = estado
        self.__imagen = imagen

    @property
    def id(self):
        return self.__id
    @property
    def marca(self):
        return self.__marca
    @property
    def modelo(self):
        return self.__modelo
    @property
    def año(self):
        return self.__año
    @property
    def tipo(self):
        return self.__tipo
    @property
    def precio_diario(self):
        return self.__precio_diario
    @property
    def estado(self):
        return self.__estado
    @property
    def imagen(self):
        return self.__imagen