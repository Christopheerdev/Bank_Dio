menu = """"

[d] Depositar
[s] Sacar
[e] Extrato
[x] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Digite o valor a ser depositado: "))

        if valor > 0:
            saldo += valor
            extrato += f"Deposito: R$ {valor:.2f} \n"
            print(f"O seu depósito de R$ {valor:.2f} foi realizado com sucesso!")
           

        else:
            print("Operação falhou, o valor informado é invalido")


    elif opcao == "s":
        valor = float(input("Digite valor do saque desejado!"))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Voce não possui saldo suficiente...")

        elif excedeu_limite:
            print("Operação não realizada, voçê não possui limite suficiente para sacar o valor desejado!")

        elif excedeu_saques:
            print("Operação nao realizada. Voçê atingiu limite de saques diários!")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f} \n"
            numero_saques += 1

        else:
            print("Operação falhou.O valor informado é invalido!")


    elif opcao == "e":
         print("\n ==========EXTRATO==========")
         print("Não foram realizadas movimentações" if not extrato else extrato)
         print(f"\n Saldo: R$ {saldo:.2f}")
         print("====================================")

    elif opcao == "x":
        break


    else:
        print("Por favor selecione uma opção valida!")



