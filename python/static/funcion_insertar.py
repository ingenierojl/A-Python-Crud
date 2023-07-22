from multiprocessing import connection
from funcion_conexion import *
from funcion_insertar import *
import mysql.connector



def select_login(correo):
    
    try:
        """"
        connection = mysql.connector.connect(host='localhost',
                                             database='basedeprueba',
                                             user='root',
                                             password='')
        cursor = connection.cursor()"""
        
        connection=conexion()
        cursor=conexion()

        queryselect=("""SELECT correo, password from usuarios where correo = %s""")

        cursor.execute(queryselect, (correo,))
        myresult=cursor.fetchall()
        connection.commit()
        return myresult
        print("Bienvenido a la funcion select-login")
 

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")





    



 

def insert_varibles_into_signup(fn, eml, psw, rpsw):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='basedeprueba',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO `usuarios` (`NombreCompleto`, `correo`, `password`, `rppasword`) 
                                VALUES (%s, %s, %s, %s) """
 

        record = (fn, eml, psw, rpsw)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into Laptop table")
 

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")














