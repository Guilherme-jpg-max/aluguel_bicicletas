# Sistema de Aluguel de Bicicletas

Este sistema foi desenvolvido para fins acadêmicos, visando simular um serviço de aluguel de bicicletas.
O projeto permite que usuários realizem o cadastro, efetuem login, verifiquem o saldo, aluguem bicicletas
e escolham estações para retirar ou devolver bicicletas. O sistema também possui um painel de administração,
onde os administradores podem gerenciar as estações e bicicletas disponíveis.

# Funcionalidades

Para Administradores:
Cadastro de Administradores: Permite o cadastro de novos administradores para gerenciar o sistema.
Gerenciamento de Estações e Bicicletas: Administradores podem adicionar, editar e excluir estações e bicicletas no sistema.

# Para Usuários Comuns:

- Cadastro de Usuários: Usuários podem criar uma conta no sistema.
- Login de Usuários: Usuários podem acessar o sistema utilizando suas credenciais.
- Aluguel de Bicicletas: Usuários podem alugar bicicletas de estações específicas.
- Adição de Saldo: Usuários podem adicionar saldo à sua conta para realizar aluguéis.
- Verificação de Saldo: Usuários podem visualizar seu saldo disponível para aluguel.
- Funcionalidades Comuns para Administradores e Usuários:
- Autenticação: Controle de acesso para garantir que apenas usuários autenticados possam acessar funcionalidades específicas.
- Consulta de Bicicletas Disponíveis: Usuários podem visualizar as bicicletas disponíveis em cada estação.
- Devolução de Bicicletas: Após o uso, os usuários podem devolver as bicicletas na estação escolhida.

# Tecnologias Utilizadas

- Flask: Framework web utilizado para o desenvolvimento do sistema.
- SQLAlchemy: ORM (Object-Relational Mapping) para interação com o banco de dados.
-Jinja2: Motor de templates utilizado para renderizar as páginas web.

# Como Executar

# Pré-requisitos:
- Certifique-se de ter o Python 3.7 ou superior instalado.

# Instalação:
   1- Clone o repositório:
   git clone https://github.com/Guilherme-jpg-max/aluguel_bicicletas.git

   2- Navegue até o diretório do projeto:
   cd aluguel_bicicletas
   
   3- Crie e ative um ambiente virtual (opcional, mas recomendado):
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate

   4- Instale as dependências do projeto:
   pip install -r requirements.txt

   5- Inicie o servidor Flask:
   flask run
