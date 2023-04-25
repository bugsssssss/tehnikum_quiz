import requests
import json

url = 'https://api.tehnikum.school/sms/sms.php'
token = 'Winners:12345678'


def send_sms(phone, text):
    data = {
        'token': token,
        'sms_phone': phone,
        'sms_text': text
    }
    response = requests.post(url, data=data)
    print(response.json())
    return response.json()
