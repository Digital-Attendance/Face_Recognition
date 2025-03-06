import json
import base64
import requests

with open("test.jpg", "rb") as f:
    encoded_image = base64.b64encode(f.read()).decode("utf-8")

url = "https://zjaxli24s5wu5anukwvvodgtoy0vckbn.lambda-url.ap-south-1.on.aws/"

payload = {
    # "body": json.dumps(
    #     {
    "email": "piyus21_ug@ei.nits.ac.in",
    "image": encoded_image,
    "registration": False,
    #     }
    # )
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)
try:
    print(response)
    response_json = response.json()
    print("Response:", json.dumps(response_json, indent=2))
except Exception as e:
    print("Error decoding JSON response:", e)
    print("Response Text:", response.text)
