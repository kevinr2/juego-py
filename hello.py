import pygame
import random
import math
import io
from pygame import mixer


def fuente_bytes(fuente):
    with open(fuente, "rb") as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


pygame.init()


# pantalla de inicio
pantalla = pygame.display.set_mode((800, 600))

# titulo
pygame.display.set_caption("Invasion espacial")

# fondo
fondo = pygame.image.load("fondo.jpg")


# music
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# icono
icon = pygame.image.load("ovni.png")
pygame.display.set_icon(icon)


def texto_final():
    mi_fuente = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente, (70, 200))


# jugador
cohete = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
# enemigo
enemigo_png = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

# for enemigos
for e in range(cantidad_enemigos):
    enemigo_png.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.1)
    enemigo_y_cambio.append(50)
# bala
img_bala = pygame.image.load("bala.png")
balas = []
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False

# puntaje
puntaje = 0
fuentes_con_bytes = fuente_bytes("FreeSansBold.ttf")
fuente = pygame.font.Font(
    fuentes_con_bytes,
    16,
)
texto_x = 10
texto_y = 10
# texto final
fuente_final = pygame.font.Font(fuentes_con_bytes, 60)


def monstar_puntaje(x, y):
    texto = fuente.render(f"Puntaje : {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


def jugador(x, y):
    pantalla.blit(cohete, (x, y))


def enemigo(x, y, ene):
    pantalla.blit(enemigo_png[ene], (x, y))


def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + (math.pow(y_1 - y_2, 2)))
    if distancia < 27:
        return True
    else:
        return False


# loop del juego


se_ejecute = True

while se_ejecute:
    # rgb
    pantalla.blit(fondo, (0, 0))

    for event in pygame.event.get():
        # para utilizar las flechas del teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio -= 1
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio += 1
            if event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                nueva_bala = {"x": jugador_x, "y": jugador_y, "velocidad": -0.5}
                balas.append(nueva_bala)
        # para soltar teclado
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
        if event.type == pygame.QUIT:
            se_ejecute = False

    # mantener dentro de la pantalla
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # enemigo movimiento de la pantalla
    for e in range(cantidad_enemigos):
        enemigo_x[e] += enemigo_x_cambio[e]

        # fin del juego
        if enemigo_y[e] > 450:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        # enemigo cambio dentro de los bordes
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3

        # colision
        for bala in balas:
            colision_bala_enemigo = hay_colision(
                enemigo_x[e], enemigo_y[e], bala["x"], bala["y"]
            )
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # jugador cambios
    jugador_x += jugador_x_cambio
    # movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    # colision

    jugador(jugador_x, jugador_y)

    monstar_puntaje(
        texto_x,
        texto_y,
    )

    # actualizar
    pygame.display.update()

# Movimiento bala
