import pygame, random
pygame.init()

screen = pygame.display.set_mode((800, 600))

# Se cambia el título e ícono de la ventana
pygame.display.set_caption("Space Invaders")
icono = pygame.image.load("alien.png")
pygame.display.set_icon(icono)

# Se carga la imagen del fondo
fondo = pygame.image.load("space.jpg").convert_alpha()

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

# Se crean las instancias de la clase Texto
puntaje = Texto(tamaño = 24, COORDENADA_X = 10, COORDENADA_Y = 10, valor = 0)
texto_game_over = Texto(tamaño = 48, COORDENADA_X = 280, COORDENADA_Y = 250, valor = "Game Over")

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

# Se crean las instancias de la clase Entidad
jugador = Entidad(imagen = "spaceship.png", posicion_x = 370,posicion_y = 480,cambio_posicion_x = 0,cambio_posicion_y = 0)
enemigo = [Entidad(imagen="enemy.png", posicion_x=random.randint(64, 736), posicion_y=random.randint(64, 136),
                   cambio_posicion_x=0.3, cambio_posicion_y=25) for _ in range(6)]

bala = Entidad(imagen = "bullet.png", posicion_x = jugador.posicion_x, posicion_y = 480, cambio_posicion_x = 0, \
               cambio_posicion_y = 0.8)
estado_bala = False

def disparar(x, y):
    global estado_bala
    estado_bala = True
    screen.blit(bala.imagen, (x + 16, y + 10))

def colision(enemigoX, enemigoY, balaX, balaY):
    # Se usa la ecuación de distancia para verificar la colisión
    distancia = ((enemigoX - balaX)**2 + (enemigoY - balaY)**2)**0.5
    if distancia <= 27:
        return True
    
    return False

NUMERO_ENEMIGOS = 6

ejecutando = True

# Iteración infinita de la ventana
while ejecutando:
    screen.blit(fondo, (0,0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Trackeo de pulsación de teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador.cambio_posicion_x = -0.3

            if evento.key == pygame.K_RIGHT:
                jugador.cambio_posicion_x = 0.3
            # Dibuja la bala en la pantalla de juego, al presionarse espacio.
            if evento.key == pygame.K_SPACE:
                if estado_bala == False:
                    bala.posicion_x = jugador.posicion_x
                    disparar(bala.posicion_x, bala.posicion_y)

        elif evento.type == pygame.KEYUP:
             if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador.cambio_posicion_x = 0 

    # Límites de la pantalla para nave y enemigos.
    jugador.posicion_x += jugador.cambio_posicion_x

    if jugador.posicion_x <= 0:
        jugador.posicion_x = 0

    elif jugador.posicion_x >= 736:
        jugador.posicion_x = 736

    # Movimiento enemigo
    for i in range(NUMERO_ENEMIGOS):

        # Se mostrará 'Game Over' cuando el enemigo esté en la posición del jugador
        if enemigo[i].posicion_y > 440:
            for j in range(NUMERO_ENEMIGOS):
                enemigo[j].posicion_y = 1000
            texto_game_over.game_over_texto()
            break                 

        enemigo[i].posicion_x += enemigo[i].cambio_posicion_x

        if enemigo[i].posicion_x <= 0:
            enemigo[i].cambio_posicion_x = 0.5
            enemigo[i].posicion_y += enemigo[i].cambio_posicion_y

        elif enemigo[i].posicion_x >= 736:
            enemigo[i].cambio_posicion_x = -0.5
            enemigo[i].posicion_y += enemigo[i].cambio_posicion_y

        # Colisión
        verificar_colision = colision(enemigo[i].posicion_x, enemigo[i].posicion_y, bala.posicion_x, bala.posicion_y)
        if verificar_colision:
            bala.posicion_y = 480
            estado_bala = False
            puntaje.valor += 1
            enemigo[i].posicion_x = random.randint(64, 736)
            enemigo[i].posicion_y = random.randint(64, 136)

        enemigo[i].mostrar_entidad()    

    # Movimiento de la bala, se cambia su estado, y se invoca a la función 'disparar'
    if bala.posicion_y <= 0:
        bala.posicion_y = 480
        estado_bala = False

    elif estado_bala == True:
        disparar(bala.posicion_x, bala.posicion_y)
        bala.posicion_y -= bala.cambio_posicion_y

    jugador.mostrar_entidad()
    puntaje.mostrar_puntaje()
    pygame.display.update()