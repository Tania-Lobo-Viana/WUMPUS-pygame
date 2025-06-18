import random

class Agente:
    def __init__(self):
        self.pos = [0, 0]
        self.flechas = 1
        self.ouro = False
        self.vivo = True
        self.regras = [
            {"percepcoes": {"fedor", "brisa"}, "acao": "voltar"},
            {"percepcoes": {"fedor"}, "acao": "atirar"},
            {"percepcoes": {"brilho"}, "acao": "pegar"},
            {"percepcoes": set(), "acao": "mover_aleatorio"},
            {"percepcoes": {"ouro"}, "acao": "voltar"}
        ]
        self.passos = 0
        self.acao_anterior = None

    def reset(self):
        self.__init__()

    def decidir_acao(self, percepcoes):
        self.passos += 1
        if self.ouro and self.pos == [0, 0]:
            return "sair"
            
        regras_possiveis = []
        for regra in self.regras:
            if regra["percepcoes"].issubset(percepcoes):
                regras_possiveis.append(regra["acao"])
        
        if not regras_possiveis:
            return "mover_aleatorio"
            
        acao = random.choice(regras_possiveis)
        self.acao_anterior = acao
        return acao

  
    def executar_acao(self, acao, mundo):
        if acao == "mover_aleatorio":
            direcoes = ["cima", "baixo", "esquerda", "direita"]
            direcao = random.choice(direcoes)
            self.mover(direcao, len(mundo))
        elif acao == "voltar":
            self.voltar_para_casa()
        elif acao == "atirar":
            direcoes = ["cima", "baixo", "esquerda", "direita"]
            direcao = random.choice(direcoes)
            self.atirar(mundo, direcao)
        elif acao == "pegar":
            self.pegar_ouro(mundo)
        elif acao == "sair":
            print("Você escapou com o ouro! Vitória!")
            return True
        return False

    def voltar_para_casa(self):
        # Movimento simples em direção à casa (0,0)
        x, y = self.pos
        if x > 0:
            self.pos[0] -= 1
        elif y > 0:
            self.pos[1] -= 1

    def mover(self, direcao, tamanho_mundo):
        x, y = self.pos
        if direcao == "cima" and x > 0:
            self.pos[0] -= 1
        elif direcao == "baixo" and x < tamanho_mundo - 1:
            self.pos[0] += 1
        elif direcao == "esquerda" and y > 0:
            self.pos[1] -= 1
        elif direcao == "direita" and y < tamanho_mundo - 1:
            self.pos[1] += 1

    def pegar_ouro(self, mundo):
        x, y = self.pos
        if mundo[x][y] == "O":
            self.ouro = True
            mundo[x][y] = "-"
            print("Você pegou o ouro!")

    def atirar(self, mundo, direcao):
        if self.flechas == 0:
            return
        self.flechas -= 1
        x, y = self.pos

        if direcao == "cima":
            for i in range(x - 1, -1, -1):
                if mundo[i][y] == "W":
                    mundo[i][y] = "-"
                    print("Você matou o Wumpus!")
                    return
        elif direcao == "baixo":
            for i in range(x + 1, len(mundo)):
                if mundo[i][y] == "W":
                    mundo[i][y] = "-"
                    print("Você matou o Wumpus!")
                    return
        elif direcao == "esquerda":
            for j in range(y - 1, -1, -1):
                if mundo[x][j] == "W":
                    mundo[x][j] = "-"
                    print("Você matou o Wumpus!")
                    return
        elif direcao == "direita":
            for j in range(y + 1, len(mundo[0])):
                if mundo[x][j] == "W":
                    mundo[x][j] = "-"
                    print("Você matou o Wumpus!")
                    return
        print("Você atirou, mas não acertou nada.")
