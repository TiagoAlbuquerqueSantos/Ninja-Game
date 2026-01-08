

class State(object):
    def __init__(self):
        self.feito = False
        self.sair = False
        self.proximo = None
        self.parametros = {}

    def inicializar(self, *args):
        self.parametros = args

    def limpar_concluir(self):
        self.feito = False
        return self.parametros

    def checar_evento(self, eventos):
        pass

    def atualizar(self, dt, tempo):
        pass

    def renderizar(self, surf):
        pass
