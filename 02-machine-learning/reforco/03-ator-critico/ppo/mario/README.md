# PPO jogando Super Mario Bros

Mesma ideia do `cart-pole.py`, mas agora a IA vê **a tela do jogo** (imagem) ao invés de 4 números. Por isso a política é uma `CnnPolicy` (rede convolucional) e o treino precisa de muito mais passos.

## Arquivos

| Arquivo | O que faz |
|---|---|
| `config.py` | Todos os hiperparâmetros e configurações (fases, passos de treino, velocidade da demonstração) |
| `ambiente.py` | Cria o jogo e aplica os wrappers: 7 ações, pular frames, tons de cinza, 84x84, empilhar 4 frames |
| `treinar.py` | Treina o PPO na fase 1-1 com vários jogos em paralelo e, no final, chama a demonstração |
| `assistir.py` | Abre uma janela mostrando a IA jogando as fases 1-1 e 1-2 (pode ser rodado sozinho) |

## Como rodar

```bash
pip install -r requirements.txt
python treinar.py    # treina, salva em modelos/ e mostra a IA jogando no final
python assistir.py   # só mostra a IA jogando com o último modelo salvo
```

- `Ctrl+C` durante o treino interrompe, salva o modelo e segue para a demonstração.
- Rodar `treinar.py` de novo continua o treino do modelo salvo (`CONTINUAR_TREINO` em `config.py`).
- Na janela da demonstração, `q` fecha.

## O que esperar

- O treino em um computador caseiro rodando na CPU leva horas: localmente, 12 ambientes em paralelo rodaram os 2 milhões de passos em 4 horas.
- A IA treina **só na fase 1-1**. A fase 1-2 (subterrânea) é visualmente diferente e ela nunca a viu, então é normal ir mal nela: serve para ver o quanto o aprendizado generaliza.
- Não existe um número fixo de partidas jogadas pela IA, mas sim de passos dados. Assim ela pode jogar mais ou menos partidas a depender se morrer rápido ou não. Mas o número mínimo é de 833 partidas.
- O episódio acaba se o Mario morrer, se o tempo acabar ou se ele concluir a fase. Tudo isso é controlado pela biblioteca `gym_super_mario_bros` que faz tudo internamente.
- O número médio de passos por episódio é informado em `ep_len_mean`.