import pygame as pg

ROWS, COLS = 10, 10
CELL = 40
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
running = True

board = [
    {"word": "LIST", "x": 1, "y": 1, "direction": "right", "hint": "It`s an ordered, mutable collection of elements."},
    {"word": "INTEGER", "x": 2, "y": 1, "direction": "down", "hint": "It`s a whole number without decimals."},
    {"word": "ARGUMENT", "x": 1, "y": 7, "direction": "right", "hint": "It`s a value passed to a function."},
    {"word": "TUPLE", "x": 4, "y": 1, "direction": "down", "hint": "It`s an ordered, immutable collection of elements."},
    {"word": "LOOP", "x": 4, "y": 4, "direction": "right", "hint": "It repeats a block of code (for, while)."},
    {"word": "PRINT", "x": 7, "y": 4, "direction": "down", "hint": "It`s a function that outputs values to the console."},
]

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
font = pg.font.SysFont("Arial", 20)
font_hint = pg.font.SysFont("Arial", 14)
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
active_cell = None


def get_hint(row, col, board):
    for item in board:
        word = item["word"]
        x0, y0 = item["x"], item["y"]
        
        for i in range(len(word)):
            dx = i if item["direction"] == "right" else 0
            dy = i if item["direction"] == "down" else 0
            
            if ((y0 + dy, x0 + dx) == (row, col)):
                return item["hint"]
    return None

def show_hint(screen, text, x, y, font):
    padding = 6
    txt = font.render(text, True, (0, 0, 0))
    rect = txt.get_rect(topleft=(x + 12, y + 12))
    
    bg = rect.inflate(padding * 2, padding * 2)
    pg.draw.rect(screen, (255, 255, 255), bg)
    pg.draw.rect(screen, (100, 100, 100), bg, 1)

    screen.blit(txt, rect)
    
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
            
    screen.fill((0, 0, 0))

    mx, my = pg.mouse.get_pos()
    col = mx // CELL
    row = my // CELL    
    
    for item in board:
        for i, letter in enumerate(item["word"]):
            shift_x = i * (item["direction"] == "right")
            shift_y = i * (item["direction"] == "down")
            x, y = item["x"] + shift_x, item["y"] + shift_y
            # text = font.render(letter, True, (0, 0, 0))
            # center_text = text.get_rect(center = (x * CELL + CELL // 2, y * CELL + CELL // 2))
            pg.draw.rect(screen, (255, 255, 255,), (x * CELL, y * CELL, CELL, CELL))
            pg.draw.rect(screen, (0, 0, 0,), (x * CELL, y * CELL, CELL + 1, CELL + 1), 1)
            # screen.blit(text, center_text)
            
    hint = get_hint(row, col, board)
    
    if hint:
        show_hint(screen, hint, mx, my, font_hint)
        
    pg.display.flip()
    clock.tick(60)

pg.quit()