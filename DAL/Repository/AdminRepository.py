from DAL.Infrastructure.ConexionDB import ConexionDB    

class AdminRepository():
    def __init__(self, vista, modelo):
        self.vista = vista
        self.modelo = modelo
        self.db = ConexionDB

    def IniciarSesionAdmin(self, id,contra):
        try:
            conexion = ConexionDB()
            conexion.CrearConnection()
            db = conexion.getConnection()

            with db.cursor() as cursor:
                cursor.execute("SELECT Contraseña FROM admin WHERE id_admin = %s",(id,))
                resultado = cursor.fetchone()
            
            conexion.CerrarConnection()
            if resultado is None:
                return False, "El id no esta registrado."
            if resultado[0] == contra:
                return True, ""
            else:
                return False, "Contraseña Incorrecta."
        except Exception as e:
            return False, f"Error al iniciar sesión: {e}"

    def verificarUsuario(self, IdAdmin, contra):
        if not self.db.CrearConnection():
            return False
        
        conexion = self.db.getConnection()
        cursor = conexion.cursor()

        query = """
            SELECT * FROM admin
            WHERE IdAdmin = %s AND Contraseña = %s
            """
        
        cursor.execute(query,(IdAdmin, contra))
        resultado = cursor.fetchone()

        self.db.CerrarConnection()
        return resultado is not None