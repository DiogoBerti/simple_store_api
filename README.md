# Simple Store API

Certifique-se de que possui o Docker e o Docker Compose intalados.
Clone a o repositório, navegue até a pasta e rodar o comando "docker-compose up --build"
A Api funciona com autenticação via JWT. para logar, utilizar a rota "api/token/" para criar o token (ou atualizar com o "api/token/refresh/")
e utilizar o token do campo "access" como Bearer no header da requisição.
Os testes irão rodar na subida do sistema.

# Documentação
Para acessar a documentação, ao subir o docker (comando acima), navegar até http://localhost:8000/redoc/ ou http://localhost:8000/swagger/

# Padrões
Usuário padrão:
    - user: root
    - password: admin
* O Usuário também funciona para a API

# OBS
Caso necessário, é possível acessar o Django Admin (http://localhost:8000/admin/) para verificar os dados nas tabelas e outras configurações.
A senha é a mesma informada em padrões
