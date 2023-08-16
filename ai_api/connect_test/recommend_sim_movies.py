import json
import requests

url = "http://localhost:9000/recommend/196"

payload = json.dumps({
    "userId": 196,
    "topN": 10
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)