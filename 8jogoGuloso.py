import copy
import os
import time

numN = 1
iteracoes = 0

# pegando o estado inicial #
seq = input('Informe o problema: ')

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

# heurística utilizada #
h2 = [[4, 0, 1, 2, 2, 1, 3, 2, 3], [3, 1, 0, 1, 2, 1, 2, 3, 2], [2, 2, 1, 0, 3, 2, 1, 4, 3],
    [3, 1, 2, 3, 0, 1, 2, 1, 2], [2, 2, 1, 2, 1, 0, 1, 2, 1], [1, 3, 2, 1, 2, 1, 0, 3, 2],
    [2, 2, 3, 4, 1, 2, 3, 0, 1], [1, 3, 2, 3, 2, 1, 2, 1, 0], [0, 4, 3, 2, 3, 2, 1, 2, 1]]

explorados = [] # irá guardar os nós já visitados

''' retorna o nó com menor custo '''
def custoMin(filhos):
    global h2
    aux = filhos[0]
    for i in filhos:
        if i.getHeu(h2) < aux.getHeu(h2):
            aux = i
    filhos.remove(aux)
    return aux

''' visualização de um estado '''
def exibe(tbl):
    for i in range(3):
        print(tbl[i])

def solucaoGulosa(tree):
    global explorados
    global numN
    global h2
    global iteracoes

    if tree.chave not in explorados: explorados.append(tree.chave)

    print('profundidade: ', tree.depth, ', custo: ', tree.getHeu(h2))
    exibe(tree.chave)
    time.sleep(0.7)
    os.system('clear')

    if tree.chave == tblTeste: return tree
    filhos = decisao(tree.chave, tree.pos0, tree)
    numN += len(filhos)
    
    # testa o nó de menor custo e expande #
    while True:
        iteracoes += 1
        a = custoMin(filhos)
        if a.chave == tblTeste: return a
        if a.chave not in explorados:

            print('profundidade: ', a.depth, ', custo: ', a.getHeu(h2))
            exibe(a.chave)
            time.sleep(0.7)
            os.system('clear')

            filhos += decisao(a.chave, a.pos0, a)
            explorados.append(a.chave)
            numN += len(a.filhos)

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

inicio = time.time()
solution = solucaoGulosa(tree)
fim = time.time()

# resultados #
print('a solucao: ', solution.chave)
aux = copy.deepcopy(solution.pai)
while(aux):
    print('           ',aux.chave)
    aux = aux.pai

print('Solução na profundidade: ', solution.depth)
print('número de nós gerados: ', numN)
print('número de iterações: ', iteracoes)
print('tempo: ', fim-inicio, 's')