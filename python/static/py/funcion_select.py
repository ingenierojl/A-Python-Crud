from py.funcion_conexion import *
import mysql.connector

def select_login(correo):    
    try:
     
        connection=conexion()
        cursor=connection.cursor()

        queryselect=("""SELECT correo, password from usuarios where correo = %s""")

        cursor.execute(queryselect, (correo,))
        myresult=cursor.fetchall()
        connection.commit()
        return myresult
         

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
 

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed") 