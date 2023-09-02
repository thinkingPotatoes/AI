import json
import requests

url = "http://localhost:9000/blogs/keyword/123"

payload = json.dumps({
    "articleId": 123,
    "review": 
            """검은조직이 나온 이번 극장판은 정말 최고의 작품입니다. 코하를 좋아하시는 분들은 꼭 보시길 바랄게요. 평점은 5점입니다."""
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)