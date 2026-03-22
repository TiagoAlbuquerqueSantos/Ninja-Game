
class Engine:
    def __init__(self, app) -> None:
        self.app = app

        self.state_dict = {}
        self.state_nome = None
        self.estado = None

    def setup_states(self, state_dict: dict, state_inicio: str) -> None:
        self.state_dict = state_dict
        self.state_nome = state_inicio
        self.estado = self.state_dict[self.state_nome]

    def trocar_estado(self) -> None:
        self.state_nome = self.estado.proximo
        params = self.estado.limpar_concluir()
        self.estado = self.state_dict[self.state_nome]
        self.estado.inicializar(params)

    def eventos_engine(self, eventos) -> None:
        self.estado.checar_evento(eventos)

    def atualizar(self, dt: float, tempo: float) -> None:
        if self.estado.feito:
            self.trocar_estado()
        self.estado.atualizar(dt, tempo)

    def renderizar(self, surf) -> None:
        self.estado.renderizar(surf)