from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, ForeignKey, PrimaryKeyConstraint, Boolean
# Serve para criar o banco de dados, porém de forma vazia

from sqlalchemy.orm import sessionmaker
# No sqlalchemy, nos criamos as tabelas e informações do banco de dados através de sessões
# Nós criamos e estruturamos as sessões, depois commitamos ela para ser salva dentro do banco de dados

from sqlalchemy.orm import declarative_base
# Serve para criar as tabelas do banco de dados

db = create_engine("sqlite:///banco_dados_treino.db")
#Cria o banco de dados
# db é a variável que será criada o banco de dados
# Create engine é o nome da função sqlalchemy que cria um banco de dados

Session = sessionmaker(bind=db) #Cria o objeto Sessão dentro do banco de dados - representado pela variável db
session = Session() #Vincula o objetico sessão criado a uma variável chamada session, que será utilizada para manipular o banco de dados


Base = declarative_base() #A base é utilizada como um campo onde todas as tabelas são criadas
# É uma classe de base, onde todas as tabelas serão como classes filhas dessa classe base

# ================ NESSA ÁREA NÓS CRIAMOS AS TABELAS DO BANCO DE DADOS ================

class Usuario(Base): #Cria a tabela usuário, que é uma classe filha da classe Base
    __tablename__ = "Usuarios" #Nome da tabela

    id = Column("id", Integer, primary_key=True, autoincrement=True) #Cria a coluna id, que é do tipo inteiro, é a chave primária da tabela e é auto incrementável
    nome = Column("nome_usuario", String(50))
    email = Column("email_usuario", String(100))
    senha = Column("senha_usuario", String(20))
    ativo = Column("ativo_usuario", Boolean)
# Para criar as colunas da tabela, você coloca que aquela coisa vai ser uma coluna (Column)
# Na coluna você coloca seu nome, seu tipo e suas características caso necessário (unique, not null, etc)
    def __init__(self, nome, email, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

class Livro(Base):
    __tablename__ = "Livros"

    id = Column("id_livro", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo_livro", String(50))
    qtde_paginas = Column("qtde_paginas_livro", Integer)
    dono = Column("dono_livro", String(50), ForeignKey("Usuarios.id"))
    #ForeignKey é utilizado para criar uma chave estrangeira, que é uma coluna que referencia outra tabela

    def __init__(self, titulo, qtde_paginas, dono):
        self.titulo = titulo
        self.qtde_paginas = qtde_paginas
        self.dono = dono


Base.metadata.create_all(bind=db) #Cria todas as tabelas do banco de dados, que são representadas pelas classes filhas da classe Base


# CRUD (Create, read, update and delete)

#=======CRIAR DADOS - CREATE=======

usuario_rodrigo = Usuario(nome="Rodrigo", email="rodrigo_teste@gmail.com", senha="123456") #Cria um usuário teste
session.add(usuario_rodrigo)
session.commit() #Salva o usuário teste no banco de dados
# No sqlalchemy, nós utilizamos dados em tempo real assim como no git, mas esses dados não são salvos no banco de dados até que seja feito o commit, que é o ato de salvar os dados no banco de dados
# Então tudo que for criado será criado na estrutura Session criada anteriormente, e quando você quiser salvar aquele dado dentro do db, aí sim você faz session.add (como git add) e depois session.commit (como git commit)

livro_senhor_dos_aneis = Livro(titulo="Senhor dos anéis", qtde_paginas=550, dono=usuario_rodrigo.id) #Cria uma instância da classe livro
session.add(livro_senhor_dos_aneis)
session.commit() #Salva o livro no banco de dados

#=======LER DADOS - READ=======

lista_usuarios = session.query(Usuario).all()
# Faz uma query/busca de todos os usuários cadastrados na tabela do banco de dados, e retorna uma lista com todos os usuários cadastrados

usuario_rodrigo = session.query(Usuario).filter_by(email="rodrigo_teste@gmail.com").first()

#=======ATUALIZAR DADOS - UPDATE=======

usuario_rodrigo.nome = "Rodrigo Sotero"
session.add(usuario_rodrigo)
session.commit()
# Você basicamente entra na caracteristica que quer atualizar através da variável que você vinculou àquela instância da tabela e altera a informação que quiser
# Nunca esquecendo que após cada alteração, você precisará fazer um session add e um session commit para atualizar o db, tirar da session e salvar no banco de dados

#=======DELETAR DADOS - DELETE=======

session.delete(usuario_rodrigo)
session.commit()