import copy
import time
import os

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

''' visualização de um estado '''
def exibe(tbl):
    for i in range(3):
        print(tbl[i])

iteracoes = 0
verificacoes = 0
numN = 0

def solucaoProfundidade(tree):
    global iteracoes
    global verificacoes
    global numN

    print('profundidade: ', tree.depth)
    exibe(tree.chave)
    time.sleep(0.7)
    os.system('clear')

    if tree.chave == tblTeste: return tree
    
    sol = None
    filhos = decisao(tree.chave, tree.pos0, tree)
    numN += len(filhos)

    for no in filhos:
        iteracoes += 1
        verificacoes += 1

        if no.chave == tblTeste: return no

        print('profundidade: ', no.depth)
        exibe(no.chave)
        time.sleep(0.7)
        os.system('clear')

        if no.depth > 7: continue

        sol = solucaoProfundidade(no)
        if sol != None: return sol

class NodoArvore:
    def __init__(self, pos0, chave=None, pai=None, depth=None):
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
solution = solucaoProfundidade(tree)
fim = time.time()

# resultados #
if solution:
    print('a solucao: ', solution.chave)
    aux = copy.deepcopy(solution.pai)
    while(aux):
        print('           ',aux.chave)
        aux = aux.pai
    print('Solução na profundidade: ', solution.depth)
else: print('Solução não encontrada')

print('iterações: ', iteracoes, '\nnós visitados: ', verificacoes)
print('número de nós gerados: ', numN)
print('tempo: ', fim-inicio, 's')