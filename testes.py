from mundo import Mundo
from agente import Agente
import time


def executar_simulacao(n, max_passos=100):
    ambiente = Mundo(n)
    agente = Agente()
    resultado = {
        'sucesso': False,
        'passos': 0,
        'motivo': None,
        'ouro': False,
        'wumpus_morto': False
    }

    for _ in range(max_passos):
        x, y = agente.pos
        # Verifica se o agente morreu
        if ambiente.matriz[x][y] == "W":
            resultado['motivo'] = "wumpus"
            agente.vivo = False
            break
        if ambiente.matriz[x][y] == "P":
            resultado['motivo'] = "poco"
            agente.vivo = False
            break
        
        percepcoes = obter_percepcoes(ambiente.matriz, agente.pos)
        acao = agente.decidir_acao(percepcoes)
        
        if agente.executar_acao(acao, ambiente.matriz):
            resultado['sucesso'] = True
            resultado['ouro'] = True
            break
            
        # Verifica se matou o Wumpus
        if acao == "atirar" and agente.flechas == 0:
            resultado['wumpus_morto'] = True

    resultado['passos'] = agente.passos
    return resultado

def obter_percepcoes(mundo, pos):
    x, y = pos
    percepcoes = set()
    vizinhos = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
    
    for i, j in vizinhos:
        if 0 <= i < len(mundo) and 0 <= j < len(mundo):
            if mundo[i][j] == "P":
                percepcoes.add("brisa")
            elif mundo[i][j] == "W":
                percepcoes.add("fedor")
            elif mundo[i][j] == "O":
                percepcoes.add("brilho")
    
    if mundo[x][y] == "O":
        percepcoes.add("ouro")
    
    return percepcoes

def executar_testes(n_simulacoes=100, tamanho_mundo=4):
    resultados = {
        'sucessos': 0,
        'mortes_por_wumpus': 0,
        'mortes_por_poco': 0,
        'passos_totais': 0,
        'wumpus_mortos': 0
    }

    for i in range(n_simulacoes):
        print(f"Executando simulação {i+1}/{n_simulacoes}", end="\r")
        resultado = executar_simulacao(tamanho_mundo)
        
        if resultado['sucesso']:
            resultados['sucessos'] += 1
        elif resultado['motivo'] == "wumpus":
            resultados['mortes_por_wumpus'] += 1
        elif resultado['motivo'] == "poco":
            resultados['mortes_por_poco'] += 1
            
        if resultado['wumpus_morto']:
            resultados['wumpus_mortos'] += 1
            
        resultados['passos_totais'] += resultado['passos']

    print("\nTestes concluídos!")
    return resultados

def analisar_resultados(resultados, n_simulacoes):
    print("\n=== Análise de Resultados ===")
    print(f"Total de simulações: {n_simulacoes}")
    print(f"Taxa de sucesso: {resultados['sucessos']/n_simulacoes*100:.2f}%")
    print(f"Mortes por Wumpus: {resultados['mortes_por_wumpus']/n_simulacoes*100:.2f}%")
    print(f"Mortes por poço: {resultados['mortes_por_poco']/n_simulacoes*100:.2f}%")
    print(f"Wumpus mortos: {resultados['wumpus_mortos']}")
    print(f"Média de passos por simulação: {resultados['passos_totais']/n_simulacoes:.2f}")
    
    print("\nDistribuição de Resultados:")
    print(f"Sucessos: {'#' * int(resultados['sucessos']/n_simulacoes*20)}")
    print(f"Mortes (Wumpus): {'#' * int(resultados['mortes_por_wumpus']/n_simulacoes*20)}")
    print(f"Mortes (Poço): {'#' * int(resultados['mortes_por_poco']/n_simulacoes*20)}")

if __name__ == "__main__":
    n_simulacoes = 100
    tamanho_mundo = 4
    
    print(f"Iniciando {n_simulacoes} simulações...")
    resultados = executar_testes(n_simulacoes, tamanho_mundo)
    analisar_resultados(resultados, n_simulacoes)
