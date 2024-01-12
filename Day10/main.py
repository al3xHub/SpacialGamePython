import pygame
from pygame import mixer
import random
import math

# Inicializar pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption('Spacial Invasion')
favicon = pygame.image.load('images/favicon.png')
pygame.display.set_icon(favicon)
fondo = pygame.image.load('images/fondo.jpg')

# agregar musica
mixer.music.load('sound/turbo_phase.mp3')
mixer.music.play(-1)

# Variable Jugador
img_jugador = pygame.image.load('images/nave.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variable enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

# Puntos
puntos = 0
fuente = pygame.font.Font('font/good-times/good times rg.otf', 32)
texto_x = 10
texto_y = 10

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('images/enemigo.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.2)
    enemigo_y_cambio.append(50)

# variable bala
img_bala = pygame.image.load('images/bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False

# texto game over
fuente_final = pygame.font.Font('font/good-times/good times rg.otf', 40)


def texto_final():
    mi_fuente_final = fuente_final.render('Game Over', True, (255,255,255))
    pantalla.blit(mi_fuente_final, (250, 200))


# funcion mostrar_puntos
def mostrar_puntos(x, y):
    texto = fuente.render(f'Puntos: {puntos}', True, (255,255,255))
    pantalla.blit(texto, (x, y))


# función jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# función enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# funciñon disparar
def disparar(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 24, y + 10))


def chequear_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y2 - y1, 2))
    if distancia < 27:
        return True
    else:
        return False


'''
Para abrir la ventana de manera permanente debemos realizar un bucle en el que se cortará la ejecución
cuando pulsemos el botón de cerrar.
ejemplo:
'''
se_ejecuta = True
while se_ejecuta:
    #  RGB pantalla
    # pantalla.fill((205, 144, 228))

    # img fondo
    pantalla.blit(fondo, (0, 0))
    # iterar eventos
    for event in pygame.event.get():
        # evento cerrar
        if event.type == pygame.QUIT:
            se_ejecuta = False
        # evento presionar teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
            elif event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
            elif event.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound('sound/disparo.mp3')
                sonido_disparo.set_volume(0.5)
                sonido_disparo.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar(bala_x, bala_y)
        # soltar flecha
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # modificar ubicación jugador
    jugador_x += jugador_x_cambio

    # mantener dentro de bordes jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar ubicación enemigo
    for e in range(cantidad_enemigos):
        # fin del juego
        if enemigo_y[e] > 460:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # mantener dentro de bordes enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.2
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.2
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colisión
        colision = chequear_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound('sound/explosion_editado.wav')
            sonido_colision.set_volume(0.1)
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntos += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    if bala_y <= -16:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntos(texto_x, texto_y)

    # Actualizar
    pygame.display.update()
