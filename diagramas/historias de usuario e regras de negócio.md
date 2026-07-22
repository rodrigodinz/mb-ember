ÉPICO 01 - Autenticação

Realizar login
	Como vendedor, quero acessar o sistema por meio de login para visualizar apenas meus dados

ÉPICO 02 - Abastecimento

Registrar abastecimento
	Como vendedor, quero registrar todas as churrasqueiras retiradas na fábrica para controlar meu estoque disponível
	Critérios da HU (Informar a data, as churrasqueiras, a quantidade, as observações e atualizar automaticamente o estoque)

Consultar abastecimento
	Como vendedor, quero visualizar todos os abastecimentos realizados para acompanhar meu histórico
	Possíveis filtros seriam por período, modelo e quantidade

Cancelar abastecimento
	Como vendedor, quero cancelar um abastecimento lançado incorretamente para manter o estoque correto

ÉPICO 03 - Estoque

Consultar estoque
	Como vendedor, quero visualizar todas as churrasqueiras disponíveis para saber o que ainda tenho para vender

Pesquisar churrasqueira
	Como vendedor, quero localizar rapidamente um modelo para verificar se possui disponibilidade

Visualizar saldo do estoque
	Como vendedor, quero visualizar a quantidade de churrasqueiras por modelo, para planejar novas compras

ÉPICO 04 - Clientes

Cadastrar cliente
	Como vendedor, quero cadastrar um cliente para facilitar vendas futuras
	O cliente pode ser uma loja ou consumidor final

Consultar clientes
	Como vendedor, quero pesquisar clientes para localizar rapidamente informações

Editar cliente
	Como vendedor, quero atualizar os dados de um cliente para manter o cadastro correto

ÉPICO 05 - Registro de vendas

Registrar venda
	Como vendedor, quero registrar minhas vendas para ter controle delas
• Fluxo
	Selecionar loja ou consumidor final → Selecionar o cliente → Selecionar churrasqueiras vendidas → Informar valor, forma de pagamento e observações
	O sistema registra a data, hora, vendedor e baixa automaticamente o estoque

Consultar vendas
	Como vendedor, quero atualizar todas as vendas para acompanhar meu desempenho
	Filtros serão hoje, semana, mês, período, cliente, loja e consumidor final

Visualizar detalhes da venda
	Como vendedor, quero visualizar todos os dados de uma venda para consultar informações antigas

Cancelar venda
	Como vendedor autorizado, quero cancelar uma venda para corrigir erros

ÉPICO 06 - Dashboard

Visualizar painel inicial
	Como vendedor, quero visualizar indicadores para entender rapidamente a situação das vendas
	Indicadores serão estoque atual, churrasqueiras vendidas e restantes, faturamento e quantidade vendida

Visualizar gráfico de vendas
	Como vendedor, quero visualizar gráficos para analisar minhas vendas
	Os gráficos podem ser de vendar por mês, semana, dia, cliente, cidade e por modelos mais vendidos

Consultar histórico
	Como vendedor, quero consultar todas as minhas vendas passadas para acompanhar meu histórico

ÉPICO 07 - Relatórios

Emitir relatório
	Como vendedor, quero gerar relatórios para acompanhar minhas vendas
	Filtros podem ser semanal, mensal, anual ou período personalizado

Exportar relatório
	Como vendedor, quero exportar um relatório para imprimir ou compartilhar

==========================================================

REGRAS DE NEGÓCIO

RN01 - Todo abastecimento deve possuir uma data de registro

RN02 - Um abastecimento pode conter uma ou mais churrasqueiras

RN03 - Ao registrar um abastecimento, o estoque deve ser incrementado automaticamente

RN04 - Uma venda somente pode ocorrer se houver quantidade suficiente em estoque

RN05 - Ao concluir uma venda, o sistema deve reduzir automaticamente o estoque

RN06 - Uma venda deve ser destinada obrigatoriamente a uma loja ou ao consumidor final

RN07 - Toda venda deve registrar automaticamente a data, hora e usuário responsável

RN08 - Cada venda pode conter uma ou mais churrasqueiras

RN09 - O sistema deve impedir estoque negativo

RN10 - O sistema deve impedir venda de quantidade superior ao estoque disponível

RN11 - Clientes devem possuir um tipo: loja ou consumidor final

RN12 - Não é permitido excluir vendas concluídas, caso necessário elas apenas serão canceladas

RN13 - Ao cancelar uma venda, o estoque deve ser recomposto automaticamente

RN14 - O dashboard deve apresentar apenas dados do usuário autenticado

RN15 - Os relatórios devem permitir filtros por período

RN16 - O histórico de abastecimentos não pode ser excluído sem autorização

RN 17 - Toda movimentação de estoque deve possuir origem (Como abastecimento, venda, cancelamento de venda e ajuste manual, caso necessário)

RN18 - O usuário deve manter histórico de todas as movimentações realizadas










