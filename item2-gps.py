import requests

LOCATIONIQ_API_KEY = 'pk.4f419236382e8e8ec0f554d8d9556a6a'
OPENROUTESERVICE_API_KEY = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjZiMmZhZDJkZjE2M2YwNWZhMzc2YmIxMmNmMDUwMDBlZjQxY2Q1ZjYxYzYyM2YyMjVlN2ZlZGI4IiwiaCI6Im11cm11cjY0In0='

def buscar_ciudad(nombre):
    url = 'https://api.locationiq.com/v1/autocomplete'
    params = {
        'key': LOCATIONIQ_API_KEY,
        'q': nombre,
        'limit': 5,
        'accept-language': 'es',
        'format': 'json'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Error al buscar ciudad:", response.status_code)
        return []

def seleccionar_ciudad(tipo):
    while True:
        entrada = input(f"🔍 Ingrese parte del nombre de la ciudad de {tipo} (o 's' para salir): ").strip()
        if entrada.lower() == 's':
            return None
        resultados = buscar_ciudad(entrada)
        if not resultados:
            print("⚠️ No se encontraron coincidencias. Intente nuevamente.")
            continue
        print(f"Coincidencias encontradas para '{entrada}':")
        for i, lugar in enumerate(resultados, 1):
            print(f"{i}. {lugar.get('display_name')}")
        try:
            seleccion = int(input("Seleccione el número de la ciudad: "))
            if 1 <= seleccion <= len(resultados):
                lat = float(resultados[seleccion - 1]['lat'])
                lon = float(resultados[seleccion - 1]['lon'])
                return (lon, lat)
            else:
                print("⚠️ Selección fuera de rango.")
        except ValueError:
            print("⚠️ Entrada inválida. Intente nuevamente.")

def obtener_ruta(origen, destino, perfil):
    url = f'https://api.openrouteservice.org/v2/directions/{perfil}'
    params = {
        'api_key': OPENROUTESERVICE_API_KEY,
        'start': f'{origen[0]},{origen[1]}',
        'end': f'{destino[0]},{destino[1]}'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        props = data['features'][0]['properties']
        distancia_km = props['segments'][0]['distance'] / 1000
        distancia_mi = distancia_km * 0.621371
        duracion_min = props['segments'][0]['duration'] / 60
        pasos = props['segments'][0]['steps']
        return distancia_km, distancia_mi, duracion_min, pasos
    else:
        print("❌ Error al obtener la ruta:", response.status_code)
        return None, None, None, None

def mostrar_menu(distancia_km, distancia_mi, duracion_min, pasos):
    while True:
        print("\n¿Qué información desea ver?")
        print("1. Mostrar la duración del viaje en millas, kilómetros y minutos.")
        print("2. Mostrar la narrativa del viaje.")
        print("s. Salir al menú principal.")
        opcion = input("Seleccione una opción: ").strip().lower()
        if opcion == '1':
            print(f"📍 Distancia total: {distancia_km:.2f} km / {distancia_mi:.2f} millas")
            print(f"⏱️ Duración estimada: {duracion_min:.1f} minutos")
        elif opcion == '2':
            print("🧭 Narrativa del viaje:")
            for paso in pasos:
                print(f" - {paso['instruction']}")
        elif opcion == 's':
            break
        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

def main():
    print("=== Consulta de rutas entre ciudades ===")
    while True:
        origen = seleccionar_ciudad("origen")
        if origen is None:
            print("👋 ¡Gracias por usar el servicio!")
            break
        destino = seleccionar_ciudad("destino")
        if destino is None:
            print("👋 ¡Gracias por usar el servicio!")
            break
        perfil = input("Tipo de transporte (driving-car, foot-walking, cycling-regular): ").strip()
        if perfil not in ['driving-car', 'foot-walking', 'cycling-regular']:
            print("⚠️ Tipo de transporte no válido.")
            continue
        distancia_km, distancia_mi, duracion_min, pasos = obtener_ruta(origen, destino, perfil)
        if pasos:
            mostrar_menu(distancia_km, distancia_mi, duracion_min, pasos)

if __name__ == "__main__":
    main()
