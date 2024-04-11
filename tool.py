import http.server
import socketserver
import json
import mysql.connector

# Manejador de peticiones HTTP
class MiManejador(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/obtener_estados_dispositivos':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Conectar a la base de datos y obtener los estados de los dispositivos
            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="h4sh",
                    password="root",
                    database="online"
                )
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("SELECT * FROM Camaras")
                dispositivos = cursor.fetchall()
                self.wfile.write(json.dumps(dispositivos).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
            finally:
                if 'conexion' in locals() and conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            # Si la ruta no es para obtener estados de dispositivos, servir archivos estáticos
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Configurar el servidor
puerto = 8000
with socketserver.TCPServer(("", puerto), MiManejador) as httpd:
    print("Servidor activo en el puerto", puerto)
    httpd.serve_forever()
