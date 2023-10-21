import json
import requests

url = "http://localhost:9000/recommend/train"

response = requests.post(url)
print(response.text)