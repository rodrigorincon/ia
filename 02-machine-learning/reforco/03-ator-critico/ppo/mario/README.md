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

- O treino roda na CPU e leva horas: em teste, 4 ambientes rodaram ~110 passos/s. Os 2 milhões de passos padrão levam algumas horas.
- A IA treina **só na fase 1-1**. A fase 1-2 (subterrânea) é visualmente diferente e ela nunca a viu, então é normal ir mal nela: serve para ver o quanto o aprendizado generaliza.
