__author__ = 'Administrator'
from config import *
from Classes import Manager

clock = pygame.time.Clock()
game = Manager(screen)
while running:
    screen.fill(black)
    game.draw()
    game.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.KEYDOWN:
            game.key_events(event)
        if event.type == pygame.KEYUP:
            game.stop_moving(event)

    pygame.display.flip()
    clock.tick(50)
