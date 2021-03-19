import random
import pygame
import tkinter as tk
from tkinter import messagebox


class cube(object):
    rows = 25
    w = 800

    def __init__(self, start, dirX=1, dirY=0, color=(128, 255, 0)):
        self.pos = start
        self.dirY = dirY
        self.dirX = dirX
        self.color = color

    def move(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.pos = (self.pos[0] + self.dirX, self.pos[1] + self.dirY)

    def draw(self, win, eyes=False):
        space = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(win, self.color, (i * space + 1, j * space + 1, space - 2, space - 2)) #we use -2 to see grids
        if eyes:
            centre = space // 2
            radius = 3
            circleMiddle = (i * space + centre - radius, j * space + 8)
            circleMiddle2 = (i * space + space - radius * 2, j * space + 8)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(win, (0, 0, 0), circleMiddle2, radius)

class snake(object):
    snakeBody = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.snakeBody.append(self.head)
        self.dirX = 0
        self.dirY = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirX = -1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY] #note last turn

                elif keys[pygame.K_UP]:
                    self.dirX = 0
                    self.dirY = -1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_RIGHT]:
                    self.dirX = 1
                    self.dirY = 0
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

                elif keys[pygame.K_DOWN]:
                    self.dirX = 0
                    self.dirY = 1
                    self.turns[self.head.pos[:]] = [self.dirX, self.dirY]

        for i, c in enumerate(self.snakeBody):
            p = c.pos[:] #taking position of cube
            if p in self.turns: #check if that position is in turn list
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.snakeBody) - 1:
                    self.turns.pop(p)
            else:
                if c.dirX == -1 and c.pos[0] <= 0: #check if we left window to the left
                    c.pos = (c.rows - 1, c.pos[1]) #reposition to the right
                elif c.dirX == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirY == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirX, c.dirY)

    def reset(self, pos):
        self.head = cube(pos)
        self.snakeBody = []
        self.snakeBody.append(self.head)
        self.turns = {}
        self.dirX = 0
        self.dirY = 1

    def addCube(self):
        tail = self.snakeBody[-1]
        dx, dy = tail.dirX, tail.dirY

        if dx == 1 and dy == 0:
            self.snakeBody.append(cube((tail.pos[0] - 1, tail.pos[1]))) #adding cube to the tail using + bcs its moving on the right
        elif dx == -1 and dy == 0:
            self.snakeBody.append(cube((tail.pos[0] + 1, tail.pos[1]))) #adding cube to the tail using + bcs its moving on the left
        elif dx == 0 and dy == 1:
            self.snakeBody.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.snakeBody.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.snakeBody[-1].dirX = dx
        self.snakeBody[-1].dirY = dy

    def draw(self, win):
        for i, c in enumerate(self.snakeBody):
            if i == 0:
                c.draw(win, True)
            else:
                c.draw(win)


def drawGrid(width, rows, win):
    sizeBtwn = width // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))


def drawWindow(win):
    global rows, width, s, snack
    win.fill((102,102,0))
    s.draw(win)
    snack.draw(win)
    drawGrid(width, rows, win)
    pygame.display.update()


def food(rows, item):
    positions = item.snakeBody

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0: #we check if position of food is on the snake
            continue #we do random x,y again if it is true
        else:
            break

    return (x, y)


def message_box(subject, message):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, message)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 800
    rows = 25
    win = pygame.display.set_mode((width, width))
    s = snake(( 128, 255, 0), (12, 12))
    snack = cube(food(rows, s), color=(102, 51, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(100)
        clock.tick(15)
        s.move()
        if s.snakeBody[0].pos == snack.pos:
            s.addCube()
            snack = cube(food(rows, s), color=(102, 51, 0))

        for x in range(len(s.snakeBody)):
            if s.snakeBody[x].pos in list(map(lambda z: z.pos, s.snakeBody[x + 1:])): #check for collision
                print('Score: ', len(s.snakeBody))
                message_box('You lost!', 'Play again...')
                s.reset((10, 10))
                break

        drawWindow(win)

    pass

main()