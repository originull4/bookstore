import requests


admin_token = '7b5777d880ad6b697b35943cc668581fd67bc428'

url = 'http://127.0.0.1:8000/api/user/list/'

headers={'Authorization': f'Token {admin_token}'}

get_response = requests.get(url=url, headers=headers)

print('status_code: ', get_response.status_code)
print(get_response.json())
