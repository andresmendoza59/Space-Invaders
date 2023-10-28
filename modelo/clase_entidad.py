import pygame

screen = pygame.display.set_mode((800, 600))

# Se crea la clase entidad, para cualquier entidad que requiera moverse en la ventana
class Entidad:
    def __init__(self, imagen : str, posicion_x, posicion_y, cambio_posicion_x, cambio_posicion_y):
        self.imagen = pygame.image.load(f"{imagen}")
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.cambio_posicion_x = cambio_posicion_x
        self.cambio_posicion_y = cambio_posicion_y

    def mostrar_entidad(self):
        screen.blit(self.imagen, (self.posicion_x, self.posicion_y))