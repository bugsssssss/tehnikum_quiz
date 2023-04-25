import requests
import json

user_info = {
    "user_id": 1213,
    "first_name": 'test',
    "phone_number": '2312312',
    "verification_code": 122134
}
url = 'http://127.0.0.1:8000/api/bot-users/'
response = requests.post(url, data=user_info)
print(response.json())
