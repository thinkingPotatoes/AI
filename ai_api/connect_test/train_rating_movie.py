import json
import requests

url = "http://localhost:9000/rating/train"

response = requests.post(url)
print(response.text)