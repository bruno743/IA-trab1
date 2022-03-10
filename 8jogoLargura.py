import copy
import time
import os

# pegando o estado inicial #
seq = input('Informe o problema: ')

# colocando o estado inicial no formato correto #
tabuleiro = {0:[int(seq[0]), int(seq[1]), int(seq[2])], 1:[int(seq[3]), int(seq[4]), int(seq[5])],
2:[int(seq[6]), int(seq[7]), int(seq[8])]}

#tabuleiro = {0:[1, 3, 6], 1:[4, 2, 8], 2:[0, 7, 5]}
#tabuleiro = {0:[4, 3, 6], 1:[8, 7, 1], 2:[0, 5, 2]}
#tabuleiro = {0:[2, 0, 3], 1:[1, 4, 5], 2:[7, 8, 6]}
#tabuleiro = {0:[1, 2, 3], 1:[4, 5, 6], 2:[7, 8, 0]}
tblTeste = {0:[1, 2, 3], 1:[4, 5, 6], 2:[7, 8, 0]}

''' acha a posição do zero, a peça vazia '''
def getZero(tabuleiro):
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == 0: return [i, j]

pos0 = getZero(tabuleiro)

''' realiza o movimento, trocando posições de elementos, peças '''
def movimento(tabul, pos, l, c, tree):
    tabuleiro = copy.deepcopy(tabul)
    tabuleiro[pos[0]][pos[1]] = tabuleiro[l][c]
    tabuleiro[l][c] = 0
    return tree.geraFilho([l, c], tabuleiro, tree)

''' verifica quantos movimentos são possíveis e os faz '''
def decisao(tabul, pos, tree):
    tb = copy.deepcopy(tabul)
    nivel = []
    if pos[0] > 0:
        nivel.append(movimento(tb, pos, pos[0]-1, pos[1], tree))
    if pos[0] < 2:
        nivel.append(movimento(tb, pos, pos[0]+1, pos[1], tree))

    if pos[1] > 0:
        nivel.append(movimento(tb, pos, pos[0], pos[1]-1, tree))
    if pos[1] < 2:
        nivel.append(movimento(tb, pos, pos[0], pos[1]+1, tree))

    return nivel

def busca(tree):
    if tree.chave == tblTeste:
        return [tree]

    return decisao(tree.chave, tree.pos0, tree)

''' visualização de um estado '''
def exibe(tbl):
    for i in range(3):
        print(tbl[i])
    
class NodoArvore:
    def __init__(self, pos0, chave=None, pai=None, depth = None):
        self.chave = chave
        self.pai = pai
        self.filhos = []
        self.pos0 = pos0
        if depth == None:
            self.depth = 0
        else:
            self.depth = depth + 1

    def geraFilho(self, pos0, chave, pai):
        filho = NodoArvore(pos0, chave, pai, pai.depth)
        self.filhos.append(filho)
        return filho

    def getHeu(self, h2):
        tabHeu = []
        for i in range(len(self.chave)):
            for j in range(len(self.chave[0])):
                tabHeu.append(h2[j+3*i][self.chave[i][j]])
        return sum(tabHeu)

tree = NodoArvore(pos0, tabuleiro)

flag = 1 # variável auxiliar, condição de parada
lista = [] # variável para armazenar todos os nós de um nível
lista += busca(tree)
explorados = [] # variável que irá conter os estados já visitados
explorados.append(tree.chave)
lacos = 0
verificacoes = 0
numN = len(tree.filhos)

inicio = time.time()
while flag == 1:
    if len(lista) < 2:
        print('a solução: ', lista[0].chave)
        print('Fim')
        break
    arvs = copy.deepcopy(lista)
    lista = []
    # testa cada nó de um nível #
    for estado in arvs:
        lacos += 1
        if estado.chave not in explorados:
            print('profundidade: ', estado.depth)
            exibe(estado.chave)
            time.sleep(0.7)
            os.system('clear')
            verificacoes += 1
            explorados.append(estado.chave)
            aux = []
            aux += busca(estado)
            numN += len(estado.filhos)
            if len(aux) < 2:
                verificacoes += 1
                print('Solução na profundidade: ', estado.depth)
                print('a solucao: ', estado.chave)
                # gerando o caminho do início até a solução #
                while(aux[0].pai):
                    print('           ',aux[0].pai.chave)
                    aux[0] = aux[0].pai
                print('fim')
                flag = 0
                break
            lista += aux # os filhos de um nó testado são armazenados aqui para o teste do próximo nível
fim = time.time()

print('número de iterações: ', lacos,'\nnós visitados: ', verificacoes, '\nnós gerados: ', numN)
print('tempo: ', fim-inicio, 's')