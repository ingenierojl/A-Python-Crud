import mysql.connector

def conexion():
    connection = mysql.connector.connect(host='localhost',
                                             database='basedeprueba',
                                             user='root',
                                             password='')

    return connection

     


