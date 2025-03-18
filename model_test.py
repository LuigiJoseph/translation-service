import requests

rest_api_url = "http://localhost:5000/translation-endpoints/api/v1/translate/helsinki/en/tr"
payload = {"text": "coffee"}

response = requests.post(rest_api_url, json=payload, headers={"Content-Type": "application/json"}, timeout=5)

print("Status Code:", response.status_code)
print("Response:", response.json())
