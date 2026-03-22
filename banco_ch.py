import textwrap

# ============================
#   CLASSES
# ============================

class Usuario:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco


class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = ""

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Valor inválido! @@@")


class ContaCorrente(Conta):
    def __init__(self, agencia, numero_conta, usuario, limite=500, limite_saques=3):
        super().__init__(agencia, numero_conta, usuario)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Saldo insuficiente! @@@")

        elif valor > self.limite:
            print("\n@@@ Valor excede o limite! @@@")

        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Número máximo de saques atingido! @@@")

        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Valor inválido! @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")


# ============================
#   SISTEMA
# ============================

usuarios = []
contas = []
AGENCIA = "0001"


# ------------------------------------------
# Funções auxiliares
# ------------------------------------------

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_usuario(cpf):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None


def criar_usuario():
    cpf = input("Informe o CPF: ")

    if filtrar_usuario(cpf):
        print("\n@@@ Usuário já existe! @@@")
        return

    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento: ")
    endereco = input("Endereço: ")

    usuario = Usuario(nome, cpf, data_nascimento, endereco)
    usuarios.append(usuario)

    print("=== Usuário criado com sucesso! ===")


def criar_conta():
    cpf = input("CPF do usuário: ")
    usuario = filtrar_usuario(cpf)

    if not usuario:
        print("\n@@@ Usuário não encontrado! @@@")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente(AGENCIA, numero_conta, usuario)
    contas.append(conta)

    print("=== Conta criada com sucesso! ===")


def listar_contas():
    for conta in contas:
        print("=" * 40)
        print(f"Agência:\t{conta.agencia}")
        print(f"Conta:\t\t{conta.numero_conta}")
        print(f"Titular:\t{conta.usuario.nome}")


def selecionar_conta():
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuario(cpf)

    if not usuario:
        print("Usuário não encontrado.")
        return None

    for conta in contas:
        if conta.usuario == usuario:
            return conta

    print("Conta não encontrada.")
    return None


# ============================
#   MAIN
# ============================

def main():
    while True:
        opcao = menu()

        if opcao == "nu":
            criar_usuario()

        elif opcao == "nc":
            criar_conta()

        elif opcao == "lc":
            listar_contas()

        elif opcao == "d":
            conta = selecionar_conta()
            if conta:
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)

        elif opcao == "s":
            conta = selecionar_conta()
            if conta:
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)

        elif opcao == "e":
            conta = selecionar_conta()
            if conta:
                conta.exibir_extrato()

        elif opcao == "q":
            print("Encerrando...")
            break

        else:
            print("Opção inválida!")


# ============================
# EXECUÇÃO
# ============================

main()
