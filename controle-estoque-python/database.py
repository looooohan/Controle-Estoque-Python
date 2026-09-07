import mysql.connector
from mysql.connector import Error
from produto import Produto


class Database:
    """
    Responsável por toda a comunicação com o banco de dados MySQL:
    conexão, criação da tabela e operações de CRUD.
    """

    def __init__(self, host="localhost", user="root", password="", database="controle_estoque"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexao = None

    def conectar(self):
        """Abre a conexão com o MySQL e garante que o banco/tabela existam."""
        try:
            # Primeiro conecta sem especificar o banco, pra poder criá-lo se não existir
            conexao_inicial = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conexao_inicial.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            conexao_inicial.close()

            # Agora conecta já no banco correto
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            self._criar_tabela()
            print("Conectado ao banco de dados com sucesso.\n")
            return True

        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return False

    def _criar_tabela(self):
        """Cria a tabela de produtos caso ela ainda não exista."""
        query = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            quantidade INT NOT NULL DEFAULT 0,
            preco DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
            categoria VARCHAR(50)
        )
        """
        cursor = self.conexao.cursor()
        cursor.execute(query)
        cursor.close()

    def fechar(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()

    # ---------- CRUD ----------

    def cadastrar_produto(self, produto: Produto):
        query = """
            INSERT INTO produtos (nome, quantidade, preco, categoria)
            VALUES (%s, %s, %s, %s)
        """
        valores = (produto.nome, produto.quantidade, produto.preco, produto.categoria)
        cursor = self.conexao.cursor()
        cursor.execute(query, valores)
        self.conexao.commit()
        cursor.close()
        print(f"Produto '{produto.nome}' cadastrado com sucesso!\n")

    def listar_produtos(self):
        query = "SELECT id, nome, quantidade, preco, categoria FROM produtos ORDER BY id"
        cursor = self.conexao.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()

        produtos = []
        for linha in resultados:
            produtos.append(Produto(id=linha[0], nome=linha[1], quantidade=linha[2],
                                     preco=float(linha[3]), categoria=linha[4]))
        return produtos

    def buscar_produto_por_id(self, id_produto):
        query = "SELECT id, nome, quantidade, preco, categoria FROM produtos WHERE id = %s"
        cursor = self.conexao.cursor()
        cursor.execute(query, (id_produto,))
        linha = cursor.fetchone()
        cursor.close()

        if linha:
            return Produto(id=linha[0], nome=linha[1], quantidade=linha[2],
                            preco=float(linha[3]), categoria=linha[4])
        return None

    def atualizar_produto(self, id_produto, nome=None, quantidade=None, preco=None, categoria=None):
        campos = []
        valores = []

        if nome is not None:
            campos.append("nome = %s")
            valores.append(nome)
        if quantidade is not None:
            campos.append("quantidade = %s")
            valores.append(quantidade)
        if preco is not None:
            campos.append("preco = %s")
            valores.append(preco)
        if categoria is not None:
            campos.append("categoria = %s")
            valores.append(categoria)

        if not campos:
            print("Nenhum dado para atualizar.\n")
            return

        valores.append(id_produto)
        query = f"UPDATE produtos SET {', '.join(campos)} WHERE id = %s"

        cursor = self.conexao.cursor()
        cursor.execute(query, tuple(valores))
        self.conexao.commit()
        linhas_afetadas = cursor.rowcount
        cursor.close()

        if linhas_afetadas:
            print(f"Produto ID {id_produto} atualizado com sucesso!\n")
        else:
            print(f"Nenhum produto encontrado com ID {id_produto}.\n")

    def remover_produto(self, id_produto):
        query = "DELETE FROM produtos WHERE id = %s"
        cursor = self.conexao.cursor()
        cursor.execute(query, (id_produto,))
        self.conexao.commit()
        linhas_afetadas = cursor.rowcount
        cursor.close()

        if linhas_afetadas:
            print(f"Produto ID {id_produto} removido com sucesso!\n")
        else:
            print(f"Nenhum produto encontrado com ID {id_produto}.\n")

    # ---------- Relatórios / queries mais elaboradas ----------

    def produtos_estoque_baixo(self, limite=10):
        query = "SELECT id, nome, quantidade, preco, categoria FROM produtos WHERE quantidade < %s ORDER BY quantidade"
        cursor = self.conexao.cursor()
        cursor.execute(query, (limite,))
        resultados = cursor.fetchall()
        cursor.close()

        return [Produto(id=l[0], nome=l[1], quantidade=l[2], preco=float(l[3]), categoria=l[4])
                for l in resultados]

    def valor_total_em_estoque(self):
        query = "SELECT SUM(quantidade * preco) FROM produtos"
        cursor = self.conexao.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()[0]
        cursor.close()
        return float(resultado) if resultado else 0.0

    def produtos_por_categoria(self):
        query = """
            SELECT categoria, COUNT(*), SUM(quantidade)
            FROM produtos
            GROUP BY categoria
        """
        cursor = self.conexao.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        return resultados  # lista de tuplas (categoria, total_produtos, total_quantidade)
