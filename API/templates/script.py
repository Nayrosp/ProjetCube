import requests

api_url = "http://192.168.22.53:5000/Donnees"  # Mettez votre URL API ici

try:
    response = requests.get(api_url)
    response.raise_for_status()  # Lèvera une exception pour les codes d'erreur HTTP

    print(f"L'API est disponible. Code de statut : {response.status_code}")
    print("Réponse JSON :", response.json())

except requests.exceptions.RequestException as e:
    print(f"Erreur lors de la requête vers l'API : {e}")