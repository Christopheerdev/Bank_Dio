import textwrap
from abc import ABC, abstractmethod

# ============================
#   HISTORICO
# ============================

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def gerar_extrato(self):
        extrato = ""

        if not self._transacoes:
            extrato = "Não foram realizadas movimentações.\n"

        for transacao in self._transacoes:
            extrato += (
                f"{transacao.__class__.__name__}: "
                f"R$ {transacao.valor:.2f}\n"
            )

        return extrato


# ============================
#   TRANSACAO (ABSTRAÇÃO)
# ============================

class Transacao(ABC):

    @abstractmethod
    def registrar(self, conta):
        pass


# ============================
#   DEPOSITO
# ============================

class Deposito(Transacao):

    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)


# ============================
#   SAQUE
# ============================

class Saque(Transacao):

    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)


# ============================
#   CLIENTE
# ============================

class Cliente:

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# ============================
#   PESSOA FISICA (HERANÇA)
# ============================

class PessoaFisica(Cliente):

    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)

        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# ============================
#   CONTA
# ============================

class Conta:

    def __init__(self, numero, agencia, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, "0001", cliente)

    def saldo(self):
        return self._saldo

    def sacar(self, valor):

        if valor > self._saldo:
            print("\n@@@ Saldo insuficiente! @@@")
            return False

        elif valor <= 0:
            print("\n@@@ Valor inválido! @@@")
            return False

        self._saldo -= valor

        print("\n=== Saque realizado com sucesso! ===")

        return True

    def depositar(self, valor):

        if valor <= 0:
            print("\n@@@ Valor inválido! @@@")
            return False

        self._saldo += valor

        print("\n=== Depósito realizado com sucesso! ===")

        return True


# ============================
#   CONTA CORRENTE (HERANÇA)
# ============================

class ContaCorrente(Conta):

    def __init__(
        self,
        numero,
        cliente,
        limite=500,
        limite_saques=3,
        agencia="0001"
    ):
        super().__init__(numero, agencia, cliente)

        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):

        if valor > self._saldo:
            print("\n@@@ Saldo insuficiente! @@@")
            return False

        elif valor > self.limite:
            print("\n@@@ Valor excede o limite! @@@")
            return False

        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Número máximo de saques atingido! @@@")
            return False

        elif valor <= 0:
            print("\n@@@ Valor inválido! @@@")
            return False

        self._saldo -= valor
        self.numero_saques += 1

        print("\n=== Saque realizado com sucesso! ===")

        return True


# ============================
#   SISTEMA
# ============================

usuarios = []
contas = []


def menu():
    menu = """\n
    ================ MENU ================
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
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

    usuario = PessoaFisica(
        nome,
        cpf,
        data_nascimento,
        endereco
    )

    usuarios.append(usuario)

    print("\n=== Usuário criado com sucesso! ===")


def criar_conta():

    cpf = input("Informe o CPF do usuário: ")

    usuario = filtrar_usuario(cpf)

    if not usuario:
        print("\n@@@ Usuário não encontrado! @@@")
        return

    numero_conta = len(contas) + 1

    conta = ContaCorrente(
        numero_conta,
        usuario
    )

    usuario.adicionar_conta(conta)

    contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas():

    for conta in contas:

        print("=" * 40)

        print(f"Agência:\t{conta._agencia}")
        print(f"Conta:\t\t{conta._numero}")
        print(f"Titular:\t{conta._cliente.nome}")


def selecionar_conta():

    cpf = input("Informe o CPF: ")

    usuario = filtrar_usuario(cpf)

    if not usuario:
        print("\nUsuário não encontrado.")
        return None

    if not usuario.contas:
        print("\nUsuário não possui conta.")
        return None

    return usuario.contas[0]


def exibir_extrato(conta):

    print("\n================ EXTRATO ================")

    print(conta.historico.gerar_extrato())

    print(f"Saldo:\t\tR$ {conta.saldo():.2f}")

    print("==========================================")


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

                transacao = Deposito(valor)

                conta._cliente.realizar_transacao(
                    conta,
                    transacao
                )

        elif opcao == "s":

            conta = selecionar_conta()

            if conta:

                valor = float(input("Valor do saque: "))

                transacao = Saque(valor)

                conta._cliente.realizar_transacao(
                    conta,
                    transacao
                )

        elif opcao == "e":

            conta = selecionar_conta()

            if conta:

                exibir_extrato(conta)

        elif opcao == "q":

            print("Encerrando...")
            break

        else:

            print("Opção inválida!")


# ============================
# EXECUÇÃO
# ============================

main()
