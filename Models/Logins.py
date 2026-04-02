from ConexionDB import ConexionDB

class ModeloLogin():
    def __init__(self):
        self.db = ConexionDB
    
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