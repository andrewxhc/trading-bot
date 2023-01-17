import http.client
import requests

# HTTP
conn = http.client.HTTPSConnection("fear-and-greed-index.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "bbbae29cf3msh3373a446fb6309cp13f3d9jsn7eebc48a49be",
    'X-RapidAPI-Host': "fear-and-greed-index.p.rapidapi.com"
    }

conn.request("GET", "/v1/fgi", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# Request
url = "https://fear-and-greed-index.p.rapidapi.com/v1/fgi"

headers2 = {
    "X-RapidAPI-Key": "bbbae29cf3msh3373a446fb6309cp13f3d9jsn7eebc48a49be",
    "X-RapidAPI-Host": "fear-and-greed-index.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)

