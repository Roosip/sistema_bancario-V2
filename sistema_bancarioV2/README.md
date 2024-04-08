# Documentação do Código

Nesta seção, faremos uma documentação detalhada das principais funções e características do código-fonte do projeto ROOSIP BANK.

## Variáveis Globais
- `saldo`: Armazena o saldo global da conta do usuário.
- `limite`: Define o limite de saque diário.
- `extrato`: Armazena o histórico de transações do usuário.
- `numero_saques`: Registra o número de saques realizados pelo usuário.
- `LIMITE_SAQUES`: Define o limite máximo de saques diários permitidos.

## Funções Principais
- `gerar_numero_conta()`: Gera números aleatórios para conta e agência.
- `menu_de_entrada()`: Exibe o menu de entrada para o usuário.
- `validar_login_usuario()`: Valida o login do usuário com base no nome e CPF fornecidos.
- `exibir_erro(mensagem)`: Exibe mensagens de erro formatadas.
- `validar_cpf(cpf)`: Valida o formato do CPF usando expressões regulares.
- `obter_entrada_usuario(mensagem, tipo, validacao=None)`: Solicita entrada do usuário com opção de validação.
- `atualizar_saldo(valor)`: Atualiza o saldo global do usuário.
- `adicionar_transacao_ao_extrato(descricao)`: Adiciona uma descrição de transação ao extrato global.
- `extrato_usuario(usuario_logado)`: Exibe o extrato de transações para o usuário logado.
- `listar_conta()`: Lista todas as contas armazenadas no arquivo JSON.
- `criar_nova_conta(usuario_logado)`: Cria uma nova conta com números de conta e agência gerados aleatoriamente.
- `menu_principal()`: Exibe o menu principal para o usuário.
- `criar_novo_usuario()`: Solicita informações do usuário e cria uma nova conta.
- `armazenar_dados_do_usuario(dados)`: Armazena os dados do usuário em um arquivo JSON.
- `atualizar_saldo_json(usuario, novo_saldo)`: Atualiza o saldo do usuário no arquivo JSON.
- `depositar(usuario_logado)`: Realiza um depósito na conta do usuário logado.
- `sacar(usuario_logado)`: Realiza um saque na conta do usuário logado.

## Fluxo Principal do Programa
O programa começa com um menu de entrada, onde o usuário pode escolher entre entrar em uma conta existente, criar um novo usuário ou sair do programa. Se o usuário optar por entrar em uma conta existente, será solicitado o nome e CPF para validação. Após o login bem-sucedido, o usuário terá acesso ao menu principal. No menu principal, o usuário pode escolher entre diferentes operações bancárias, como depósito, saque, visualização de extrato, entre outras. Caso seja um novo usuário, o usuário pode selecionar a opção "Criar novo usuário" no menu de entrada e preencher suas informações pessoais para registrar uma nova conta bancária.

## Notas Importantes
- Este projeto é apenas uma simulação bancária simples e não se conecta a nenhum banco real.
- Todas as informações de contas e transações são armazenadas localmente em um arquivo JSON (`dados_do_usuario.json`).
- Esta documentação fornece uma visão geral das principais funcionalidades e fluxos do código-fonte do projeto ROOSIP BANK. Para mais detalhes, consulte o código fonte diretamente.

# ROOSIP BANK

Bem-vindo ao ROOSIP BANK! Este é um projeto de simulação bancária simples desenvolvido em Python. Com este programa, você pode realizar diversas operações bancárias, como criar uma nova conta, fazer depósitos, sacar dinheiro, visualizar extratos e muito mais.

## Funcionalidades
- **Entrar em uma conta existente:** Se você já possui uma conta cadastrada, pode fazer login para acessar suas funcionalidades.
- **Criar novo usuário:** Se você é um novo cliente, pode criar uma nova conta no banco preenchendo suas informações pessoais.
- **Depositar:** Realize depósitos em sua conta bancária.
- **Sacar:** Faça saques de sua conta bancária, respeitando o limite diário estabelecido.
- **Extrato:** Visualize o extrato de transações da sua conta bancária.
- **Nova Consulta:** Realize uma nova consulta na sua conta bancária.
- **Listar Conta:** Veja uma lista de todas as contas cadastradas no banco.
- **Criar Nova Conta:** Crie uma nova conta no banco.
- **Novo Usuário:** Registre-se como um novo usuário do banco.
- **Sair:** Encerre o programa.

## Como Utilizar
Ao executar o programa, você será recebido com um menu de entrada, onde pode escolher entre entrar em uma conta existente, criar um novo usuário ou sair do programa. Se optar por entrar em uma conta existente, será solicitado seu nome completo e CPF para validação. Após o login bem-sucedido, você terá acesso ao menu principal, onde pode escolher entre as diferentes operações bancárias.

Caso seja um novo usuário, você pode selecionar a opção "Criar novo usuário" no menu de entrada e preencher suas informações pessoais para registrar uma nova conta bancária.

## Pré-Requisitos
Certifique-se de ter o Python instalado em sua máquina para executar este projeto.

## Como Executar
1. Clone este repositório em sua máquina:
    ```bash
    git clone https://github.com/seu-usuario/roosip-bank.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd roosip-bank
    ```
3. Execute o programa:
    ```bash
    python roosip_bank.py
    ```

## Notas
- Este projeto é apenas uma simulação bancária simples e não se conecta a nenhum banco real.
- Todas as informações de contas e transações são armazenadas localmente em um arquivo JSON (`dados_do_usuario.json`).




Espero que este README tenha sido útil! Se tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato. Obrigado por escolher o ROOSIP BANK! 🏦💰
