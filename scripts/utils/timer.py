from typing import Any

from pygame.time import get_ticks


class Timer:
    def __init__(
            self,
            duracao: int,
            repetir: bool = False,
            auto_start: bool = False,
            funcao: Any = None
    ) -> None:
        self.duracao = duracao
        self.tempo_inicial = 0
        self.ativo = False
        self.repetir = repetir
        self.funcao = funcao
        if auto_start:
            self.ativar()

    def ativar(self) -> None:
        self.ativo = True
        self.tempo_inicial = get_ticks()

    def desativar(self) -> None:
        self.ativo = False
        self.tempo_inicial = 0
        if self.repetir:
            self.ativar()

    def atualizar(self) -> None:
        if self.ativo:
            tempo_atual = get_ticks()
            if tempo_atual - self.tempo_inicial >= self.duracao:
                if self.funcao:
                    self.funcao()
                self.desativar()
