from random import random, choice


class Nuvem:
    def __init__(self, pos, img, velocidade, margem):
        self.pos = list(pos)
        self.img = img
        self.vel = velocidade
        self.margem = margem

    def atualizar(self, dt):
        self.pos[0] += self.vel * 100 * dt

    def renderizar(self, surf, deslocamento=(0, 0)):
        renderizar_pos = (self.pos[0] - deslocamento[0] * self.margem, self.pos[1] - deslocamento[1] * self.margem)
        surf.blit(self.img, (renderizar_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(),
                             renderizar_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))


class Nuvens:
    def __init__(self, imagens_nuvens, quant=16):
        self.nuvens = []

        for _ in range(quant):
            img_nuvem = choice(imagens_nuvens)
            pos = (int(random() * 99999), int(random() * 99999))
            vel = 0.2 + random() * 0.2
            margem = 0.5 + random() * 0.5
            self.nuvens.append(Nuvem(pos, img_nuvem, vel, margem))

        self.nuvens.sort(key=lambda x: x.margem)

    def atualizar(self, dt):
        for nuvem in self.nuvens:
            nuvem.atualizar(dt)

    def renderizar(self, surf, deslocamento=(0, 0)):
        for nuvem in self.nuvens:
            nuvem.renderizar(surf, deslocamento=deslocamento)
