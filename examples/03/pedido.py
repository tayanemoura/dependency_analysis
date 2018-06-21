
class Pedido: 
    def __init__(self, vendedor, itemPedido, cliente):
        #self.dataPedido = dataPedido
        self.vendedor = vendedor
        self.status = "criado"
        self.itemPedido = itemPedido
        self.cliente = cliente

    def encerrarPedido(self):
        self.status = "encerrado"

    def cancelarPedido(self):
        self.status = "cancelado"

    def adicionaItem(self, produto, item):
        item.addProduto(produto)


		
class ItemPedido:

    def __init__(self, preco):
        self.produto = None
        self.quantidade = 0
        self.preco = 0.0

    def addProduto(self, produto):
        self.produto = produto

    def incluirItem(self):
        self.quantidade += 1

    def excluirItem(self):
        if(self.quantidade != 0):
            self.quantidade -= 1
        else:
            print("Nao ha mais produtos para serem excluidos")

    def getQtd(self):
        return self.quantidade

class Pessoa:
    def __init__(self,nome, cpf):
        self.nome = nome
        self.cpf = cpf

    def getNome(self):
        return self.nome

		
class Cliente:

    def __init__(self, limiteCredito, status, pessoa):
        self.limiteCredito = limiteCredito
        self.status = status
        self.pessoa = pessoa

    def getCredito(self):
        return self.limiteCredito

    def consultaCliente(self):
        print("Cliente: " + self.pessoa.getNome() + " status:" + self.status + " limite " + str(self.limiteCredito))
       

class Produto:
    def __init__(self,nomeProduto, peso, qtdDisponivel):
        self.nomeProduto = nomeProduto
        self.peso = peso
        self.qtdDisponivel = qtdDisponivel

    def consultarProduto(self):
        print("Produto: " + self.nomeProduto + " peso:" +str(self.peso) + " qtd: "+str(self.qtdDisponivel))

    def getQtdDisponivel(self):
        return self.qtdDisponivel

    def addProduto(self):
        self.qtdDisponivel += 1



pessoa1 = Pessoa('Ana', '76569')
cliente1 = Cliente(1000.0, 'ativo', pessoa1)
cliente1.consultaCliente()
produto01 = Produto('quadro', '2', 10)
produto01.consultarProduto()
item01 = ItemPedido(400.0)
item01.incluirItem()
pedido01 = Pedido( 'Carlos', item01, cliente1)
pedido01.adicionaItem(produto01, item01)


	
