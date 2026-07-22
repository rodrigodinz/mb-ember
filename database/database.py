from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    VARCHAR,
    DateTime,
    Date,
    Enum,
    DECIMAL,
    JSON
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

database = create_engine("sqlite:///database.db")

Session = sessionmaker(bind=database)
session = Session()

Base = declarative_base()

# ======================CRIAR AS TABELAS=======================


class Usuario(Base):
    __tablename__ = "Usuarios"

    id = Column("id_usuario", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome_usuario", VARCHAR)
    email = Column("email_usuario", VARCHAR)
    senha_hash = Column("senha_usuario", VARCHAR)
    perfil = Column(
        "perfil_usuario", Enum("vendedor", "usuario", "admin", name="perfil_usuario")
    )
    ativo = Column("ativo_usuario", Boolean)
    data_cadastro = Column("data_cadastro_usuario", DateTime)

    def __init__(self, nome, email, senha_hash, perfil, ativo=True):
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.perfil = perfil
        self.ativo = ativo

    # autenticar(email, senha) - boolean
    # alterarSenha(novaSenha) - Void
    # obterMeusDados () - Usuario


class Log_Acesso(Base):
    __tablename__ = "Log de acesso"

    id_log_acesso = Column("id_acesso", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    data_hora = Column("datahora_log", DateTime)
    ip = Column("ip_log", VARCHAR)
    sucesso = Column("sucesso_log", Boolean)

    def __init__(self, id_usuario, data_hora, ip, sucesso):
        self.id_usuario = id_usuario
        self.data_hora = data_hora
        self.ip = ip
        self.sucesso = sucesso

    # registrarAcesso (sucesso, ip) - void


class Churrasqueira(Base):
    __tablename__ = "Churrasqueira"

    id_churrasqueira = Column(
        "id_churrasqueira", Integer, primary_key=True, autoincrement=True
    )
    codigo = Column("codigo_churrasqueira", VARCHAR, unique=True)
    modelo = Column("modelo_churrasqueira", VARCHAR)
    descricao = Column("descricao_churrasqueira", VARCHAR)
    preco_venda = Column("preco_venda_churrasqueira", DECIMAL)
    ativo = Column("ativo_churrasqueira", Boolean)

    def __init__(self, codigo, modelo, descricao, preco_venda, ativo=True):
        self.codigo = codigo
        self.modelo = modelo
        self.descricao = descricao
        self.preco_venda = preco_venda
        self.ativo = ativo

    # cadastrar() - Void
    # editar() - Void
    # pesquisar(termo) - list<Churrasqueira>


class Estoque(Base):
    __tablename__ = "Estoque"

    id_estoque = Column("id_estoque", Integer, primary_key=True, autoincrement=True)
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    quantidade_disponivel = Column("quantidade_disponivel", Integer)
    data_atualizacao = Column("data_atualizacao_estoque", DateTime)

    def __init__(self, id_churrasqueira, quantidade_disponivel, data_atualizacao):
        self.id_churrasqueira = id_churrasqueira
        self.quantidade_disponivel = quantidade_disponivel
        self.data_atualizacao = data_atualizacao

    # obterSaldo() - Int
    # atualizarQuantidade() - void
    # verificarDisponibilidade(qtd) - boolean


# ARRUMAR NO DIAGRAMA DE CLASSE, CRIANDO A CLASSE CANCELAMENTO (QUE ESTARÁ A SEGUIR)
class Cancelamento(Base):
    __tablename__ = "Cancelamento_de_alguma_coisa"

    id_cancelamento = Column("id_cancelamento", Integer, primary_key=True, autoincrement=True)
    cancelado = Column("cancelamento", Boolean)
    data_cancelamento = Column("data_cancelamento", DateTime)
    motivo_cancelamento = Column("motivo_cancelamento", VARCHAR)

    def __init__(self, cancelado, data_cancelamento, motivo_cancelamento):
        self.cancelado = cancelado
        self.data_cancelamento = data_cancelamento
        self.motivo_cancelamento = motivo_cancelamento

    # cancelar(motivo) - Void


# ARRUMAR NO DIAGRAMA DE CLASSE, CRIANDO A CLASSE CANCELAMENTO (QUE ESTARÁ A SEGUIR)
class Abastecimento(Base):
    __tablename__ = "Abastecimento Estoque"

    id_abastecimento = Column("id_abastecimento", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    data_abastecimento = Column("data_abastecimento", DateTime)
    observacoes = Column("observacoes_abastecimento", VARCHAR)
    cancelado = Column("cancelamento_abastecimento", Boolean, ForeignKey("Cancelamento.cancelado"))

    def __init__(self, id_abastecimento, id_usuario, data_abastecimento, observacoes, cancelado):
        self.id_abastecimento = id_abastecimento
        self.id_usuario = id_usuario
        self.data_abastecimento = data_abastecimento
        self.observacoes = observacoes
        self.cancelado = cancelado

    # cadastrar() - Void
    # listar(filtros) - list<abastecimentos>

class Item_abastecimento(Base):
    __tablename__ = "qual_item_abastecimento"

    id_item_abastecimento = Column("id_item_abastecimento", Integer, primary_key=True, autoincrement=True)
    id_abastecimento = Column("id_abastecimento", Integer, ForeignKey("Abastecimento.id_abastecimento"))
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    quantidade = Column("quantidade_abastecimento", Integer)

    def __init__(self, id_abastecimento, id_churrasqueira, quantidade):
        self.id_abastecimento = id_abastecimento
        self.id_churrasqueira = id_churrasqueira
        self.quantidade = quantidade

    # adicionarItem() - void
    # removerItem() - void

class Movimentacao_estoque(Base):
    __tablename__ = "movimentacao_de_estoque"

    id_movimentacao = Column("id_movimentacao", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    data_hora = Column("datahora_movimentacao_estoque", DateTime)
    tipo_movimentacao = Column("tipo_movimentacao", Enum("entrada", "saida", name="tipo_movimentacao"))
    origem = Column("origem_movimentacao", Enum("abastecimento", "venda", "cancelamento_venda", "ajuste_manual", name="origem_movimentacao"))
    quantidade = Column("quantidade_movimentacao", Integer)
    saldo_anterior = Column("saldo_anterior", Integer)
    saldo_posterior = Column("saldo_posterior", Integer)
    observacoes = Column("observacoes_movimentacao", VARCHAR)

    def __init__(self, id_usuario, id_churrasqueira, data_hora, tipo_movimentacao, origem, quantidade, saldo_anterior, saldo_posterior, observacoes):
        self.id_usuario = id_usuario
        self.id_churrasqueira = id_churrasqueira
        self.data_hora = data_hora
        self.tipo_movimentacao = tipo_movimentacao
        self.origem = origem
        self.quantidade = quantidade
        self.saldo_anterior = saldo_anterior
        self.saldo_posterior = saldo_posterior
        self.observacoes = observacoes

    # registrar() - Void
    # listar(filtros) - list<Movimentacao_estoque>

    # O que fazer com o tipo_movimentacao (ENUM) (Entrada e saída)
    # O que fazer com a origem (ENUM) (Abastecimento, venda, cancelamento_venda, ajuste_manual)

class Cliente(Base):
    __tablename__ = "Clientes"

    id_cliente = Column("id_cliente", Integer, primary_key=True, autoincrement=True)
    tipo = Column("tipo_cliente", Enum("fisica", "juridica", name="tipo_cliente"))
    nome = Column("nome_cliente", VARCHAR)
    cpf_cnjp = Column("cpf_cnpj_cliente", VARCHAR)
    telefone = Column("telefone_cliente", VARCHAR)
    email = Column("email_cliente", VARCHAR)
    endereco = Column("endereco_cliente", VARCHAR)
    cidade = Column("cidade_cliente", VARCHAR)
    estado = Column("estado_cliente", VARCHAR)
    cep = Column("cep_cliente", VARCHAR)
    ativo = Column("ativo_cliente", Boolean)
    data_cadastro = Column("data_cadastro_cliente", DateTime)

    def __init__(self, tipo, nome, cpf_cnpj, telefone, email, endereco, cidade, estado, cep, data_cadastro, ativo=True):
        self.tipo = tipo
        self.nome = nome
        self.cpf_cnpj = cpf_cnpj
        self.telefone = telefone
        self.email = email
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.ativo = ativo
        self.data_cadastro = data_cadastro

    # cadastrar() - Void
    # editar() - Void
    # desativar() - Void

class Loja(Base):
    __tablename__ = "Lojas"

    id_loja = Column("id_loja", Integer, primary_key=True, autoincrement=True)
    id_cliente = Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente"), unique=True)
    razao_social = Column("razao_social_loja", VARCHAR)
    inscricao_estadual = Column("inscricao_estadual_loja", VARCHAR)

    def __init__(self, id_cliente, razao_social, inscricao_estadual):
        self.id_cliente = id_cliente
        self.razao_social = razao_social
        self.inscricao_estadual = inscricao_estadual

    # obterDadosLoja() - Loja

class Consumidor_Final(Base):
    __tablename__ = "Consumidor_Final"

    id_consumidor = Column("id_consumidor", Integer, primary_key=True, autoincrement=True)
    id_cliente = Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente"))
    data_nascimento = Column("data_nascimento_consumidor", Date)
    observacoes = Column("observacoes_consumidor", VARCHAR)

    def __init__(self, id_cliente, data_nascimento, observacoes):
        self.id_cliente = id_cliente
        self.data_nascimento = data_nascimento
        self.observacoes = observacoes
    
    # obterDadosConsumidor() - Consumidor_Final

class Venda(Base):
    __tablename__ = "Vendas"

    id_venda = Column("id_venda", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    id_cliente = Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente"))
    forma_pagamento = Column("nome_forma_pagamento", VARCHAR, ForeignKey("Forma_pagamento.nome_forma_pagamento"))
    data_venda = Column("data_venda", DateTime)
    valor_total = Column("valor_total_venda", DECIMAL)
    observacoes = Column("observacoes_venda", VARCHAR)
    status = Column("status_venda", Enum("concluida", "cancelada", "pendente", name="status_venda"))

    def __init__(self, id_usuario, id_cliente, data_venda, forma_pagamento, valor_total, observacoes, status):
        self.id_usuario = id_usuario
        self.id_cliente = id_cliente
        self.data_venda = data_venda
        self.forma_pagamento = forma_pagamento
        self.valor_total = valor_total
        self.observacoes = observacoes
        self.status = status

    # registrar() - Void
    # consultar(filtros) - list<Venda>

class Item_venda(Base):
    __tablename__ = "Item_da_venda"

    id_item_venda = Column("id_item_venda", Integer, primary_key=True, autoincrement=True)
    id_venda = Column("id_venda", Integer, ForeignKey("Vendas.id_venda"))
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    quantidade = Column("quantidade_item_venda", Integer)
    preco_unitario = Column("preco_unitario_item_venda", DECIMAL)
    subtotal = Column("subtotal_item_venda", DECIMAL)

    def __init__(self, id_venda, id_churrasqueira, quantidade, preco_unitario, subtotal):
        self.id_venda = id_venda
        self.id_churrasqueira = id_churrasqueira
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = subtotal

    #CalcularSubTotal() - DECIMAL

class Forma_pagamento(Base):
    __tablename__ = "Forma_pagamento"

    id_forma_pagamento = Column("id_forma_pagamento", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome_forma_pagamento", VARCHAR, unique=True)
    ativo = Column("ativo_forma_pagamento", Boolean)

    def __init__(self, id_forma_pagamento, nome, ativo):
        self.id_forma_pagamento = id_forma_pagamento
        self.nome = nome
        self.ativo = ativo

    # cadastrar() - Void
    # editar() - Void
    # listarAtivos(): List<FormaPagamento>

class Relatorio(Base):
    __tablename__ = "Relatorios"

    id_relatorio = Column("id_relatorio", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    tipo_relatorio = Column("tipo_relatorio", Enum("vendas", "abastecimentos", "estoque", "movimentacoes", "desempenho"))
    filtros_aplicados = Column("filtros_aplicados_relatorios", JSON)
    data_geracao = Column("data_relatorio", DateTime)

    def __init__(self, id_usuario, tipo_relatorio, filtros_aplicados, data_geracao):
        self.id_usuario = id_usuario
        self.tipo_relatorio = tipo_relatorio
        self.filtros_aplicados = filtros_aplicados
        self.data_geracao = data_geracao

    # gerar() - Void
    # exportarPDF() - File
    # exportarExcel() - File



Base.metadata.create_all(bind=database)

# ====================CRIAR INSTÂNCIA DA TABELA=====================


# ====================== READ =======================


# ====================== UPDATE =======================


# ====================== DELETE =======================
