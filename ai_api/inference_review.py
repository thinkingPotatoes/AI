import requests

def predict_block_review(content):
    API_URL = "https://api-inference.huggingface.co/models/hyewon/comment-classifier-model"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    outputs = query({
        "inputs": content,
    })

    isBlock = False
    if type(outputs) == list:
        result = outputs[0][0]['label']
        # 악플 위험 높은 댓글: LABEL_0
        if result == "LABEL_0":
            isBlock = True

    return isBlock