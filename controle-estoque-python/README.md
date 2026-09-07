# Controle de Estoque

Sistema em Python para gerenciamento de estoque de produtos, com persistência 
em banco de dados MySQL. Permite cadastrar, listar, atualizar e remover 
produtos, além de gerar relatórios simples direto do banco de dados.

## Funcionalidades

- Cadastro, listagem, atualização e remoção de produtos (CRUD completo)
- Criação automática do banco de dados e da tabela na primeira execução
- Relatório de produtos com estoque baixo
- Relatório de valor total em estoque
- Relatório de produtos agrupados por categoria
- Validação básica de dados de entrada

## Conceitos aplicados

- **Conexão com banco de dados relacional (MySQL)** usando `mysql-connector-python`
- **SQL**: `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, além de 
  queries com `WHERE`, `SUM`, `GROUP BY` e `ORDER BY`
- **Organização em camadas**: separação entre modelo de dados (`Produto`), 
  acesso ao banco (`Database`) e interface com o usuário (`main.py`)
- **Tratamento de erros** na conexão com o banco e na entrada de dados do usuário

## Tecnologias

- Python 3
- MySQL
- Biblioteca `mysql-connector-python`

## Como executar

1. Clone o repositório:
   ```
   git clone https://github.com/seuusuario/controle-estoque-python.git
   cd controle-estoque-python
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Configure o MySQL:
   - Tenha um servidor MySQL rodando localmente (ex: via XAMPP, MySQL Server ou Docker)
   - Ajuste usuário e senha em `main.py`, na linha:
     ```python
     db = Database(host="localhost", user="root", password="", database="controle_estoque")
     ```
   - O banco de dados e a tabela são criados automaticamente na primeira execução

4. Execute o programa:
   ```
   python main.py
   ```
