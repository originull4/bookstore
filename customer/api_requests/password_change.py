import requests
from getpass import getpass

url = 'http://127.0.0.1:8000/api/user/password/change/23/'

staff_token = 'e057191755dfd335f1a3c1a3eb3992e5765bef41'

old_password = getpass('old password: ')
password1 = getpass('new password: ')
password2 = getpass('confirm new password: ')

data = {'old_password': old_password, 'password1': password1, 'password2': password2}

headers={'Authorization': f'Token {staff_token}'}

get_response = requests.put(url=url, data=data, headers=headers)


print('status_code: ', get_response.status_code)
print(get_response.json())
