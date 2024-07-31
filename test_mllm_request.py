import requests

url = 'http://210.94.172.164:20191/image'
headers = {'Content-Type': 'multipart/form-data'}

files = {'file': open('images/1.jpg', 'rb')}
data = {'text': {"What mob is you can see?How far is it?"}, 'is_del': '1'}
response = requests.post(url, files=files, data=data)
# print(response)
print(response.json())