import requests

url = 'http://127.0.0.1:8000/api/user/detail/23/'

admin_token = '7b5777d880ad6b697b35943cc668581fd67bc428'
staff_token = 'e057191755dfd335f1a3c1a3eb3992e5765bef41'

headers={'Authorization': f'Token {staff_token}'}

get_response = requests.get(url=url, headers=headers)


print('status_code: ', get_response.status_code)
print(get_response.json())
