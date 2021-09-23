import pygame as pg
from random import choice, randrange
import DBAccessor
import Main


class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_font)
        self.interval = randrange(5, 30)

    def draw(self,):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_font)
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        surface.blit(self.value, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(3, 10)
        self.speed = randrange(3, 7)
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE)]

    def draw(self):
        [symbol.draw() for i, symbol in enumerate(self.symbols)]


RES = WIDTH, HEIGHT = 200, 300
FONT_SIZE = 40

pg.init()
pg.display.set_caption('Библиотека')
screen = pg.display.set_mode(RES)
surface = pg.Surface(RES)
clock = pg.time.Clock()

russian = [chr(int('0x0410', 16) + i) for i in range(66)]
font = pg.font.Font(DBAccessor.base_path + "font\SlimamifMedium.ttf", FONT_SIZE, bold=True)
green_font = [font.render(char, True, (randrange(0, 20), randrange(0, 20), randrange(0, 20))) for char in russian]

symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]

i = 0
while True:
    screen.blit(surface, (0, 0))
    surface.fill(pg.Color('white'))

    for symbol_column in symbol_columns:
        symbol_column.draw()
    i = i + 1
    if i > 200:
        pg.quit()
        Main.LoginForm()

    [exit() for i in pg.event.get() if i.type == pg.QUIT]
    pg.display.flip()
    clock.tick(60)
