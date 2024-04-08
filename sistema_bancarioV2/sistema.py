import textwrap
import json
import re
from datetime import datetime
from colorama import Fore, Back, Style
from random import randint

# Variáveis globais
saldo = 0.0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

# Função para gerar número de conta e agência
def gerar_numero_conta():
    # Gera um número de conta e uma agência aleatórios
    numero_conta = randint(10000, 99999)
    numero_agencia = randint(1000, 9999)
    return numero_conta, numero_agencia

# Função para exibir o menu de entrada
def menu_de_entrada():
    # Exibe o menu de entrada para o usuário escolher uma opção
    texto_menu_de_entrada = f'''\n
    {Fore.LIGHTYELLOW_EX}==================================ROOSIP BANK======================================={Style.RESET_ALL}
    = Olá, seja bem-vindo ao {Fore.LIGHTYELLOW_EX}ROOSIP BANK{Style.RESET_ALL}. Escolha uma das opções do que deseja fazer.  =
    = [lo]\tEntrar em uma conta existente                                              =
    = [nu]\tCriar novo usuário                                                         =
    = [q]\tSair                                                                       =
    {Fore.LIGHTYELLOW_EX}===================================================================================={Style.RESET_ALL}
    {Fore.LIGHTBLUE_EX}Opção{Style.RESET_ALL}: '''
    return input(textwrap.dedent(texto_menu_de_entrada))

# Função para validar o login do usuário
def validar_login_usuario():
    # Solicita nome e CPF ao usuário e valida no arquivo JSON
    while True:
        try:
            nome = obter_entrada_usuario("Digite o seu nome completo: ", str)
            cpf = obter_entrada_usuario("Digite os 11 dígitos do seu CPF no formato 'XXX.XXX.XXX-XX': ", str, validar_cpf)

            with open('dados_do_usuario.json', 'r') as arquivo:
                usuarios = json.load(arquivo)

            for usuario in usuarios:
                if usuario["nome"] == nome and usuario["cpf"] == cpf:
                    print(f"{Fore.GREEN}======= Login bem-sucedido! ======={Style.RESET_ALL}")
                    return usuario  # Retorna os dados do usuário encontrado

            print("Usuário não encontrado. Por favor, verifique suas informações e tente novamente.")
            return None

        except ValueError as e:
            exibir_erro(e)

# Função para exibir mensagens de erro
def exibir_erro(mensagem):
    # Exibe mensagens de erro formatadas
    print(f"Erro: {mensagem}")

# Função para validar CPF
def validar_cpf(cpf):
    # Valida o formato do CPF usando uma expressão regular
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        raise ValueError("O CPF fornecido está em um formato inválido. Por favor, insira no formato 'XXX.XXX.XXX-XX'.")
    return True

# Função para obter entrada do usuário com validação
def obter_entrada_usuario(mensagem, tipo, validacao=None):
    # Solicita entrada do usuário e valida de acordo com o tipo e, opcionalmente, uma função de validação
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
    # Atualiza o saldo global
    global saldo
    saldo += valor

# Função para adicionar transação ao extrato
def adicionar_transacao_ao_extrato(descricao):
    # Adiciona uma descrição de transação ao extrato global
    global extrato
    extrato += descricao + "\n"

# Lista de histórico de transações
historico_transacoes = []

# Função para exibir o extrato do usuário
def extrato_usuario(usuario_logado):
    # Exibe o extrato de transações para o usuário logado
    print(f"{Fore.LIGHTYELLOW_EX}==================== Extrato ===================={Style.RESET_ALL}")
    for transacao in historico_transacoes:
        if transacao[0] == 'deposito':
            print(f"Depósito de {Fore.LIGHTYELLOW_EX}R${transacao[1]:.2f}{Style.RESET_ALL} em {transacao[2]}")
        elif transacao[0] == 'saque':
            print(f"Saque de {Fore.LIGHTRED_EX}R${transacao[1]:.2f}{Style.RESET_ALL} em {transacao[2]}")
    print(f"Saldo atual: {Fore.LIGHTGREEN_EX}R${usuario_logado['saldo']:.2f}{Style.RESET_ALL}")
    print(f"Limite de saques: {LIMITE_SAQUES}")
    print(f"Número de saques restantes: {LIMITE_SAQUES - numero_saques}")
    print(f"{Fore.LIGHTYELLOW_EX}=================================================={Style.RESET_ALL}")

