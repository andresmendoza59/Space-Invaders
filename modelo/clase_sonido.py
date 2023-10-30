import pygame

class Sonido:
    def __init__(self, multimedia: str):
        self.multimedia: str = multimedia

    def reproducir_musica(self):
        pygame.mixer.music.load(f"{self.multimedia}")
        pygame.mixer.music.play(-1)

    def reproducir_sonido(self):
        sonido = pygame.mixer.Sound(f"{self.multimedia}")
        sonido.play()