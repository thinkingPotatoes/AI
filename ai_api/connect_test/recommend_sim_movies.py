import json
import requests

url = "http://localhost:9000/recommend"

payload = json.dumps({
    "userId": 1,
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)