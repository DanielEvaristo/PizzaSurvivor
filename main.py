import pygame

#Inicializar pygame
pygame.init()

#Crear pantalla de juego
pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pizza Survivor")
icono = pygame.image.load("pizza.png")
pygame.display.set_icon(icono)

#Fondo de juego
fondo = pygame.image.load("fondo.png")
fondo = pygame.transform.scale(fondo,(800,600))


#Bucle principal del juego
se_ejecuta = True
while se_ejecuta:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        pantalla.blit(fondo,(0,0))
        pygame.display.update()

pygame.quit()
