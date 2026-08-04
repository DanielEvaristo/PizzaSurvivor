import pygame
import random

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
repartidor_velocidad = 5

# Perro
perro_img = pygame.image.load("assets/perro.png")
perro_img = pygame.transform.scale(perro_img, (54, 54))
velocidad_perro = 3
perros = []

tiempo_ultimo_perro = 0
intervalo_perro = 2000

# Pizza
pizza_img = pygame.image.load("assets/pizza.png")
pizza_img = pygame.transform.scale(pizza_img, (32, 32))
pizzas = []
velocidad_pizza = 8
tiempo_ultima_pizza = 0
intervalo_pizza = 3000

# Vidas
corazon_img = pygame.image.load("assets/corazon.png")
corazon_img = pygame.transform.scale(corazon_img, (32, 32))
vidas = 3
tiempo_ultimo_golpe = 0
duracion_invulnerabilidad = 1000  # 1 segundo exacto


def repartir(x, y):
    pantalla.blit(repartidor_img, (x, y))


def perro(x, y):
    pantalla.blit(perro_img, (x, y))


def dibujar_vidas():
    for i in range(vidas):
        pantalla.blit(corazon_img, (10 + i * 38, 10))


# NUEVA FUNCIÓN: Genera un perro en un borde aleatorio de la pantalla
def crear_perro():
    borde = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
    if borde == 'arriba':
        x = random.randint(0, 800 - 54)
        y = -54
    elif borde == 'abajo':
        x = random.randint(0, 800 - 54)
        y = 600
    elif borde == 'izquierda':
        x = -54
        y = random.randint(0, 600 - 54)
    else:  # derecha
        x = 800
        y = random.randint(0, 600 - 54)

    perros.append([x, y])


def encontrar_perro_mas_cercano(x, y):
    perro_mas_cercano = None
    distancia_mas_cercana = None

    for perro_actual in perros:
        dx = perro_actual[0] - x
        dy = perro_actual[1] - y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia_mas_cercana is None or distancia < distancia_mas_cercana:
            distancia_mas_cercana = distancia
            perro_mas_cercano = perro_actual

    return perro_mas_cercano


def lanzar_pizza():
    perro_objetivo = encontrar_perro_mas_cercano(repartidor_x, repartidor_y)

    if perro_objetivo is not None:
        pizza_x = repartidor_x + 16
        pizza_y = repartidor_y + 34

        objetivo_x = perro_objetivo[0] + 27
        objetivo_y = perro_objetivo[1] + 27

        dx = objetivo_x - pizza_x
        dy = objetivo_y - pizza_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia > 0:
            cambio_x = (dx / distancia) * velocidad_pizza
            cambio_y = (dy / distancia) * velocidad_pizza
            pizzas.append([pizza_x, pizza_y, cambio_x, cambio_y])


def dibujar_pizza(x, y):
    pantalla.blit(pizza_img, (x, y))


