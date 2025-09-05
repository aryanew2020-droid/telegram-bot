import requests, base64

api_key = "sk-Zytg7AMjAn39DzuyNLlK0gqy1JN4Bj0lsN37bFVqQjtuegjb"  
 "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "text_prompts": [{"text": "A pink-haired anime girl wearing hoodie and shorts"}],
    "cfg_scale": 7,
    "height": 512,
    "width": 512,
    "samples": 1,
    "steps": 30,
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    image_base64 = result["artifacts"][0]["base64"]
    with open("output.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
    print("✅ Image saved as output.png")
else:
    print("❌ Error:", response.text)