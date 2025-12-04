import pygame
import random
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 255, 0)
INVADER_COLOR = (255, 0, 0)
BULLET_COLOR = (0, 0, 255)


class Bullet:
    def __init__(self, position, velocity):
        self.size = {'width': 3, 'height': 3}
        self.position = dict(position)
        self.velocity = dict(velocity)

    def update(self):
        self.position['x'] += self.velocity['x']
        self.position['y'] += self.velocity['y']


class Invader:
    def __init__(self, game, position):
        self.game = game
        self.size = {'width': 16, 'height': 16}
        self.position = dict(position)
        self.patrolX = 0
        self.speedX = 1

    def update(self):
        if self.patrolX < 0 or self.patrolX > 500:
            self.speedX = -self.speedX
        self.position['x'] += self.speedX
        self.patrolX += self.speedX

        if random.random() < 0.02 and not self.game.invaders_below(self):
            bullet = Bullet(
                {'x': self.position['x'] + self.size['width'] / 2 - 1.5,
                 'y': self.position['y'] + self.size['height']},
                {'x': random.random() - 0.5, 'y': 2}
            )
            self.game.add_body(bullet)


class Player:
    def __init__(self, game, game_size):
        self.game = game
        self.bullets = 0
        self.timer = 0
        self.size = {'width': 16, 'height': 16}
        self.position = {
            'x': game_size['x'] / 2 - self.size['width'] / 2,
            'y': game_size['y'] - self.size['height'] - 20
        }

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.position['x'] = max(0, self.position['x'] - 2)
        if keys[pygame.K_RIGHT]:
            self.position['x'] = min(self.game.game_size['x'] - self.size['width'],
                                     self.position['x'] + 2)
        if keys[pygame.K_SPACE] and self.bullets < 5:
            bullet = Bullet(
                {'x': self.position['x'] + self.size['width'] / 2 - 1.5,
                 'y': self.position['y'] - 4},
                {'x': 0, 'y': -6}
            )
            self.game.add_body(bullet)
            self.bullets += 1

        self.timer += 1
        if self.timer % 12 == 0:
            self.bullets = 0


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.game_size = {'x': SCREEN_WIDTH, 'y': SCREEN_HEIGHT}
        self.bodies = self.create_invaders()
        self.player = Player(self, self.game_size)
        self.bodies.append(self.player)
        self.clock = pygame.time.Clock()

    def add_body(self, body):
        self.bodies.append(body)

    def create_invaders(self):
        return [Invader(self, {'x': 30 + (i % 8) * 30, 'y': 30 + (i % 3) * 30})
                for i in range(24)]

    def colliding(self, b1, b2):
        if b1 is b2:
            return False
        return not (
            b1.position['x'] + b1.size['width'] < b2.position['x'] or
            b1.position['y'] + b1.size['height'] < b2.position['y'] or
            b1.position['x'] > b2.position['x'] + b2.size['width'] or
            b1.position['y'] > b2.position['y'] + b2.size['height']
        )

    def invaders_below(self, invader):
        return any(isinstance(b, Invader) and
                   b.position['y'] > invader.position['y'] and
                   abs(b.position['x'] - invader.position['x']) < invader.size['width']
                   for b in self.bodies)

    def update(self):
        self.bodies = [b for b in self.bodies
                       if all(not self.colliding(b, other) for other in self.bodies if b is not other)]
        self.bodies = [b for b in self.bodies if 0 <= b.position['y'] <= self.game_size['y']]
        for body in self.bodies:
            body.update()

    def draw_body(self, body, color):
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(int(body.position['x']), int(body.position['y']),
                                     int(body.size['width']), int(body.size['height'])))

    def draw(self):
        self.screen.fill(WHITE)
        for body in self.bodies:
            if isinstance(body, Player):
                self.draw_body(body, PLAYER_COLOR)
            elif isinstance(body, Invader):
                self.draw_body(body, INVADER_COLOR)
            elif isinstance(body, Bullet):
                self.draw_body(body, BULLET_COLOR)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders (Python)")
    Game(screen).run()


if __name__ == "__main__":
    main()