def detectar_colisiones():
    global perros, pizzas, vidas, tiempo_ultimo_golpe
    pizzas_sobrevivientes = []
    perros_sobrevivientes = perros[:]

    # 1. COLISIÓN: PIZZAS CON PERROS
    for pizza_actual in pizzas:
        pizza_choco = False
        for perro_actual in perros_sobrevivientes[:]:
            dx = perro_actual[0] - pizza_actual[0]
            dy = perro_actual[1] - pizza_actual[1]
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            if distancia < 27:
                perros_sobrevivientes.remove(perro_actual)
                pizza_choco = True
                break

        if not pizza_choco:
            pizzas_sobrevivientes.append(pizza_actual)

    # 2. COLISIÓN: PERROS CON REPARTIDOR
    tiempo_actual = pygame.time.get_ticks()
    invulnerable = tiempo_actual - tiempo_ultimo_golpe < duracion_invulnerabilidad

    # Si NO somos invulnerables, revisamos si un perro nos toca
    if not invulnerable:
        # Obtenemos el centro aproximado del repartidor (caja de 64x100)
        centro_repartidor_x = repartidor_x + 32
        centro_repartidor_y = repartidor_y + 50

        for perro_actual in perros_sobrevivientes[:]:
            # Centro aproximado del perro (caja de 54x54)
            centro_perro_x = perro_actual[0] + 27
            centro_perro_y = perro_actual[1] + 27

            dx = centro_repartidor_x - centro_perro_x
            dy = centro_repartidor_y - centro_perro_y
            distancia = (dx ** 2 + dy ** 2) ** 0.5

            # Si la distancia es menor a un radio combinado (ej. 45 píxeles)
            if distancia < 45:
                vidas -= 1
                tiempo_ultimo_golpe = tiempo_actual
                perros_sobrevivientes.remove(perro_actual) # El perro que te golpea desaparece
                break # Salimos del ciclo para no perder más de 1 vida en el mismo frame

    pizzas = pizzas_sobrevivientes
    perros = perros_sobrevivientes


# Reloj para controlar los FPS
reloj = pygame.time.Clock()

# Bucle principal del juego
se_ejecuta = True
while se_ejecuta:

    # 1. CAPTURA DE EVENTOS (Teclado y Ratón)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

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

    # 2. ACTUALIZACIÓN DE LÓGICA
    repartidor_x += repartidor_cambio_x
    repartidor_y += repartidor_cambio_y

    # Límites de pantalla para el repartidor
    if repartidor_x < 0:
        repartidor_x = 0
    elif repartidor_x > 736:
        repartidor_x = 736
    if repartidor_y < 0:
        repartidor_y = 0
    elif repartidor_y > 500:
        repartidor_y = 500

    tiempo_actual = pygame.time.get_ticks()

    # Crear un nuevo perro cada 2 segundos
    if tiempo_actual - tiempo_ultimo_perro >= intervalo_perro:
        crear_perro()
        tiempo_ultimo_perro = tiempo_actual

    # Movimiento de los perros persiguiendo al repartidor
    for perro_actual in perros:
        dx = repartidor_x - perro_actual[0]
        dy = repartidor_y - perro_actual[1]
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia > 0:
            perro_actual[0] += (dx / distancia) * velocidad_perro
            perro_actual[1] += (dy / distancia) * velocidad_perro

    # Lanzar una pizza cada 3 segundos hacia el perro más cercano
    if tiempo_actual - tiempo_ultima_pizza >= intervalo_pizza:
        lanzar_pizza()
        tiempo_ultima_pizza = tiempo_actual

    # Movimiento de pizzas
    for pizza_actual in pizzas:
        pizza_actual[0] += pizza_actual[2]
        pizza_actual[1] += pizza_actual[3]

    # Limpiar pizzas fuera de pantalla
    pizzas = [
        pizza_actual
        for pizza_actual in pizzas
        if -32 <= pizza_actual[0] <= 800 and -32 <= pizza_actual[1] <= 600
    ]

    # Llamar a la función de colisiones antes de dibujar
    detectar_colisiones()

    # 3. DIBUJO EN PANTALLA
    pantalla.blit(fondo, (0, 0))

    invulnerable = tiempo_actual - tiempo_ultimo_golpe < duracion_invulnerabilidad

    # El repartidor solo se dibuja si no es invulnerable, O si lo es, hace el efecto intermitente (titilar)
    if not invulnerable or (tiempo_actual // 150) % 2 == 0:
        repartir(repartidor_x, repartidor_y)

    for perro_actual in perros:
        perro(perro_actual[0], perro_actual[1])

    for pizza_actual in pizzas:
        dibujar_pizza(pizza_actual[0], pizza_actual[1])

    dibujar_vidas()

    pygame.display.update()

    # Controlar que el juego corra a 60 cuadros por segundo
    reloj.tick(60)

pygame.quit()