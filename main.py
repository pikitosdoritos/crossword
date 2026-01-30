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
    vert_hint = ""
    hor_hint = ""
    for item in board:
        word = item["word"]
        x0, y0 = item["x"], item["y"]
        
        for i in range(len(word)):
            dx = i if item["direction"] == "right" else 0
            dy = i if item["direction"] == "down" else 0
            
            if ((y0 + dy, x0 + dx) == (row, col)):
                if item["direction"] == "right":
                    hor_hint = item["hint"]
                elif item["direction"] == "down":
                    vert_hint = item["hint"]
                
    if vert_hint and hor_hint:
        return f"→: {hor_hint}\n↓: {vert_hint}"
        
    elif vert_hint:
        return vert_hint
        
    elif hor_hint:
        return hor_hint
    
    else:
        return None

def show_hint(screen, text, x, y, font):
    padding = 6
    line_gap = 2
    
    lines = text.split("\n")
    
    rendered = [font.render(line, True, (0, 0, 0)) for line in lines]
    
    max_width = max(s.get_width() for s in rendered)
    max_height = sum(s.get_height() for s in rendered) + line_gap * (len(lines) - 1)
    
    rect = pg.Rect(x + 12, y + 12, max_width, max_height)
    
    if x + rect.width + padding > WIDTH:
        rect.x = WIDTH - rect.width - padding
    if y + rect.height + padding > HEIGHT:
        rect.y = HEIGHT - rect.height - padding
    
    bg = rect.inflate(padding * 2, padding * 2)
    pg.draw.rect(screen, (255, 255, 255), bg)
    pg.draw.rect(screen, (100, 100, 100), bg, 1)

    y_offset = rect.y
    for surf in rendered:
        screen.blit(surf, (rect.x, y_offset))
        y_offset += surf.get_height() + line_gap

def calc_cells():
    all_cells = set()
    for item in board:
        item["cells"] = list()
        for i in range(len(item["word"])):
            shift_x = i if item["direction"] == "right" else 0
            shift_y = i if item["direction"] == "down" else 0
            
            coords = (item["x"] + shift_x, item["y"] + shift_y)
            
            item["cells"].append(coords)
            all_cells.add(coords)

calc_cells()
            
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
            
        if e.type == pg.MOUSEBUTTONDOWN:
            click_mx, click_my = e.pos
            active_cell = (click_my // CELL, click_mx // CELL)
            
        if e.type == pg.KEYDOWN and active_cell:
            row, col = active_cell
            
            if e.key == pg.K_BACKSPACE:
                grid[row][col] = None
            
            if e.unicode.isalpha():
                grid[row][col] = e.unicode.upper()
                
    screen.fill((0, 0, 0))

    mx, my = pg.mouse.get_pos()
    col = mx // CELL
    row = my // CELL    
    
    for item in board:
        for i, letter in enumerate(item["word"]):
            x, y = item["cells"][i]
            pg.draw.rect(screen, (255, 255, 255,), (x * CELL, y * CELL, CELL, CELL))
            pg.draw.rect(screen, (0, 0, 0,), (x * CELL, y * CELL, CELL + 1, CELL + 1), 1)
            
    for r in range(ROWS):
        for c in range(COLS):
            letter = grid[r][c]
            if letter:
                x = c * CELL
                y = r * CELL
                text = font.render(letter, True, (0, 0, 0))
                center_text = text.get_rect(center = (x + CELL // 2, y + CELL // 2))
                screen.blit(text, center_text)
            
    if active_cell:
        r, c = active_cell
        pg.draw.rect(screen, (0, 150, 255), (c * CELL, r * CELL, CELL, CELL), 2)
            
    hint = get_hint(row, col, board)
    
    if hint:
        show_hint(screen, hint, mx, my, font_hint)
        
    pg.display.flip()
    clock.tick(60)

pg.quit()