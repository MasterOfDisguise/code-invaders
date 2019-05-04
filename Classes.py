__author__ = 'Administrator'
from config import *


class Ship(pygame.sprite.Sprite):

    def __init__(self, manager):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.image = pygame.image.load("ship_1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = width/2
        self.rect.y = height*9/10
        self.vx = 0
        self.vy = 0
        self.dead = False

    def key_events(self, event):
            if event.key == pygame.K_LEFT:
                self.vx = -2
            if event.key == pygame.K_RIGHT:
                self.vx = 2
            if event.key == pygame.K_UP:
                self.vy = -2
            if event.key == pygame.K_DOWN:
                self.vy = 2
            if event.key == pygame.K_SPACE:
                self.fire()

    def stop_moving(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            self.vx = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            self.vy = 0

    def fire(self):
        if len(self.manager.screen.bullets) < 1 and not self.dead:
            bullet = Bullet(self.rect.x, self.rect.y)
            self.manager.screen.add_bullet(bullet)

    def draw(self):
            self.manager.surface.blit(self.image, self.rect)

    def move(self):
        if not self.dead:
            self.rect.x += self.vx
            self.rect.y += self.vy
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > height:
                self.rect.bottom = height
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.right > width:
                self.rect.right = width

    def die(self):
        self.manager.screen.enemy_bullets.empty()
        self.dead = True
        self.manager.lives -= 1
        self.vx = 0
        self.vy = 0
        self.image = pygame.image.load("ship_1_death.png").convert()
        if self.manager.lives > 0:
            threading.Timer(1.0, self.resurrect).start()
        else:
            threading.Timer(1.0, self.manager.game_over).start()

    def resurrect(self):
        self.dead = False
        self.image = pygame.image.load("ship_1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = width/2
        self.rect.y = height*9/10


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = -8
        self.image = pygame.image.load("bullet_image.PNG").convert()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x + 16

    def off_screen(self):
        if self.rect.y <= -20:
            self.kill()

    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.off_screen()
        self.move()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, manager, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.image = pygame.image.load("enemy1_image.PNG").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fire_interval = random.randint(4000, 7000)
        self.fire_counter = random.randint(0, self.fire_interval)
        self.direction = -10
        self.label = -100
        self.move_interval = 50
        self.move_counter = 0
        self.score_value = 100

    def fire_back(self):
        bullet = EnemyBullet(self.rect.x + 17, self.rect.y + 16)
        self.manager.screen.add_enemy_bullet(bullet)

    def move(self):
        if self.move_counter >= self.move_interval:
            self.rect.x += self.direction
            self.label += self.direction
            self.move_counter = 0
        if self.label == -200 or self.label == 200:
            self.rect.y += 20
            self.direction *= -1
            self.label = 0

    def update(self):
        self.move()
        self.move_counter += 1
        self.fire_counter += 1
        if self.fire_counter == self.fire_interval:
            self.fire_back()
            self.fire_counter = 0
            self.fire_interval = random.randint(400, 700)


class EnemyBullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy_bullet.PNG").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def off_screen(self):
        if self.rect.y >= height+20:
            self.kill()

    def move(self):
        self.rect.y += self.speed

    def update(self):
        self.off_screen()
        self.move()


class Formation(pygame.sprite.Group):

    def __init__(self, manager):
        pygame.sprite.Group.__init__(self)
        self.manager = manager
        self.direction = -1
        self.make_formation()

    def make_enemy(self, x, y):
            alien = Enemy(self.manager, x, y)
            self.add(alien)

    def make_formation(self):
        for i in range(100, width-100, 60):
            for a in range(0, 300, 60):
                self.make_enemy(i, a)


class StartScreen():

    def __init__(self, manager):
        self.manager = manager
        self.text3 = eztext.Input(maxlength=45, color=white, prompt='CODE INVADERS')
        self.text3.set_pos(width/2 - 80, 100)
        self.text = eztext.Input(maxlength=45, color=white, prompt='use arrow keys to move and space to fire')
        self.text.set_pos(width/2 - 200, height/2 - 50)
        self.text2 = eztext.Input(maxlength=45, color=white, prompt='press space to start')
        self.text2.set_pos(width/2 - 100, height/2 + 100)

    def draw(self):
        self.text3.draw(self.manager.surface)
        self.text.draw(self.manager.surface)
        self.text2.draw(self.manager.surface)

    def key_events(self, event):
        if event.key == pygame.K_SPACE:
            self.manager.start_game()

    def stop_moving(self, event):
        pass

    def update(self):
        pass


class GameScreen():

    def __init__(self, manager):
        self.manager = manager
        self.score = eztext.Input(maxlength=45, color=white, prompt='score: ' + str(self.manager.score))
        self.life_counter = eztext.Input(maxlength=45, color=white, prompt='lives:' + str(self.manager.lives))
        self.life_counter.set_pos(639, 0)
        self.ship = Ship(self.manager)
        self.bullets = pygame.sprite.Group()
        self.formation = Formation(self.manager)
        self.enemy_bullets = pygame.sprite.Group()
        # self.lives = Lives(self.manager)


    def draw(self):
        self.bullets.draw(self.manager.surface)
        self.ship.draw()
        self.formation.draw(self.manager.surface)
        self.enemy_bullets.draw(self.manager.surface)
        self.score.draw(self.manager.surface)
        self.life_counter.draw(self.manager.surface)
        # self.lives.draw(self.manager.surface)


    def add_bullet(self, thing):
        self.bullets.add(thing)

    def add_enemy_bullet(self, thing):
        self.enemy_bullets.add(thing)

    def key_events(self, event):
        self.ship.key_events(event)

    def stop_moving(self, event):
        self.ship.stop_moving(event)

    def update(self):
        self.ship.move()
        self.bullets.update()
        self.enemy_bullets.update()
        self.formation.update()

        for enemy in self.formation:
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(bullet, enemy):
                    bullet.kill()
                    enemy.kill()
                    self.manager.score += enemy.score_value
                    self.score = eztext.Input(maxlength=45, color=white, prompt='score: ' + str(self.manager.score))

        for bullet in self.enemy_bullets:
            if pygame.sprite.collide_rect(bullet, self.ship):
                bullet.kill()
                self.ship.die()
                self.life_counter = eztext.Input(maxlength=45, color=white, prompt='lives:' + str(self.manager.lives))
                self.life_counter.set_pos(639, 0)

        for alien in self.formation:
            if pygame.sprite.collide_rect(alien, self.ship):
                alien.kill()
                self.ship.die()
                self.life_counter = eztext.Input(maxlength=45, color=white, prompt='lives:' + str(self.manager.lives))
                self.life_counter.set_pos(639, 0)

        if len(self.formation) == 0:
            threading.Timer(1.0, self.formation.make_formation())
            self.manager.lives += 1


class GameOverScreen():

    def __init__(self, manager):
        self.manager = manager
        self.text = eztext.Input(maxlength=45, color=white, prompt='GAME OVER')
        self.text.set_pos(width/2 - 80, 100)
        self.text2 = eztext.Input(maxlength=45, color=white, prompt='enter initials:')
        self.text2.set_pos(width/2 - 100, height/2)
        self.text3 = eztext.Input(maxlength=3, color=white, prompt='')
        self.text3.set_pos(width/2 + 60, height/2)

    def draw(self):
        self.text.draw(self.manager.surface)
        self.text2.draw(self.manager.surface)
        self.text3.draw(self.manager.surface)

    def key_events(self, event):
        self.text3.update(event)
        if event.key == pygame.K_RETURN:
            initials = self.text3.value
            f = open('HighScores', 'r')
            my_scores = json.load(f)

            score = [initials, self.manager.score]
            my_scores.append(score)
            my_scores.sort(reverse=True)
            f.close()

            f = open('HighScores', 'w')
            json.dump(my_scores, f)
            f.close()
            sys.exit()

    def stop_moving(self, event):
        pass

    def update(self):
        pass


class Manager:

    def __init__(self, surface):
        self.surface = surface
        self.screen = StartScreen(self)
        level = 1
        self.score = 0
        self.lives = 3

    def draw(self):
        self.screen.draw()

    def update(self):
        self.screen.update()

    def key_events(self, event):
        self.screen.key_events(event)

    def stop_moving(self, event):
        self.screen.stop_moving(event)

    def start_game(self):
        self.screen = GameScreen(self)

    def game_over(self):
        self.screen = GameOverScreen(self)
