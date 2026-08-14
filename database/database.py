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

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base

from datetime import datetime

database = create_engine("sqlite:///database/database.db")

Session = sessionmaker(bind=database)

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
    ativo = Column("ativo_usuario", Boolean, default=True)
    data_cadastro = Column("data_cadastro_usuario", DateTime)

    rel_log_acesso = relationship("Log_Acesso", back_populates="rel_usuario")
    rel_mov_estoque = relationship("Movimentacao_estoque", back_populates="rel_usuario")
    rel_venda = relationship("Venda", back_populates="rel_usuario")
    rel_relatorio = relationship("Relatorio", back_populates="rel_usuario")
    rel_abastecimento = relationship("Abastecimento", back_populates="rel_usuario")

    # autenticar(email, senha) - boolean
    # alterarSenha(novaSenha) - Void
    # obterMeusDados () - Usuario

class Log_Acesso(Base):
    __tablename__ = "Log de acesso"

    id_log_acesso = Column("id_acesso", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    data_hora = Column("datahora_log", DateTime)
    ip = Column("ip_log", VARCHAR)
    sucesso = Column("sucesso_log", Boolean, default=True)

    rel_usuario = relationship("Usuario", back_populates="rel_log_acesso")

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
    ativo = Column("ativo_churrasqueira", Boolean, default=True)

    # cadastrar() - Void
    # editar() - Void
    # pesquisar(termo) - list<Churrasqueira>

    rel_estoque = relationship("Estoque", back_populates="rel_churrasqueira", uselist=False)

    rel_mov_estoque = relationship("Movimentacao_estoque", back_populates="rel_churrasqueira")

    rel_item_venda = relationship("Item_venda", back_populates="rel_churrasqueira")

    rel_item_abastecimento = relationship("Item_abastecimento", back_populates="rel_churrasqueira")

class Estoque(Base):
    __tablename__ = "Estoque"

    id_estoque = Column("id_estoque", Integer, primary_key=True, autoincrement=True)
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"), unique=True)
    quantidade_disponivel = Column("quantidade_disponivel", Integer)
    data_atualizacao = Column("data_atualizacao_estoque", DateTime, default=datetime.now, onupdate=datetime.now)

    # obterSaldo() - Int
    # atualizarQuantidade() - void
    # verificarDisponibilidade(qtd) - boolean

    rel_churrasqueira = relationship("Churrasqueira", back_populates="rel_estoque")

class Abastecimento(Base):
    __tablename__ = "Abastecimento_Estoque"

    id_abastecimento = Column("id_abastecimento", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    data_abastecimento = Column("data_abastecimento", DateTime)
    observacoes = Column("observacoes_abastecimento", VARCHAR)
    cancelado = Column("cancelamento_abastecimento", Boolean)
    data_cancelamento = Column("data_cancelamento", DateTime)
    motivo_cancelamento = Column("motivo_cancelamento", VARCHAR)

    rel_item_abastecimento = relationship("Item_abastecimento", back_populates="rel_abastecimento")
    rel_usuario = relationship("Usuario", back_populates="rel_abastecimento")

    # cadastrar() - Void
    # cancelar(motivo) - Void
    # listar(filtros) - list<abastecimentos>

class Item_abastecimento(Base):
    __tablename__ = "Item_Abastecimento"

    id_item_abastecimento = Column("id_item_abastecimento", Integer, primary_key=True, autoincrement=True)
    id_abastecimento = Column("id_abastecimento", Integer, ForeignKey("Abastecimento_Estoque.id_abastecimento"))
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    quantidade = Column("quantidade_abastecimento", Integer)

    rel_abastecimento = relationship("Abastecimento", back_populates="rel_item_abastecimento")
    rel_churrasqueira = relationship("Churrasqueira", back_populates="rel_item_abastecimento")

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

    # registrar() - Void
    # listar(filtros) - list<Movimentacao_estoque>

    rel_churrasqueira = relationship("Churrasqueira", back_populates="rel_mov_estoque")
    rel_usuario = relationship("Usuario", back_populates="rel_mov_estoque")

    # O que fazer com o tipo_movimentacao (ENUM) (Entrada e saída)
    # O que fazer com a origem (ENUM) (Abastecimento, venda, cancelamento_venda, ajuste_manual)

class Cliente(Base):
    __tablename__ = "Clientes"

    id_cliente = Column("id_cliente", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome_cliente", VARCHAR)
    cpf_cnpj = Column("cpf_cnpj_cliente", VARCHAR)
    telefone = Column("telefone_cliente", VARCHAR)
    email = Column("email_cliente", VARCHAR)
    endereco = Column("endereco_cliente", VARCHAR)
    cidade = Column("cidade_cliente", VARCHAR)
    estado = Column("estado_cliente", VARCHAR)
    cep = Column("cep_cliente", VARCHAR)
    ativo = Column("ativo_cliente", Boolean, default=True)
    data_cadastro = Column("data_cadastro_cliente", DateTime)
    tipo_cliente = Column("tipo_cliente", String)

    __mapper_args__ = {
        "polymorphic_on": tipo_cliente,
        "polymorphic_identity": "cliente"
    }

    rel_venda = relationship("Venda", back_populates="rel_cliente")

    # cadastrar() - Void
    # editar() - Void
    # desativar() - Void

class Loja(Cliente):
    __tablename__ = "Lojas"

    id_cliente = Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente"), unique=True, primary_key=True)
    razao_social = Column("razao_social_loja", VARCHAR)
    inscricao_estadual = Column("inscricao_estadual_loja", VARCHAR)

    __mapper_args__ = {
        "polymorphic_identity": "loja"
    }

    # obterDadosLoja() - Loja

class Consumidor_Final(Cliente):
    __tablename__ = "Consumidor_Final"

    id_cliente = Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente"), unique=True, primary_key=True)
    data_nascimento = Column("data_nascimento_consumidor", Date)
    observacoes = Column("observacoes_consumidor", VARCHAR)

    __mapper_args__ = {
        "polymorphic_identity": "consumidor_final"
    }
    
    # obterDadosConsumidor() - Consumidor_Final

class Venda(Base):
    __tablename__ = "Vendas"

    id_venda = Column("id_venda", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", Integer, ForeignKey("Usuarios.id_usuario"))
    id_cliente = Column("id_cliente", Integer, ForeignKey("Clientes.id_cliente"))
    forma_pagamento = Column("id_forma_pagamento", Integer, ForeignKey("Forma_pagamento.id_forma_pagamento"))
    data_venda = Column("data_venda", DateTime)
    valor_total = Column("valor_total_venda", DECIMAL)
    observacoes = Column("observacoes_venda", VARCHAR)
    status = Column("status_venda", Enum("concluida", "cancelada", "pendente", name="status_venda"))
    data_cancelamento = Column("data_cancelamento_venda", DateTime)
    motivo_cancelamento = Column("motivo_cancelamento_venda", VARCHAR)

    rel_usuario = relationship("Usuario", back_populates="rel_venda")
    rel_cliente = relationship("Cliente", back_populates="rel_venda")
    rel_item_venda = relationship("Item_venda", back_populates="rel_venda", cascade="all, delete-orphan")
    rel_forma_pagamento = relationship("Forma_pagamento", back_populates="rel_venda")

    # registrar() - Void
    # cancelar() - Void
    # consultar(filtros) - list<Venda>

class Item_venda(Base):
    __tablename__ = "Item_da_venda"

    id_item_venda = Column("id_item_venda", Integer, primary_key=True, autoincrement=True)
    id_venda = Column("id_venda", Integer, ForeignKey("Vendas.id_venda"))
    id_churrasqueira = Column("id_churrasqueira", Integer, ForeignKey("Churrasqueira.id_churrasqueira"))
    quantidade = Column("quantidade_item_venda", Integer)
    preco_unitario = Column("preco_unitario_item_venda", DECIMAL)
    subtotal = Column("subtotal_item_venda", DECIMAL)

    rel_venda = relationship("Venda", back_populates="rel_item_venda")

    rel_churrasqueira = relationship("Churrasqueira", back_populates="rel_item_venda")

    #CalcularSubTotal() - DECIMAL

class Forma_pagamento(Base):
    __tablename__ = "Forma_pagamento"

    id_forma_pagamento = Column("id_forma_pagamento", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome_forma_pagamento", VARCHAR, unique=True)
    ativo = Column("ativo_forma_pagamento", Boolean, default=True)

    rel_venda = relationship("Venda", back_populates="rel_forma_pagamento")

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

    rel_usuario = relationship("Usuario", back_populates="rel_relatorio")

    # gerar() - Void
    # exportarPDF() - File
    # exportarExcel() - File



Base.metadata.create_all(database)

# ====================CRIAR INSTÂNCIA DA TABELA=====================


# ====================== READ =======================


# ====================== UPDATE =======================


# ====================== DELETE =======================