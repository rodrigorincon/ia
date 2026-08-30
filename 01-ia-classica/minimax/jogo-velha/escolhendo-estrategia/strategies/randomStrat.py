import types
from typing import List, Tuple
import random

Position = Tuple[int, int]
TabRow = List[str]
Tabuleiro = List[TabRow]

def escolher_aleatoriamente(self, jogadas: List[Position]) -> Position:
  return random.choice(jogadas)

def setRandomStrat(self):
  self.definir_proxima_jogada = types.MethodType(escolher_aleatoriamente, self)
