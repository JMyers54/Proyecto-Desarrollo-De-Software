import mariadb as sql

class ConexionDB():
    def __init__(self):
        self.__host = "127.0.0.1"
        self.__port = 3306
        self.__user = "root"
        self.__password = ""
        self.__database = "ALQUILER_VEHICULOS"
        self.__connection = None


    def getConnection(self):
        return self.__connection
    
    def CrearConnection(self):
                self.__connection = sql.connect(
                    host = self.__host,
                    port = self.__port,
                    user = self.__user,
                    password = self.__password,
                    database = self.__database,
                    unix_socket = "/opt/lampp/var/mysql/mysql.sock"
                )

    def CerrarConnection(self):
        if self.__connection:
            self.__connection.close()
            self.__connection = None

