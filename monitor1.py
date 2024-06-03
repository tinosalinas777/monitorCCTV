import time
import ping3
import mysql.connector

# Función para verificar si un equipo está en línea
def check_online(ip):
    return ping3.ping(ip)

# Conectarse a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="h4sh",
    password="root",
    database="online"
)

# Lista de direcciones IP a verificar
direcciones_ip = ["192.168.0.2", "192.168.0.3", "192.168.0.23","192.168.0.200","192.168.0.43","192.168.0.70"]

while True:
    try:
        for ip_equipo in direcciones_ip:
            # Verificar si el equipo está en línea
            estado_equipo = "En línea" if check_online(ip_equipo) else "Fuera de línea"

            # Crear el cursor
            cursor = conexion.cursor()

            # Verificar si ya existe un registro para esta IP
            cursor.execute("SELECT * FROM Camaras WHERE ip = %s", (ip_equipo,))
            resultado = cursor.fetchone()

            if resultado:
                # Si existe, actualizar el estado
                consulta = "UPDATE Camaras SET nombre = %s WHERE ip = %s"
                valores = (estado_equipo, ip_equipo)
                cursor.execute(consulta, valores)
            else:
                # Si no existe, insertar un nuevo registro
                consulta = "INSERT INTO Camaras (nombre, ip) VALUES (%s, %s)"
                valores = (estado_equipo, ip_equipo)
                cursor.execute(consulta, valores)

            # Confirmar los cambios en la base de datos
            conexion.commit()

            # Cerrar el cursor
            cursor.close()

            print(f"Estado actualizado correctamente para la IP {ip_equipo}")

    except Exception as e:
        print("Error al actualizar la información:", e)

    # Esperar 5 segundos antes de la próxima actualización
    time.sleep(5)

# Cerrar la conexión
conexion.close()
