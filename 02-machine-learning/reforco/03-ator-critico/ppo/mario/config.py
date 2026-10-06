# Todas as configurações do projeto ficam aqui para facilitar os experimentos
import os

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_MODELOS = os.path.join(PASTA_PROJETO, "modelos")
ARQUIVO_MODELO = os.path.join(PASTA_MODELOS, "mario_ppo")  # o stable-baselines3 adiciona o ".zip"

# ------------------------------------------------------------------------------------------------
# AMBIENTE
# ------------------------------------------------------------------------------------------------
FASE_TREINO = "1-1"               # mundo-fase usado no treino
FASES_DEMONSTRACAO = ["1-1", "1-2"]  # fases mostradas ao final do treino
PULAR_FRAMES = 4      # a IA escolhe uma ação a cada 4 frames (repete a ação nos frames intermediários)
TAMANHO_IMAGEM = 84   # a tela (240x256 colorida) vira uma imagem 84x84 em tons de cinza
FRAMES_EMPILHADOS = 4  # a IA vê os últimos 4 frames juntos, assim consegue perceber movimento e velocidade
ESCALA_RECOMPENSA = 15  # divide a recompensa do jogo para deixá-la perto da faixa [-1, 1], o que estabiliza o treino

# ------------------------------------------------------------------------------------------------
# TREINO (PPO)
# ------------------------------------------------------------------------------------------------
TOTAL_PASSOS = 2_000_000  # passos somados de todos os ambientes em todos os episódios.
N_AMBIENTES = 12          # cópias do jogo rodando em paralelo (cada uma em um processo)
N_STEPS = 512             # passos coletados por ambiente antes de cada atualização (buffer = N_STEPS * N_AMBIENTES)
BATCH_SIZE = 256          # tamanho dos mini-batches do gradiente
N_EPOCHS = 4              # quantas vezes o buffer é reaproveitado em cada atualização
TAXA_APRENDIZADO = 0.0001
GAMMA = 0.9               # fator de desconto
GAE_LAMBDA = 0.95         # balanço curto x longo prazo no cálculo da vantagem
CLIP_RANGE = 0.2          # limita a atualização da política a no máximo 20%
ENT_COEF = 0.01           # bônus de entropia: incentiva a IA a continuar testando ações diferentes
SALVAR_A_CADA = 100_000   # passos entre os checkpoints salvos em modelos/
CONTINUAR_TREINO = True   # se já existir um modelo salvo, continua o treino a partir dele

# ------------------------------------------------------------------------------------------------
# DEMONSTRAÇÃO VISUAL
# ------------------------------------------------------------------------------------------------
FPS_DEMONSTRACAO = 15     # 60 fps do NES / 4 frames pulados = velocidade real do jogo
ESCALA_JANELA = 3         # aumenta a janela (a tela do NES é pequena)
ACAO_DETERMINISTICA = False  # False = sorteia a ação pelas probabilidades da política (igual ao treino), o que evita a IA travar repetindo a mesma ação
MAX_PASSOS_DEMONSTRACAO = 3000  # segurança caso a IA fique parada
