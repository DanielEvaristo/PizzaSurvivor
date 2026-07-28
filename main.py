import pygame

#Inicializar pygame
pygame.init()

#Crear pantalla de juego
pantalla = pygame.display.set_mode((800,600))


#Bucle principal del juego
se_ejecuta = True
while se_ejecuta:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        pantalla.fill((230,220,240))
        pygame.display.update()

pygame.quit()
