import textwrap
import json
import re
from datetime import datetime

saldo = 0.0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Função para exibir mensagens de erro
def exibir_erro(mensagem):
    print(f"Erro: {mensagem}")

# Função para validar CPF
def validar_cpf(cpf):
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        raise ValueError("O CPF fornecido está em um formato inválido. Por favor, insira no formato 'XXX.XXX.XXX-XX'.")
    return True

# Função para obter entrada do usuário com validação
def obter_entrada_usuario(mensagem, tipo, validacao=None):
    while True:
        try:
            entrada = tipo(input(mensagem))
            if validacao is not None and not validacao(entrada):
                raise ValueError("Entrada inválida. Por favor, tente novamente.")
            return entrada
        except ValueError as e:
            exibir_erro(e)

# Função para atualizar saldo
def atualizar_saldo(valor):
    global saldo
    saldo += valor

# Função para adicionar transação ao extrato
def adicionar_transacao_ao_extrato(descricao):
    global extrato
    extrato += descricao + "\n"

# FUNÇÃO DO MENU
def menu():
    menu_texto = '''\n
    ==========MENU==========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Consulta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    =>: '''
    return input(textwrap.dedent(menu_texto))

# FUNÇÃO CRIAR NOVO USUÁRIO
def criar_novo_usuario():
    dados_do_usuario = {}
    while True:
        try:
            dados_do_usuario["nome"] = obter_entrada_usuario("Digite o seu nome completo: ", str)
            if not dados_do_usuario["nome"]:
                raise ValueError("O nome não pode estar vazio.")
            
            while True:
                data_de_nascimento_str = obter_entrada_usuario("Digite a sua data de nascimento (DD/MM/AAAA): ", str)
                try:
                    data_de_nascimento = datetime.strptime(data_de_nascimento_str, "%d/%m/%Y")
                    if datetime.now().year - data_de_nascimento.year < 18:
                        raise ValueError("A idade deve ser maior ou igual a 18 anos.")
                    dados_do_usuario["data_nascimento"] = data_de_nascimento.strftime("%d/%m/%Y")
                    break  # Se a data for válida e a idade for maior ou igual a 18 anos, sai do loop
                except ValueError:
                    print("Formato de data inválido. Por favor, insira a data no formato DD/MM/AAAA.")

            
            cpf = obter_entrada_usuario("Digite os 11 digitos do seu cpf, sem pontos e traços: ", str, validar_cpf)
            dados_do_usuario["cpf"] = cpf
            
            dados_do_usuario["logradouro"] = obter_entrada_usuario("Digite o seu logdrouro: ", str)
            if not dados_do_usuario["logradouro"]:
                raise ValueError("O logradouro não pode estar vazio.")
            
            dados_do_usuario["numero"] = obter_entrada_usuario("Digite o numero do seu endereço: ", int)
            if not dados_do_usuario["numero"]:
                raise ValueError("O numero da residência deve conter apenas numeros.")
            
            dados_do_usuario["bairro"] = obter_entrada_usuario("Digite o nome do seu bairro: ", str)
            if not dados_do_usuario["bairro"]:
                raise ValueError("O nome do bairro não pode estar vazio.")
            
            dados_do_usuario["cidade"] = obter_entrada_usuario("Digite o nome da sua cidade: ", str)
            if not dados_do_usuario["cidade"]:
                raise ValueError("O nome da cidade não pode estar vazio.")
            
            dados_do_usuario["unidade_federal"] = obter_entrada_usuario("Digite a sua Unidade Federal. Ex: 'SP', 'RJ':", str)
            if not dados_do_usuario['unidade_federal']:
                raise ValueError("A unidade federal não pode estar vazia.")
            
            dados_do_usuario["estado"] = obter_entrada_usuario("Digite o nome do seu estado: ", str)
            if not dados_do_usuario["estado"]:
                raise ValueError("O estado não pode estar vazio.")
            
            break

        except ValueError as e:
            exibir_erro(e)
        
    return dados_do_usuario

# FUNÇÃO ARMAZENAR DADOS DO USUÁRIO
def armazenar_dados_do_usuario(dados):
    try:
        with open('dados_do_usuario.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        usuarios = []

    usuarios.append(dados)

    with open('dados_do_usuario.json', 'w') as arquivo:
        json.dump(usuarios, arquivo, indent=4)

    print("Informações salvas com sucesso!")
# FUNÇÃO DEPOSITAR
def depositar():
    valor_depositado = obter_entrada_usuario("Por favor, digite o valor do depósito: ", float)
    if valor_depositado <= 0:
        exibir_erro("O valor do depósito deve ser maior que zero.")
        return
    atualizar_saldo(valor_depositado)
    adicionar_transacao_ao_extrato(f"Depósito de R${valor_depositado:.2f}")
    print(f"Seu saldo atualizado é de: R${saldo:.2f}")

# FUNÇÃO SACAR
def sacar():
    global numero_saques
    if numero_saques >= LIMITE_SAQUES:
        print("Você atingiu a quantidade de saques diários, volte outro dia.")
        return
    
    valor_saque = obter_entrada_usuario("Digite o valor que deseja sacar: ", float)
    if valor_saque <= 0:
        exibir_erro("O valor do saque deve ser maior que zero.")
        return
    if valor_saque > saldo:
        exibir_erro("Valor de saque inválido, pois seu saldo é insuficiente.")
        return
    if valor_saque > limite:
        exibir_erro("O valor de saque é maior que o limite diário.")
        return
    
    saldo -= valor_saque
    numero_saques += 1
    limite -= valor_saque
    adicionar_transacao_ao_extrato(f"Saque de R${valor_saque:.2f}")
    print(f"Seu saque de R${valor_saque:.2f} foi realizado com sucesso!\n"
            f"Seu saldo atual é: R${saldo:.2f}\n"
            f"Seu número de saques é de: {numero_saques} de {LIMITE_SAQUES} saques\n"
            f"Seu limite diário é de: R${limite:.2f}.")

informacoes_do_usuario = "dados_do_usuario.json"

while True:
    opcao = menu()

    if opcao == "d":
        depositar()
    
    elif opcao == "s":
        sacar()
    
    elif opcao == "nu":
        informacoes = criar_novo_usuario()
        armazenar_dados_do_usuario(informacoes)

    elif opcao == "q":
        break
