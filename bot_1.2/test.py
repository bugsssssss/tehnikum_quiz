import requests
import json

# user_info = {
#     "user_id": 1213,
#     "first_name": 'test',
#     "phone_number": '2312312',
#     "verification_code": 122134
# }
# url = 'https://p-api2.tehnikum.school/api/bot-users/'
# response = requests.post(url, data=user_info)
# print(response.json())


# url = 'http://127.0.0.1:8000/api/bot-users/1918321/'

# data = {"category_id": 3}

# # response = requests.get(url).json()
# response = requests.put(url, data=data)


url = 'https://p-api2.tehnikum.school/api/bot-users/657061394/'

data = {"category_id": None, 'is_verified': True}

response = requests.put(url, data=data)
