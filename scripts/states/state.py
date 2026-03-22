
from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self) -> None:
        self.feito = False
        self.sair = False
        self.proximo = None
        self.parametros = {}

    def inicializar(self, *args):
        self.parametros = args

    def limpar_concluir(self) -> dict:
        self.feito = False
        return self.parametros

    @abstractmethod
    def checar_evento(self, eventos) -> None:
        pass

    @abstractmethod
    def atualizar(self, dt, tempo) -> None:
        pass

    @abstractmethod
    def renderizar(self, surf) -> None:
        pass
