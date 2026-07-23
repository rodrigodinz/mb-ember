from database import Session
from database import(
    Usuario,
    Forma_pagamento,
    Churrasqueira,
    Estoque
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
        modelo="Inox 01",
        descricao="Churrasqueira Inox Mundial 01",
        preco_venda=200.00
    )

    session.add(teste_churrasqueira)
    session.flush()

    teste_estoque = Estoque(
        id_churrasqueira=teste_churrasqueira.id_churrasqueira,
        quantidade_disponivel=20,
    )

    session.add(teste_estoque)
    session.commit()



