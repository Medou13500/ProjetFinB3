import requests

API_KEY = "AIzaSyC79Rhe2OwqpEgrt3uACIM0s73xWs63bDw"
EMAIL = "mehdybouzid8@gmail.com"
PASSWORD = "Medou13500!"

url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
payload = {
    "email": EMAIL,
    "password": PASSWORD,
    "returnSecureToken": True
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    id_token = response.json()["idToken"]
    print("✅ ID Token Firebase :\n")
    print(id_token)
else:
    print("❌ Erreur :", response.json())
