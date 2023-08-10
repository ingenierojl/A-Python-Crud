from funcion_conexion import *
import mysql.connector

def insert_varibles_into_signup(fn, eml, psw, rpsw):
    try:
       
        connection=conexion()       
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














