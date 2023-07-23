import json
import requests

url = "http://localhost:9000/rating/302"

payload = json.dumps({
    "userId": 196,
    "movieId": 302
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)