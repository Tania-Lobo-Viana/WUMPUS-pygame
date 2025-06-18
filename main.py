from mundo import Mundo
from agente import Agente
from sensores import sensores
from testes import obter_percepcoes

def mostrar_visao_agente(mundo, agente_pos):
    print("\nVisão do Agente:")
    for i in range(len(mundo)):
        linha = []
        for j in range(len(mundo[i])):
            if [i, j] == agente_pos:
                linha.append(" 🥷🏻 ")
            else:
                linha.append(" ❓ ")
        print(" ".join(linha))
    print()

def modo_interativo():
    n = int(input("Digite o tamanho da matriz (n >= 3): "))
    while n < 3:
        n = int(input("Valor inválido. Digite um número >= 3: "))

    ambiente = Mundo(n)
    jogador = Agente()

    print("Bem-vindo ao Mundo de Wumpus (Modo Interativo)!")
    print("Controles: mover, pegar, atirar, sair")

    while True:
        mostrar_visao_agente(ambiente.matriz, jogador.pos)
        sensores(ambiente.matriz, jogador.pos)
        
        acao = input("Escolha uma ação: ").lower()
        
        if acao == "sair":
            break
            
        percepcoes = obter_percepcoes(ambiente.matriz, jogador.pos)
        if acao == "auto":
            acao = jogador.decidir_acao(percepcoes)
            print(f"Agente escolheu: {acao}")
        
        if acao == "mover":
            direcao = input("Direção: ").lower()
            jogador.mover(direcao, len(ambiente.matriz))
        elif acao == "pegar":
            jogador.pegar_ouro(ambiente.matriz)
        elif acao == "atirar":
            direcao = input("Direção: ").lower()
            jogador.atirar(ambiente.matriz, direcao)
        
        x, y = jogador.pos
        if ambiente.matriz[x][y] == "W":
            print("Você encontrou o Wumpus! Game Over!")
            break
        if ambiente.matriz[x][y] == "P":
            print("Você caiu em um poço! Game Over!")
            break
        if jogador.ouro and jogador.pos == [0, 0]:
            print("Parabéns! Você venceu com o ouro!")
            break

if __name__ == "__main__":
    print("1. Modo Interativo")
    print("2. Executar Testes Automatizados")
    opcao = input("Escolha o modo: ")
    
    if opcao == "1":
        modo_interativo()
    else:
        from testes import executar_testes, analisar_resultados
        n_simulacoes = int(input("Número de simulações: "))
        tamanho_mundo = int(input("Tamanho do mundo: "))
        resultados = executar_testes(n_simulacoes, tamanho_mundo)
        analisar_resultados(resultados, n_simulacoes)
