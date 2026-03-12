from Models.ConexionDB import ConexionDB
import os, shutil
from Controllers.ClaseVehiculo import Vehiculo
from tkinter import messagebox
class Funciones():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
    
    def EmpleadoRegistrado(self,):
        Nombre = self.vista.EntryCedula.get()
        Cedula = self.vista.EntryNombre.get()
        Contra = self.vista.EntryContra.get()

    def IniciarSesionAdmin(self, id,contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM administrador WHERE id = %s",(id))
                resultado = cursor.fetchone()
            
            conexion.CerrarConnection()
            if resultado is None:
                print("El id no esta registrado.")
                return False
            if resultado[0] == contra:
                return True
            else:
                print("Contraseña Incorrecta.")
                return False
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            return False

    def loginAdmin(self):
        id = self.vista.EntryId.get()
        contra = self.vista.EntryContra.get()
        if self.IniciarSesionAdmin(id, contra):
            self.vista.OpcioneAdmin()
        else:
            messagebox.showerror("Error","Cedula o Contraseña incorrecta.")



    def agregarVehiculo(self, id, marca, modelo, año, tipo, precio_diario, estado, imagen):
        pass