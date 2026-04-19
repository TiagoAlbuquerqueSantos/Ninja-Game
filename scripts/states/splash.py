
from .state import State


class Splash(State):
    def __init__(self):
        super().__init__()
        self.proximo = None

    def checar_evento(self, eventos):
        pass

    def atualizar(self, dt, tempo):
        pass

    def renderizar(self, surf):
        pass