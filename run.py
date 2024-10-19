from app import create_app
import os

# Crear la aplicación Flask usando la función factory `create_app`
app = create_app()

# Punto de entrada principal para ejecutar la aplicación
if __name__ == '__main__':
    # Ejecutar la aplicación Flask con el modo debug activado
    # Escuchar en todas las interfaces y utilizar el puerto especificado por la variable de entorno
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
