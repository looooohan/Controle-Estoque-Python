from database import Database
from produto import Produto


def exibir_menu():
    print("=" * 40)
    print("       CONTROLE DE ESTOQUE")
    print("=" * 40)
    print("1. Cadastrar produto")
    print("2. Listar produtos")
    print("3. Atualizar produto")
    print("4. Remover produto")
    print("5. Relatório: produtos com estoque baixo")
    print("6. Relatório: valor total em estoque")
    print("7. Relatório: produtos por categoria")
    print("0. Sair")
    print("=" * 40)


def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Valor inválido. Digite um número (ex: 10.50).")


def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def cadastrar(db):
    print("\n--- Cadastro de novo produto ---")
    nome = input("Nome: ").strip()
    quantidade = ler_int("Quantidade: ")
    preco = ler_float("Preço (R$): ")
    categoria = input("Categoria: ").strip()

    if quantidade < 0 or preco < 0:
        print("Quantidade e preço não podem ser negativos.\n")
        return

    produto = Produto(nome=nome, quantidade=quantidade, preco=preco, categoria=categoria)
    db.cadastrar_produto(produto)


def listar(db):
    print("\n--- Lista de produtos ---")
    produtos = db.listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado.\n")
        return
    for p in produtos:
        print(p)
    print()


def atualizar(db):
    print("\n--- Atualizar produto ---")
    id_produto = ler_int("ID do produto a atualizar: ")
    produto = db.buscar_produto_por_id(id_produto)

    if not produto:
        print("Produto não encontrado.\n")
        return

    print(f"Produto atual: {produto}")
    print("Deixe em branco os campos que não quer alterar.")

    nome = input("Novo nome: ").strip()
    quantidade_str = input("Nova quantidade: ").strip()
    preco_str = input("Novo preço: ").strip()
    categoria = input("Nova categoria: ").strip()

    db.atualizar_produto(
        id_produto,
        nome=nome if nome else None,
        quantidade=int(quantidade_str) if quantidade_str else None,
        preco=float(preco_str) if preco_str else None,
        categoria=categoria if categoria else None
    )


def remover(db):
    print("\n--- Remover produto ---")
    id_produto = ler_int("ID do produto a remover: ")
    db.remover_produto(id_produto)


def estoque_baixo(db):
    print("\n--- Produtos com estoque baixo (< 10 unidades) ---")
    produtos = db.produtos_estoque_baixo(limite=10)
    if not produtos:
        print("Nenhum produto com estoque baixo.\n")
        return
    for p in produtos:
        print(p)
    print()


def valor_total(db):
    total = db.valor_total_em_estoque()
    print(f"\nValor total em estoque: R${total:.2f}\n")


def por_categoria(db):
    print("\n--- Produtos por categoria ---")
    resultados = db.produtos_por_categoria()
    if not resultados:
        print("Nenhum dado disponível.\n")
        return
    for categoria, total_produtos, total_quantidade in resultados:
        categoria_nome = categoria if categoria else "(sem categoria)"
        print(f"{categoria_nome}: {total_produtos} produto(s) cadastrado(s), "
              f"{total_quantidade} unidade(s) no total")
    print()


def main():
    db = Database(host="localhost", user="root", password="1234", database="controle_estoque")

    if not db.conectar():
        print("Não foi possível conectar ao banco. Encerrando.")
        return

    opcoes = {
        "1": cadastrar,
        "2": listar,
        "3": atualizar,
        "4": remover,
        "5": estoque_baixo,
        "6": valor_total,
        "7": por_categoria,
    }

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("Encerrando o sistema. Até mais!")
            break
        elif escolha in opcoes:
            opcoes[escolha](db)
        else:
            print("Opção inválida. Tente novamente.\n")

    db.fechar()


if __name__ == "__main__":
    main()
