import requests
import base64

url = "http://127.0.0.1:8000/generate_response"

def image_url_to_base64(image_url: str) -> str:
    """
    Converts an image from a URL to a Base64 encoded string.
    """
    response = requests.get(image_url)
    image_bytes = response.content
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return image_base64


image_base64 = image_url_to_base64(
"https://omnomnom.dp.ua/image/cache/catalog/pizza_new/new4/pepperoni-500x500.jpg")
payload = {"image_base64": image_base64}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

### Output:
# {
#     "status": "success",
#     "result": '{"calories": 100, "proteins": 10, "fats": 20, "carbohydrates": 30}',
# }
