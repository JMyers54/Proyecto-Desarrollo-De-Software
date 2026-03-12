from tkinter import *
import tkinter as tk
from tkinter import ttk
from Controllers.Funciones import *
from Models.ConexionDB import *

class VentanaPrincipal():
    def __init__(self):
        self.modelo = ConexionDB()
        self.ventana1 = tk.Tk()
        self.ventana1.title("alquiler de vehiculos")
        self.ventana1.config(width= 700, height= 500, bg="#262627")
        self.ventana1.resizable(0,0)
        self.Titulo = tk.Label(self.ventana1, text="alquiler de vehiculos", bg="#262627", font=("Arial",20))
        self.Titulo.place(relx=0.350, rely=0.10)
        self.btnPrincipal = tk.Button(self.ventana1, text="Menu", bg="#848489", command=lambda: VentanaMenu(self.modelo), font=("Arial",14))
        self.btnPrincipal.place(relx=0.470, rely=0.40)
        self.ventana1.mainloop()

class VentanaMenu():
    def __init__(self, modelo):
        self.modelo = modelo
        self.ventana2 = tk.Toplevel()
        self.ventana2.title("Menu")
        self.ventana2.config(width= 700, height= 500, bg="#262627")
        self.ventana2.resizable(0,0)
        self.pestaña = ttk.Notebook(self.ventana2)
        self.pestaña.place(relx=0.0, rely=0.0, width=700, height=500)

        self.administrador = tk.Frame(self.pestaña)
        self.empleados = tk.Frame(self.pestaña)
        self.catalogo = tk.Frame(self.pestaña)
        self.novedades = tk.Frame(self.pestaña)

        self.pestaña.add(self.novedades, text="Novedades")
        self.pestaña.add(self.catalogo, text="Catalogo")
        self.pestaña.add(self.empleados, text="Empleados")
        self.pestaña.add(self.administrador, text="Administracción")
        
        self.administrador.config(background="#262627")
        self.empleados.config(background="#262627")
        self.novedades.config(background="#262627")
        self.catalogo.config(background="#262627")

        PestañaAdministrador(self.administrador, self.modelo)
        PestañaEmpleado(self.empleados)
        PestañaCatalogo(self.catalogo)
        PestañaNovedades(self.novedades)

class PestañaAdministrador():
    def __init__(self,frame,modelo):
        self.frame = frame
        self.modelo = modelo
        self.funciones = Funciones(self,modelo)
        self.lblId = tk.Label(self.frame ,text="ID de admin" ,bg="#262627")
        self.lblId.place(relx=0.29,rely=0.33)
        self.EntryId = tk.Entry(self.frame)
        self.EntryId.place(relx=0.39, rely=0.33)
        self.lblContra = tk.Label(self.frame ,text="Contraseña" ,bg="#262627")
        self.lblContra.place(relx=0.26,rely=0.43)
        self.EntryContra = tk.Entry(self.frame)
        self.EntryContra.place(relx=0.39, rely=0.43)
        self.btnEntrar = tk.Button(self.frame, text="Entrar", command= self.funciones.loginAdmin)
        self.btnEntrar.place(relx= 0.41,rely=0.53)
        self.btnRegistrar = tk.Button(self.frame, text="Registrar", command=lambda: RegistrarEmpleado())
        self.btnRegistrar.place(relx= 0.51, rely=0.53)

class PestañaEmpleado():
    def __init__(self,frame):
        self.frame = frame
        self.lblNombre = tk.Label(self.frame ,text="Nombre" ,bg="#262627")
        self.lblNombre.place(relx=0.29,rely=0.33)
        self.nombre = tk.Entry(self.frame)
        self.nombre.place(relx=0.39, rely=0.33)
        self.lblContra = tk.Label(self.frame ,text="Contraseña" ,bg="#262627")
        self.lblContra.place(relx=0.26,rely=0.43)
        self.Contra = tk.Entry(self.frame)
        self.Contra.place(relx=0.39, rely=0.43)
        self.btn= tk.Button(self.frame, text="Entrar")
        self.btn.place(relx= 0.46,rely=0.53, width=70, height=43)

class PestañaCatalogo():
    def __init__(self,frame):
        self.frame = frame
        self.scroll = tk.Scrollbar(self.frame,orient="vertical")
        self.scroll.set(0.2,0.5)
        self.scroll.place(relx=0.98,rely=0.0,height=480)
        self.btn= tk.Button(self.frame, text="rrrr")
        self.btn.place(relx= 0.12,rely=0.23, width=40, height=23)

class PestañaNovedades():
    def __init__(self,frame):
        self.frame = frame
        self.btn= tk.Button(self.frame, text="rrrr")
        self.btn.place(relx= 0.12,rely=0.23, width=40, height=23)

class RegistrarEmpleado():
    def __init__ (self):
        self.Registrar = tk.Toplevel()
        self.Registrar.config(width=700,height=500,bg="#262627")
        self.Registrar.title("Registrar")
        self.Registrar.resizable(0,0)
        #--------------------Registro------------------------
        tk.Label(self.Registrar ,text="Nombre" ,bg="#262627").place(relx=0.29,rely=0.33)
        self.nombre = tk.Entry(self.Registrar)
        self.nombre.place(relx=0.39, rely=0.33)
        tk.Label(self.Registrar, text="Cedula", bg="#262627").place(relx=0.29, rely=0.43)
        self.Cedula = tk.Entry(self.Registrar)
        self.Cedula.place(relx=0.39, rely=0.43)
        tk.Label(self.Registrar, text="Correo", bg="#262627").place(relx=0.29, rely=0.53)
        self.Correo = tk.Entry(self.Registrar)
        self.Correo.place(relx=0.39, rely=0.53)
        tk.Label(self.Registrar ,text="Contraseña" ,bg="#262627").place(relx=0.26,rely=0.63)
        self.Contra = tk.Entry(self.Registrar)
        self.Contra.place(relx=0.39, rely=0.63)
        self.btnRegistrar = tk.Button(self.Registrar, text="Registrar", command=Funciones.EmpleadoRegistrado).place(relx=0.46, rely=0.73)

class OpcionesAdmin():
    def __init__(self):
        self.ventana = tk.Toplevel()
        self.ventana.config(width= 700, height= 500, bg="#262627")
        self.ventana.resizable(0,0)