# Função para listar todas as contas
def listar_conta():
    # Lista todas as contas armazenadas no arquivo JSON
    try:
        with open('dados_do_usuario.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        print("Não há usuários cadastrados.")
        return

    print(f"\n{Fore.LIGHTYELLOW_EX}======== Lista de Contas ========{Style.RESET_ALL}")
    for idx, usuario in enumerate(usuarios, 1):
        print(f"{idx}. Conta: {usuario['numero_conta']} | Agência: {usuario['numero_agencia']} | Nome: {usuario['nome']}")
    print(f"{Fore.LIGHTYELLOW_EX}================================={Style.RESET_ALL}")

# Função para criar uma nova conta
def criar_nova_conta(usuario_logado):
    # Cria uma nova conta com um número de conta e agência gerados aleatoriamente
    nova_conta = {}
    numero_conta, numero_agencia = gerar_numero_conta()
    
    nova_conta["nome"] = usuario_logado["nome"]
    nova_conta["cpf"] = usuario_logado["cpf"]
    nova_conta["numero_conta"] = numero_conta
    nova_conta["numero_agencia"] = numero_agencia
    nova_conta["saldo"] = 0.0

    armazenar_dados_do_usuario(nova_conta)
    print(f"{Fore.GREEN}Nova conta criada com sucesso!{Style.RESET_ALL}")

# Função para exibir o menu principal
def menu_principal():
    # Exibe o menu principal para o usuário
    menu_texto = f'''\n
    {Fore.LIGHTYELLOW_EX}==========MENU=========={Style.RESET_ALL}
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Consulta
    [lc]\tListar Conta
    [cnc]\tCriar Nova Conta
    [nu]\tNovo Usuário
    [q]\tSair
        ==>: '''
    return input(textwrap.dedent(menu_texto))

# Função para criar um novo usuário
def criar_novo_usuario():
    # Solicita informações do usuário e cria um novo usuário
    dados_do_usuario = {}
    numero_conta, numero_agencia = gerar_numero_conta()
    while True:
        try:
            dados_do_usuario["nome"] = obter_entrada_usuario("Digite o seu nome completo: ", str)
            if not dados_do_usuario["nome"]:
                raise ValueError("O nome não pode estar vazio.")
            
            # Solicita e valida a data de nascimento
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

            # Solicita e valida o CPF
            cpf = obter_entrada_usuario("Digite os 11 dígitos do seu CPF no formato 'XXX.XXX.XXX-XX': ", str, validar_cpf)
            dados_do_usuario["cpf"] = cpf
            
            # Solicita informações de endereço
            dados_do_usuario["logradouro"] = obter_entrada_usuario("Digite o seu logradouro: ", str)
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
            
            dados_do_usuario["numero_conta"] = numero_conta
            dados_do_usuario["numero_agencia"] = numero_agencia
            
            break

        except ValueError as e:
            exibir_erro(e)
        
    return dados_do_usuario

# Função para armazenar os dados do usuário em um arquivo JSON
def armazenar_dados_do_usuario(dados):
    # Armazena os dados do usuário no arquivo JSON
    try:
        with open('dados_do_usuario.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        usuarios = []
    
    dados["saldo"] = saldo

    usuarios.append(dados)

    with open('dados_do_usuario.json', 'w') as arquivo:
        json.dump(usuarios, arquivo, indent=4)

    print(f"{Fore.GREEN}===== Informações salvas com sucesso! ====={Style.RESET_ALL}")
    print(f"== Agora você pode acessar sua conta através do menu inicial. ==")

# Função para atualizar o saldo do usuário no arquivo JSON
def atualizar_saldo_json(usuario, novo_saldo):
    # Atualiza o saldo do usuário no arquivo JSON
    try:
        with open('dados_do_usuario.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo de dados do usuário não encontrado.")
        return

    for u in usuarios:
        if u["cpf"] == usuario["cpf"]:
            u["saldo"] = novo_saldo

    with open('dados_do_usuario.json', 'w') as arquivo:
        json.dump(usuarios, arquivo, indent=4)

    print(f"{Fore.GREEN}Saldo atualizado com sucesso no arquivo.{Style.RESET_ALL}")

# Função para realizar um depósito
def depositar(usuario_logado):
    # Realiza um depósito na conta do usuário logado
    global saldo
    valor_depositado = obter_entrada_usuario("Por favor, digite o valor do depósito: ", float)
    if valor_depositado <= 0:
        exibir_erro("O valor do depósito deve ser maior que zero.")
        return
    novo_saldo = usuario_logado["saldo"] + valor_depositado
    atualizar_saldo_json(usuario_logado, novo_saldo)
    adicionar_transacao_ao_extrato(f"Depósito de R${Fore.GREEN}{valor_depositado:.2f}{Style.RESET_ALL}")
    historico_transacoes.append(('deposito', valor_depositado, datetime.now()))
    print(f"Seu saldo atualizado é de: {Fore.GREEN}R${novo_saldo:.2f}{Style.RESET_ALL}")

# Função para realizar um saque
def sacar(usuario_logado):
    # Realiza um saque na conta do usuário logado
    global numero_saques, limite
    if numero_saques >= LIMITE_SAQUES:
        print("Você atingiu a quantidade de saques diários, volte outro dia.")
        return
    
    valor_saque = obter_entrada_usuario("Digite o valor que deseja sacar: ", float)
    if valor_saque <= 0:
        exibir_erro("O valor do saque deve ser maior que zero.")
        return
    if valor_saque > usuario_logado["saldo"]:
        exibir_erro("Valor de saque inválido, pois seu saldo é insuficiente.")
        return
    if valor_saque > limite:
        exibir_erro("O valor de saque é maior que o limite diário.")
        return
    
    novo_saldo = usuario_logado["saldo"] - valor_saque
    atualizar_saldo_json(usuario_logado, novo_saldo)
    numero_saques += 1
    limite -= valor_saque
    adicionar_transacao_ao_extrato(f"Saque de {Fore.LIGHTRED_EX}R${valor_saque:.2f}{Style.RESET_ALL}")
    historico_transacoes.append(('saque', valor_saque, datetime.now()))
    print(f"Seu saque de R${valor_saque:.2f} foi realizado com sucesso!\n"
            f"Seu saldo atual é: {Fore.LIGHTGREEN_EX}R${novo_saldo:.2f}{Style.RESET_ALL}\n"
            f"Seu número de saques é de: {numero_saques} de {LIMITE_SAQUES} saques\n"
            f"Seu limite diário é de: R${limite:.2f}.")

# Loop principal do programa
while True:
    opcao_menu_de_entrada = menu_de_entrada()
    
    if opcao_menu_de_entrada == "lo":
        usuario_encontrado = validar_login_usuario()
        if usuario_encontrado:
            print(f"== Bem-vindo de volta,", usuario_encontrado["nome"],"! ==")
            print("Escolha uma das opções abaixo, fique à vontade!")
            while True:
                opcao_menu_principal = menu_principal()

                if opcao_menu_principal == "d":
                    depositar(usuario_encontrado)
                
                elif opcao_menu_principal == "s":
                    sacar(usuario_encontrado)
                
                elif opcao_menu_principal == "e":
                    extrato_usuario(usuario_encontrado)
                
                elif opcao_menu_principal == "nu":
                    informacoes = criar_novo_usuario()
                    armazenar_dados_do_usuario(informacoes)

                elif opcao_menu_principal == "lc":
                    listar_conta()

                elif opcao_menu_principal == "cnc":
                    criar_nova_conta(usuario_encontrado)

                elif opcao_menu_principal == "q":
                    break
        else:
            continue  # Retorna ao menu de entrada se o login falhar

    elif opcao_menu_de_entrada == "nu":
        informacoes = criar_novo_usuario()
        armazenar_dados_do_usuario(informacoes)

    elif opcao_menu_de_entrada == "q":
        break
