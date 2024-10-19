import subprocess
import os

def run_commands():    
    # Comando para iniciar el servidor con Gunicorn
    try:
        print("Iniciando el servidor con Gunicorn...")
        port = os.environ.get('PORT', '5000')  # Usa el puerto definido o el 5000 por defecto
        subprocess.run(['gunicorn', f'--bind=0.0.0.0:{port}', '--workers=3', 'run:app'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == '__main__':
    run_commands()
