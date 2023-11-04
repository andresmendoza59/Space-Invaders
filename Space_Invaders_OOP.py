import pygame
import random
from modelo.clase_texto import Texto
from modelo.clase_entidad import Entidad
from modelo.clase_sonido import Sonido
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))

# Se cambia el título e ícono de la ventana
pygame.display.set_caption("Space Invaders")
icono = pygame.image.load("multimedia/alien.png")
pygame.display.set_icon(icono)

# Se carga la imagen del fondo y la música del juego
fondo = pygame.image.load("multimedia/space.jpg").convert_alpha()
musica_fondo = Sonido("multimedia/musica_de_fondo.mp3")
musica_fondo.reproducir_musica()

# Se crean las instancias de la clase Texto
puntaje = Texto(tamaño = 24, COORDENADA_X = 10, COORDENADA_Y = 10, valor = 0)
texto_game_over = Texto(tamaño = 48, COORDENADA_X = 280, COORDENADA_Y = 250, valor = "Game Over")

# Se crean las instancias de la clase Entidad
jugador = Entidad(imagen = "multimedia/spaceship.png", posicion_x = 370,posicion_y = 480, cambio_posicion_x = 0, cambio_posicion_y = 0)

enemigo = [Entidad(imagen = "multimedia/enemy.png", posicion_x = random.randint(64, 736), posicion_y = random.randint(64, 136),
                   cambio_posicion_x = 0.3, cambio_posicion_y = 25) for _ in range(6)]
bala = Entidad(imagen = "multimedia/bullet.png", posicion_x = jugador.posicion_x, posicion_y = 480, cambio_posicion_x = 0, \
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
                    sonido_bala = Sonido("multimedia/laser-arma.mp3")
                    sonido_bala.reproducir_sonido()
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
            enemigo[i].cambio_posicion_x = 0.3
            enemigo[i].posicion_y += enemigo[i].cambio_posicion_y

        elif enemigo[i].posicion_x >= 736:
            enemigo[i].cambio_posicion_x = -0.3
            enemigo[i].posicion_y += enemigo[i].cambio_posicion_y

        # Colisión
        verificar_colision = colision(enemigo[i].posicion_x, enemigo[i].posicion_y, bala.posicion_x, bala.posicion_y)
        if verificar_colision:
            sonido_colision = Sonido("multimedia/colision.mp3")
            sonido_colision.reproducir_sonido()
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