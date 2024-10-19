import subprocess
import os

def run_commands():
    # Comando para iniciar migraciones de base de datos
    try:
        print("Iniciando versiones de base de datos...")
        subprocess.run(['flask', 'db', 'init'], check=True)
        print("Migraciones iniciadas con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al iniciar migraciones: {e}")
        return

    # Comando para iniciar migraciones de base de datos
    try:
        print("Iniciando migraciones de base de datos...")
        subprocess.run(['flask', 'db', 'migrate', '-m', '"Initial migration."'], check=True)
        print("Migraciones iniciadas con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al iniciar migraciones: {e}")
        return

    # Comando para aplicar migraciones de base de datos
    try:
        print("Aplicando migraciones de base de datos...")
        subprocess.run(['flask', 'db', 'upgrade'], check=True)
        print("Migraciones aplicadas con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al aplicar migraciones: {e}")
        return
    
    # Comando para iniciar el servidor con Gunicorn
    try:
        print("Iniciando el servidor con Gunicorn...")
        port = os.environ.get('PORT', '5000')  # Usa el puerto definido o el 5000 por defecto
        subprocess.run(['gunicorn', f'--bind=0.0.0.0:{port}', '--workers=3', 'run:app'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == '__main__':
    run_commands()
