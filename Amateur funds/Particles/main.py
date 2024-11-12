import pygame, sys, random
clock = pygame.time.Clock()
from pygame import *

pygame.init()
WINDOW_SIZE = (800, 400)

pygame.display.set_caption("Particles demo")
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

#particularly, particles :D
# [loc, vel, timer]

particles = []
color = [(219, 209, 20), (219, 126, 20), (219, 20, 23), (20, 149, 219)]

while True:
    mx, my = pygame.mouse.get_pos()
    particles.append([[mx, my], [random.randint(-20, 40) / 10 - 1, -2], random.randint(6,8)])
    screen.fill((0,0,0))

    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1 # if you increase this you can get something like an explosion, but still you may need to tweak this in the actaul game :)
        pygame.draw.circle(screen, random.choice(color), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        particle[1][1] -= 0.5
        if particle[2] <= random.randint(0,4):
            particles.remove(particle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(45)