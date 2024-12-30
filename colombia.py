import requests

def obtener_datos_usuario(usuario, token=None):
    url = f"https://api.github.com/users/{usuario}"
    headers = {}
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos del usuario: {response.status_code}")
        return None

def obtener_repositorios(usuario, token=None):
    url = f"https://api.github.com/users/{usuario}/repos?per_page=100"
    headers = {}
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    repos = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos += response.json()
            url = response.links.get('next', {}).get('url')
        else:
            print(f"Error al obtener los repositorios: {response.status_code}")
            return []
    
    return repos

def lenguaje_mas_utilizado(repos):
    lenguajes = {}
    
    for repo in repos:
        lenguaje = repo.get('language', None)
        if lenguaje:
            lenguajes[lenguaje] = lenguajes.get(lenguaje, 0) + 1
    
    if lenguajes:
        return max(lenguajes, key=lenguajes.get)
    return "No se pudo determinar el lenguaje más utilizado"

def obtener_stars_forks(repos):
    stars = 0
    forks = 0
    
    for repo in repos:
        stars += repo.get('stargazers_count', 0)
        forks += repo.get('forks_count', 0)
    
    return stars, forks

def generar_informe(usuario, token=None):
    datos_usuario = obtener_datos_usuario(usuario, token)
    if not datos_usuario:
        return

    repos = obtener_repositorios(usuario, token)
    
    print(f"\nInforme de GitHub para el usuario: {usuario}")
    print(f"Nombre: {datos_usuario['name']}")
    print(f"Bio: {datos_usuario.get('bio', 'No disponible')}")
    print(f"Ubicación: {datos_usuario.get('location', 'No disponible')}")
    
    lenguaje = lenguaje_mas_utilizado(repos)
    print(f"Lenguaje más utilizado: {lenguaje}")
    
    cantidad_repos = len(repos)
    print(f"Cantidad de repositorios: {cantidad_repos}")
    
    seguidores = datos_usuario['followers']
    print(f"Número de seguidores: {seguidores}")
    
    seguidos = datos_usuario['following']
    print(f"Número de seguidos: {seguidos}")
    
    stars, forks = obtener_stars_forks(repos)
    print(f"Stars totales: {stars}")
    print(f"Forks totales: {forks}")

# uso
usuario = "JanSua"
token = None 
generar_informe(usuario, token)
