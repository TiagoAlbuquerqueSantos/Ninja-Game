class Particula:
    def __init__(self, main, tipo_p, pos, velocidade=(0, 0), frame=0):
        self.main = main
        self.tipo = tipo_p
        self.pos = list(pos)
        self.velocidade = list(velocidade)
        self.animacao = self.main.assets['particulas/' + tipo_p].copia()
        self.animacao.frame = frame

    def atualizar(self):
        interromper = False
        if self.animacao.concluido:
            interromper = True

        self.pos[0] += self.velocidade[0]
        self.pos[1] += self.velocidade[1]

        self.animacao.atualizar()

        return interromper

    def renderizar(self, surf, deslocamento=(0, 0)):
        imagem = self.animacao.imagem()
        surf.blit(imagem, (self.pos[0] - deslocamento[0] - imagem.get_width() // 2,
                           self.pos[1] - deslocamento[1] - imagem.get_height() // 2))
