from Controllers.ClaseEmpleado import Empleado
from Controllers.ClaseCliente import  Cliente
from Controllers.ClaseVehiculo import Vehiculo
class Factura(Empleado,Cliente,Vehiculo):
    def __init__(self,NombreEmpleado,NombreCliente,NombreVehiculo,TipoVehiculo,ModeloVehiculo,AñoVehiculo):
        self.__NombreEmpleado = NombreEmpleado
        self.__NombreCliente = NombreCliente
        self.__NombreVehiculo = NombreVehiculo
        self.__TipoVehiculo = TipoVehiculo
        self.__ModeloVehiculo = ModeloVehiculo
        self.__AñoVehiculo = AñoVehiculo
