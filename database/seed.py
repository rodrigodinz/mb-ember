import datetime

from database import Session
from database import(
    Usuario,
    Forma_pagamento,
    Churrasqueira,
    Estoque,
    Venda,
    Item_venda,
    Consumidor_Final
)

with Session() as session:

    teste_usuario = Usuario(
        nome="Rodrigo",
        email="rodrigo_diniz@gmail.com",
        senha_hash ="123456",
        perfil="vendedor",
    )

    session.add(teste_usuario)

    formas_pagamento = [
        Forma_pagamento(nome="debito"),
        Forma_pagamento(nome="credito"),
        Forma_pagamento(nome="pix"),
        Forma_pagamento(nome="dinheiro")
    ]

    session.add_all(formas_pagamento)

    teste_churrasqueira = Churrasqueira(
        codigo="CHIN01",
        modelo="Mundial Básica",
        descricao="Churrasqueira Inox Mundial Básica",
        preco_venda=200.00
    )

    session.add(teste_churrasqueira)
    session.flush()

    teste_estoque = Estoque(
        rel_churrasqueira=teste_churrasqueira,
        quantidade_disponivel=10,
    )

    session.add(teste_estoque)

    ##--------------------------------- PÓS RELATIONSHIP ---------------------------------##

    nova_churrasqueira = [
        Churrasqueira(
            codigo="CHIN02",
            modelo="Mundial Luxo",
            descricao="Churrasqueira Inox Mundial de luxo",
            preco_venda=250.00
            ),
        Churrasqueira( 
            codigo="CHIN03",
            modelo="Mundial Premium",
            descricao="Churrasqueira Inox Mundial Premium",
            preco_venda=300.00
        ),
        Churrasqueira(
            codigo="CHIN04",
            modelo="Mundial Master",
            descricao="Churrasqueira Inox Mundial Master",
            preco_venda=350.00
        )
    ]

    session.add_all(nova_churrasqueira)

    cliente_teste = Consumidor_Final(
        nome="Rodrigo Teste",
        cpf_cnpj="123.456.789-00",
        telefone="(11) 94444-4464",
        email="email_teste@gmail.com",
        endereco="Rua Teste, 123",
        cidade="Cidade Teste",
        estado="ET",
        cep="12345-678",
        data_cadastro=datetime.datetime.now(),
        data_nascimento=datetime.datetime.now().date(),
        observacoes="Cliente de teste para vendas",
    )

    churras_inox_basica = teste_churrasqueira

    churras_inox_luxo = nova_churrasqueira[0]

    venda_atual = Venda(
        data_venda=datetime.datetime.now(),
        valor_total=churras_inox_basica.preco_venda + churras_inox_luxo.preco_venda,
        status="concluida",
        rel_forma_pagamento=formas_pagamento[0],
        rel_usuario=teste_usuario,
        rel_cliente=cliente_teste,
        rel_item_venda=[
            Item_venda(
                rel_churrasqueira=churras_inox_basica,
                quantidade=1,
                preco_unitario=churras_inox_basica.preco_venda,
                subtotal=churras_inox_basica.preco_venda,


            ),
            Item_venda(
                rel_churrasqueira=churras_inox_luxo,
                quantidade=1,
                preco_unitario=churras_inox_luxo.preco_venda,
                subtotal=churras_inox_luxo.preco_venda,
            )
        ]
    )

    session.add(venda_atual)
    session.commit()

    venda_salva = session.query(Venda).first()
    print(f"Cliente: {venda_salva.rel_cliente.nome} \nItens comprados:")

    for item in venda_salva.rel_item_venda:
        print(f"\n{item.rel_churrasqueira.modelo} \n- Quantidade:  {item.quantidade:.2f} \n- Preço Unitário: {item.preco_unitario:.2f} \n- Subtotal: {item.subtotal:.2f}")



