import requests

create_user_data = {
    'username': 'raxit',
    'email': 'raxit@vmail.com',
    'password': '12345678'
}

res = requests.post('http://127.0.0.1:5000/create_user', json=create_user_data)

print(res.text)

# create_question_data = {
#     'qcontent': 'This is first question'
# }

# res = requests.post('http://127.0.0.1:5000/create_question', json=create_question_data)
# print(res.text)

