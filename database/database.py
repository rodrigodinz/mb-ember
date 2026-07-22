from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    PrimaryKeyConstraint,
    VARCHAR,
    DateTime,
    Date,
    Enum,
    DECIMAL,
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

database = create_engine("sqlite:///banco_dados.db")

Session = sessionmaker(database)
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
    id_churrasqueira = Column(
        "id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira")
    )
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
""" class Cancelamento(Base):
    __tablename__ = "Cancelamento de alguma coisa"

    cancelado = Column("cancelamento", Boolean)
    data_cancelamento = Column("data_cancelamento", DateTime)
    motivo_cancelamento = Column("motivo_cancelamento", VARCHAR)

    def __init__(self, cancelado, data_cancelamento, motivo_cancelamento):
        self.cancelado = cancelado
        self.data_cancelamento = data_cancelamento
        self.motivo_cancelamento = motivo_cancelamento

    # cancelar(motivo) - Void """


# ARRUMAR NO DIAGRAMA DE CLASSE, CRIANDO A CLASSE CANCELAMENTO (QUE ESTARÁ A SEGUIR)
class Abastecimento(Base):
    __tablename__ = "Abastecimento Estoque"

    id_abastecimento = Column(
        "id_abastecimento", Integer, primary_key=True, autoincrement=True
    )
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    data_abastecimento = Column("data_abastecimento", DateTime)
    observacoes = Column("observacoes_abastecimento", VARCHAR)
    cancelado = Column(
        "cancelamento_abastecimento", Boolean, ForeignKey("Cancelamento.cancelado")
    )

    def __init__(self, id_abastecimento, data_abastecimento, observacoes):
        self.id_abastecimento = id_abastecimento
        self.data_abastecimento = data_abastecimento
        self.observacoes = observacoes

    # cadastrar() - Void
    # listar(filtros) - list<abastecimentos>

class Item_abastecimento(Base):
    __tablename__ = "qual_item_abastecimento"

    id_item_abastecimento = Column("id_item_abastecimento", Integer, primary_key=True, autoincrement=True)
    id_abastecimento = Column("id_abastecimento", Integer, ForeignKey("Abastecimento.id_abastecimento"))
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    quantidade = Column("quantidade_abastecimento", Integer)

    def __init__(self, quantidade):
        self.quantidade = quantidade

    # adicionarItem() - void
    # removerItem() - void

class Movimentacao_estoque(Base):
    __tablename__ = "movimentacao_de_estoque"

    id_movimentacao = Column("id_movimentacao", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuario.id_usuario"))
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    data_hora = Column("datahora_movimentacao_estoque", DateTime)
    tipo_movimentacao = Column("tipo_movimentacao", Enum("entrada", "saida", name="tipo_movimentacao"))
    origem = Column("origem_movimentacao", Enum("abastecimento", "venda", "devolucao", name="origem_movimentacao"))
    quantidade = Column("quantidade_movimentacao", Integer)
    saldo_anterior = Column("saldo_anterior", Integer)
    saldo_posterior = Column("saldo_posterior", Integer)
    observacoes = Column("observacoes_movimentacao", VARCHAR)

    def __init__(self, data_hora, tipo_movimentacao, origem, quantidade, saldo_anterior, saldo_posterior, observacoes):
        self.data_hora = data_hora
        self.tipo_movimentacao = tipo_movimentacao
        self.origem = origem
        self.quantidade = quantidade
        self.saldo_anterior = saldo_anterior
        self.saldo_posterior = saldo_posterior
        self.observacoes = observacoes



# ====================CRIAR INSTÂNCIA DA TABELA=====================


# ====================== READ =======================


# ====================== UPDATE =======================


# ====================== DELETE =======================
