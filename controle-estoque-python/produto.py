class Produto:
    """
    Representa um produto do estoque.
    Guarda os dados básicos e sabe calcular seu próprio valor total em estoque.
    """

    def __init__(self, id=None, nome="", quantidade=0, preco=0.0, categoria=""):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.categoria = categoria

    def valor_total(self):
        """Retorna o valor total desse produto em estoque (quantidade * preço)."""
        return self.quantidade * self.preco

    def __str__(self):
        return (f"[{self.id}] {self.nome} | Categoria: {self.categoria} | "
                f"Qtd: {self.quantidade} | Preço: R${self.preco:.2f} | "
                f"Total: R${self.valor_total():.2f}")
