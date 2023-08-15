from funcion_conexion import *

def actualizarcorreowherenombre(nombre, nuevo_correo):
    try:
        connection = conexion()
        cursor = connection.cursor()

        query = f"UPDATE usuarios SET correo = %s WHERE NombreCompleto = %s;"
        values = (nuevo_correo, nombre)
        
        cursor.execute(query, values)

        connection.commit()
        print("Record updated successfully")

    except mysql.connector.Error as error:
        print("Failed to update record:", error)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Llama a la función con los valores correspondientes

