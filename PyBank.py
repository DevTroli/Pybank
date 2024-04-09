import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Classe que representa um Cliente
class Cliente:
    def __init__(self, endereco):
        """
        Inicializa o objeto Cliente.

        Args:
            endereco (str): Endereço do cliente.
        """
        self.endereco = endereco
        self.contas = []  # Lista para armazenar as contas associadas ao cliente

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação para a conta associada ao cliente.

        Args:
            conta (Conta): Conta associada ao cliente.
            transacao (Transacao): Transação a ser realizada.
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona uma conta à lista de contas do cliente.

        Args:
            conta (Conta): Conta a ser adicionada.
        """
        self.contas.append(conta)

# Classe que representa uma Pessoa Física, que é um tipo de Cliente
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        """
        Inicializa um objeto PessoaFisica.

        Args:
            nome (str): Nome da pessoa física.
            data_nascimento (str): Data de nascimento da pessoa física (formato: dd-mm-aaaa).
            cpf (str): CPF da pessoa física.
            endereco (str): Endereço da pessoa física.
        """
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe abstrata que representa uma Conta
class Conta:
    def __init__(self, numero, cliente):
        """
        Inicializa um objeto Conta.

        Args:
            numero (int): Número da conta.
            cliente (Cliente): Cliente associado à conta.
        """
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()  # Instância do histórico de transações

    @classmethod
    def nova_conta(cls, cliente, numero):
        """
        Cria uma nova instância de Conta.

        Args:
            cliente (Cliente): Cliente associado à conta.
            numero (int): Número da conta.

        Returns:
            Conta: Nova instância de Conta.
        """
        return cls(numero, cliente)

    @property
    def saldo(self):
        """Getter para o saldo da conta."""
        return self._saldo

    @property
    def numero(self):
        """Getter para o número da conta."""
        return self._numero

    @property
    def agencia(self):
        """Getter para a agência da conta."""
        return self._agencia

    @property
    def cliente(self):
        """Getter para o cliente associado à conta."""
        return self._cliente

    @property
    def historico(self):
        """Getter para o histórico de transações da conta."""
        return self._historico

    def sacar(self, valor):
        """
        Realiza uma operação de saque na conta.

        Args:
            valor (float): Valor a ser sacado.

        Returns:
            bool: Verdadeiro se o saque foi bem-sucedido, Falso caso contrário.
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        """
        Realiza uma operação de depósito na conta.

        Args:
            valor (float): Valor a ser depositado.

        Returns:
            bool: True se o depósito foi bem-sucedido, False caso contrário.
        """
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

# Classe que representa uma Conta Corrente, que é um tipo de Conta
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        """
        Inicializa um objeto ContaCorrente.

        Args:
            numero (int): Número da conta corrente.
            cliente (Cliente): Cliente associado à conta.
            limite (float, optional): Limite de saldo negativo permitido na conta. Defaults to 500.
            limite_saques (int, optional): Número máximo de saques permitidos na conta. Defaults to 3.
        """
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """
        Realiza uma operação de saque na conta corrente, considerando limites.

        Args:
            valor (float): Valor a ser sacado.

        Returns:
            bool: True se o saque foi bem-sucedido, False caso contrário.
        """
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        """
        Retorna uma representação em string da conta corrente.

        Returns:
            str: Representação em string da conta corrente.
        """
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Classe que representa o histórico de transações de uma conta
class Historico:
    def __init__(self):
        """Inicializador da classe Historico."""
        self._transacoes = []

    @property
    def transacoes(self):
        """
        Getter para as transações registradas no histórico.

        Returns:
            list: Lista de transações realizadas na conta.
        """
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico.

        Args:
            transacao (Transacao): Transação a ser registrada.
        """
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

# Classe abstrata que representa uma transação
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        """Getter para o valor da transação."""
        pass

    @abstractclassmethod
    def registrar(self, conta):
        """
        Método abstrato para registrar uma transação.

        Args:
            conta (Conta): Conta na qual a transação será registrada.
        """
        pass

# Classe que representa uma transação de saque
class Saque(Transacao):
    def __init__(self, valor):
        """
        Inicializa um objeto Saque.

        Args:
            valor (float): Valor do saque.
        """
        self._valor = valor

    @property
    def valor(self):
        """Getter para o valor do saque."""
        return self._valor

    def registrar(self, conta):
        """
        Registra um saque na conta.

        Args:
            conta (Conta): Conta na qual o saque será registrado.
        """
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Classe que representa uma transação de depósito
class Deposito(Transacao):
    def __init__(self, valor):
        """
        Inicializa um objeto Deposito.

        Args:
            valor (float): Valor do depósito.
        """
        self._valor = valor

    @property
    def valor(self):
        """Getter para o valor do depósito."""
        return self._valor

    def registrar(self, conta):
        """
        Registra um depósito na conta.

        Args:
            conta (Conta): Conta na qual o depósito será registrado.
        """
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Função que exibe o menu principal do sistema
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

# Função que filtra um cliente por CPF
def filtrar_cliente(cpf, clientes):
    """
    Filtra um cliente por CPF.

    Args:
        cpf (str): CPF a ser procurado.
        clientes (list): Lista de clientes do banco.

    Returns:
        Cliente: Cliente encontrado ou None se não encontrado.
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função que recupera a primeira conta de um cliente
def recuperar_conta_cliente(cliente):
    """
    Recupera a primeira conta de um cliente.

    Args:
        cliente (Cliente): Cliente do qual se quer recuperar a conta.

    Returns:
        Conta: Primeira conta do cliente ou None se não houver contas.
    """
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

# Função para realizar um depósito
def depositar(clientes):
    """
    Realiza um depósito na conta de um cliente.

    Args:
        clientes (list): Lista de clientes do banco.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para realizar um saque
def sacar(clientes):
    """
    Realiza um saque na conta de um cliente.

    Args:
        clientes (list): Lista de clientes do banco.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para exibir o extrato de uma conta
def exibir_extrato(clientes):
    """
    Exibe o extrato de uma conta de um cliente.

    Args:
        clientes (list): Lista de clientes do banco.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

# Função para criar um novo cliente
def criar_cliente(clientes):
    """
    Cria um novo cliente.

    Args:
        clientes (list): Lista de clientes do banco.
    """
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

# Função para criar uma nova conta
def criar_conta(numero_conta, clientes, contas):
    """
    Cria uma nova conta.

    Args:
        numero_conta (int): Número da nova conta.
        clientes (list): Lista de clientes do banco.
        contas (list): Lista de contas do banco.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

# Função para listar todas as contas do banco
def listar_contas(contas):
    """
    Lista todas as contas do banco.

    Args:
        contas (list): Lista de contas do banco.
    """
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# Função principal que controla o fluxo do programa
def main():
    clientes = []  # Lista para armazenar os clientes do banco
    contas = []  # Lista para armazenar as contas do banco

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()

