import requests

url = 'http://127.0.0.1:8000/api/user/23/'

admin_token = '7b5777d880ad6b697b35943cc668581fd67bc428'
staff_token = '94b1918ac5395cb0d887c496f906cb9f7777363a'

headers={'Authorization': f'Token {staff_token}'}

get_response = requests.get(url=url, headers=headers)


print('status_code: ', get_response.status_code)
print(get_response.json())