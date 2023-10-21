import json
import requests

url = "http://localhost:9000/rating"

payload = json.dumps({
    "userId": 302,
    "movieId": ["A06376", "B00013"]
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)