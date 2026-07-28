import pygame

# Inicializar pygame
pygame.init()

# Crear pantalla de juego
pantalla = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pizza Survivor")
icono = pygame.image.load("assets/pizza.png")
pygame.display.set_icon(icono)

# Fondo de juego
fondo = pygame.image.load("assets/fondo.png")
fondo = pygame.transform.scale(fondo, (800, 600))

# Repartidor
repartidor_img = pygame.image.load("assets/repartidor.png")
repartidor_img = pygame.transform.scale(repartidor_img, (64, 100))
repartidor_x = 368
repartidor_y = 440
repartidor_cambio_x = 0
repartidor_cambio_y = 0
repartidor_velocidad = 5  # Subimos la velocidad base para que se sienta fluido a 60 FPS


def repartir(x, y):
    pantalla.blit(repartidor_img, (x, y))


# Reloj para controlar los FPS (Fotogramas por segundo)
reloj = pygame.time.Clock()

# Bucle principal del juego
se_ejecuta = True
while se_ejecuta:

    # 1. CAPTURA DE EVENTOS (Teclado y Ratón)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # CORREGIDO: Faltaba el .type aquí
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                repartidor_cambio_x = -repartidor_velocidad
            if evento.key == pygame.K_RIGHT:
                repartidor_cambio_x = repartidor_velocidad
            if evento.key == pygame.K_UP:
                repartidor_cambio_y = -repartidor_velocidad
            if evento.key == pygame.K_DOWN:
                repartidor_cambio_y = repartidor_velocidad

        if evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_RIGHT):
                repartidor_cambio_x = 0
            if evento.key in (pygame.K_UP, pygame.K_DOWN):
                repartidor_cambio_y = 0

    # 2. ACTUALIZACIÓN DE LÓGICA (Fuera del for de eventos)
    repartidor_x += repartidor_cambio_x
    repartidor_y += repartidor_cambio_y
    if repartidor_x < 0:
        repartidor_x = 0
    elif repartidor_x > 736:
        repartidor_x = 736
    if repartidor_y < 0:
        repartidor_y = 0
    elif repartidor_y > 500:
        repartidor_y = 500

    # 3. DIBUJO EN PANTALLA (Fuera del for de eventos)
    pantalla.blit(fondo, (0, 0))
    repartir(repartidor_x, repartidor_y)

    pygame.display.update()

    # Controlar que el juego corra a 60 cuadros por segundo
    reloj.tick(60)

pygame.quit()