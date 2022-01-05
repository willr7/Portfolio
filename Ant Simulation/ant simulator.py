import pygame
import random
import math

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))

RED = (255, 0, 0)
MAROON = (128, 0, 0)

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

HOME = pygame.Rect(WIDTH // 2 - 20, WIDTH // 2 - 20, 40, 40)
FOOD = []
FOOD.append(pygame.Rect(200, 200, 40, 40)) 
FOOD.append(pygame.Rect(400, 200, 40, 40))
FOOD.append(pygame.Rect(200, 400, 40, 40)) 
FOOD.append(pygame.Rect(400, 400, 40, 40))

score = 0

class Ant():
    def __init__(self, speed):
        self.speed = speed

        self.width = 10
        self.height = 10
        self.x = WIDTH // 2 - self.width // 2
        self.y = WIDTH // 2 - self.height // 2

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.xdirection = random.randrange(-2 * 3, 2 * 3)
        self.ydirection = random.randrange(-2 * 3, 2 * 3)
        self.xspeed = math.cos(self.xdirection) * self.speed
        self.yspeed = math.sin(self.ydirection) * self.speed

        self.path = []
        self.path_color = RED

        self.right = 4
        self.left = -4
        self.up = -4
        self.down = 4

        self.targeting = False
        self.target = self
        self.target_order = 0

class Node():
    def __init__(self, pos, color, strength, order):
        self.x, self.y = pos
        self.color = color
        self.strength = strength
        self.active = True
        self.order = order


ANTS = []
for i in range(10):
    ANTS.append(Ant(2))

def move_ant(ant, counter):
    ant.path.sort(key=lambda x: x.color)

    if ant.path_color == GREEN:
        temp = False
        for node in ant.path:
            if node.color == RED and node.active:
                home_x = (HOME.x + HOME.width // 2) - (ant.x + ant.width // 2)
                home_y = (HOME.y + HOME.height // 2) - (ant.y + ant.height // 2)
                x = (node.x + 5) - (ant.x + ant.width // 2)
                y = (node.y + 5) - (ant.y + ant.height // 2)

                theta = math.atan2(y, x)
                home_theta = math.atan2(home_y, home_x)

                if counter % 10:
                    ant.xdirection = theta + random.randrange(0, 10) / 10
                    ant.ydirection = theta + random.randrange(0, 10) / 10

                if ant.rect.colliderect(pygame.Rect(node.x, node.y, 10, 10)):
                    node.active = False
                temp = True
        if not temp:
            x = (HOME.x + HOME.width // 2) - (ant.x + ant.width // 2)
            y = (HOME.y + HOME.height // 2) - (ant.y + ant.height // 2)

            theta = math.atan2(y, x)

            if counter % 10:
                ant.xdirection = theta + random.randrange(0, 10) / 5
                ant.ydirection = theta + random.randrange(0, 10) / 5

    if ant.targeting:
        for node in ant.target.path:
            if ant.rect.colliderect(pygame.Rect(node.x, node.y, 10, 10)):
                if node.color == RED and node.active:
                    home_x = (HOME.x + HOME.width // 2) - (ant.x + ant.width // 2)
                    home_y = (HOME.y + HOME.height // 2) - (ant.y + ant.height // 2)
                    x = (node.x + 5) - (ant.x + ant.width // 2)
                    y = (node.y + 5) - (ant.y + ant.height // 2)

                    theta = math.atan2(y, x)
                    home_theta = math.atan2(home_y, home_x)

                    if counter % 10:
                        ant.xdirection = theta + random.randrange(0, 10) / 10
                        ant.ydirection = theta + random.randrange(0, 10) / 10

                    if ant.rect.colliderect(pygame.Rect(node.x, node.y, 10, 10)):
                        node.active = False
                    temp = True

            if not temp:
                x = (HOME.x + HOME.width // 2) - (ant.x + ant.width // 2)
                y = (HOME.y + HOME.height // 2) - (ant.y + ant.height // 2)

                theta = math.atan2(y, x)

                if counter % 10:
                    ant.xdirection = theta + random.randrange(0, 10) / 5
                    ant.ydirection = theta + random.randrange(0, 10) / 5

    
    if ant.path_color == GREEN and ant.rect.colliderect(HOME):
        ant.path_color = RED
        global score
        score += 1
        ant.down = 4
        ant.up = -4
        ant.left = -4
        ant.right = 4
        print(score)

    if ant.path_color == RED and counter % 3 == 0 and not ant.targeting:
        for ANT in ANTS:
            for i in range(len(ANT.path)):
                if ANT.path[i].color == GREEN and ant.rect.colliderect(pygame.Rect(ANT.path[i].x, ANT.path[i].y, 10, 10)):
                    home_x = (HOME.x + HOME.width // 2) - (ant.x + ant.width // 2)
                    home_y = (HOME.y + HOME.height // 2) - (ant.y + ant.height // 2)
                    x = (ANT.path[i - 1].x + 5) - (ant.x + ant.width // 2)
                    y = (ANT.path[i - 1].y + 5) - (ant.y + ant.height // 2)

                    theta = math.atan2(y, x)

                    ant.xdirection = theta + random.randrange(0, 10) / 10
                    ant.ydirection = theta + random.randrange(0, 10) / 10

        if ant.left == ant.right:
            ant.xdirection += ant.left / 10
        else:
            ant.xdirection += random.randrange(ant.left, ant.right) / 10

        if ant.up == ant.down:
            ant.ydirection += ant.up / 10
        else:
            ant.ydirection += random.randrange(ant.up, ant.down) / 10

    for food in FOOD:
        if ant.rect.colliderect(food):
            ant.path_color = GREEN
    
    ant.xspeed = math.cos(ant.xdirection) * ant.speed
    ant.yspeed = math.sin(ant.ydirection) * ant.speed

    while not (ant.x + ant.xspeed > 0 and ant.x + ant.xspeed + ant.width < WIDTH):
        ant.xdirection += random.randrange(-6, 6) / 10
        ant.xspeed = math.cos(ant.xdirection) * ant.speed
    
    while not (ant.y + ant.yspeed > 0 and ant.y + ant.yspeed + ant.width < WIDTH):
        ant.ydirection += random.randrange(-6, 6) / 10
        ant.yspeed = math.cos(ant.ydirection) * ant.speed

    ant.x += ant.xspeed
    ant.y += ant.yspeed

    ant.rect.x = ant.x
    ant.rect.y = ant.y

def main():
    run = True
    var = 0
    while run:
        pygame.time.Clock().tick(50)
        WIN.fill(WHITE)
        for ant in ANTS:
            if len(ant.path) >= 100:
                ant.path.remove(ant.path[0])
            if var % 8 == 0:
                ant.path.append(Node((ant.x, ant.y), ant.path_color, 0, len(ant.path)))
            move_ant(ant, var)
            ant.path.sort(key=lambda x: x.order)
            # [0, 1, 2,... len(ant.path) - 1]
            # for node in ant.path:
            for i in range(len(ant.path)):
                t_surf = pygame.Surface((10,10))
                t_surf.set_alpha(255 - 255 * (len(ant.path) - i) / len(ant.path))
                t_surf.fill(ant.path[i].color)
                WIN.blit(t_surf, (ant.path[i].x, ant.path[i].y))
                ant.path[i].order -= 1
            pygame.draw.rect(WIN, MAROON, ant)
        for food in FOOD:
            pygame.draw.rect(WIN, GREEN, food)
        pygame.draw.rect(WIN, BLUE, HOME)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        var += 1

if __name__ == "__main__":
    main()