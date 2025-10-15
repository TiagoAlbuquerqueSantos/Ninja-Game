import random

class Nuvem:
    def __init__(self, pos, img, velocidade, margem):
        self.pos = list(pos)
        self.img = img
        self.vel = velocidade
        self.margem = margem

    def atualizar(self):
        self.pos[0] += self.vel

    def renderizar(self, surf, deslocamento=(0, 0)):
        renderizar_pos = (self.pos[0] - deslocamento[0] * self.margem, self.pos[1] - deslocamento[1] * self.margem)
        surf.blit(self.img, (renderizar_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(),
                             renderizar_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))

class Nuvens:
    def __init__(self, imagens_nuvens, quant=16):
        self.nuvens = []

        for i in range(quant):
            self.nuvens.append(Nuvem((random.random() * 99999, random.random() * 99999),
                                     random.choice(imagens_nuvens), random.random() * 0.05 + 0.05,
                                     random.random() * 0.6 + 0.2))
        self.nuvens.sort(key=lambda x: x.margem)

    def atualizar(self):
        for nuvem in self.nuvens:
            nuvem.atualizar()

    def renderizar(self, surf, deslocamento=(0, 0)):
        for nuvem in self.nuvens:
            nuvem.renderizar(surf, deslocamento=deslocamento)
