import requests

url = "http://localhost:8000/"

print("--------------------------------------------------")
print("----------------SE AÑADE UNA PARTIDA--------------")
print("--------------------------------------------------")
response = requests.request(
    method="POST", url=url + "guess", json={"player": "Juan"}
)
print(response.text)


response = requests.request(
    method="GET",url=url+"guess"
)
print("--------------------------------------------------")
print("-----------SE MUESTRAN LAS PARTIDAS--------------")
print("--------------------------------------------------")
print(response.text)

print("--------------------------------------------------")
print("----------------SE JUEGA UNA PARTIDA--------------")
print("--------------------------------------------------")
response = requests.request(
    method="PUT", url=url + "guess", json={"attempt": 82}
)
print(response.text)