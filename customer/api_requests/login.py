import requests
from getpass import getpass

url = 'http://127.0.0.1:8000/api/user/login/'
username = input('username: ')
password = getpass('passowrd: ')

data = {'username': username, 'password': password}
get_response = requests.post(url=url, data=data)
print('status_code: ', get_response.status_code)
print(get_response.json())
