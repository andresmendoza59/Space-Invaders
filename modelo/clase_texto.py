import pygame

screen = pygame.display.set_mode((800, 600))
# Se crea la clase texto para toda acción en el programa que implique agregar texto a la ventana
class Texto:
    def __init__(self, tamaño : int, COORDENADA_X : int, COORDENADA_Y : int, valor, tipo_letra = "freesansbold.ttf"):
        self.tamaño = tamaño
        self.tipo_letra = pygame.font.Font(f"{tipo_letra}", self.tamaño)
        self.valor = valor
        self.COORDENADA_X = COORDENADA_X
        self.COORDENADA_Y = COORDENADA_Y
        
    def mostrar_puntaje(self):
        puntaje = self.tipo_letra.render(f"Puntaje: {str(self.valor)}", True, (255, 255, 255))
        screen.blit(puntaje, (self.COORDENADA_X, self.COORDENADA_Y))

    def game_over_texto(self):
        over = self.tipo_letra.render(f"{self.valor}", True, (255, 255, 255))
        screen.blit(over, (self.COORDENADA_X, self.COORDENADA_Y))