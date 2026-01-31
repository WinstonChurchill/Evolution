import random
from core.Interface import *
from core.Settings import *
from core.Entity import *
from core.Map import *

pygame.init()

icon = pygame.image.load('gfx/1.ico')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

map = Map(150, 100)

for y in range(map.size[1]):
    for x in range(map.size[0]):
        if random.random() <= 0.1:
            entity = Entity(x, y)
            map.map[y][x] = entity

running = True
iteration = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = True
                while paused:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            running = False
                            paused = False
                        elif e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_SPACE:
                                paused = False

    pygame.display.set_caption(f"Evolution Version: {VERSION} Iteration: {iteration} FPS: {int(clock.get_fps())}")
    screen.fill(WHITE)

    entities_to_process = []
    for y in range(map.size[1]):
        for x in range(map.size[0]):
            cell = map.get_cor_map(x, y)
            if cell != '' and isinstance(cell, Entity):
                entities_to_process.append((x, y, cell))

    for x, y, cell in entities_to_process:
        if map.get_cor_map(x, y) != cell:
            continue

        visible_cells = ""
        check_positions = []
        
        if cell.rotation == 0:  # Вверх
            check_positions = [
                ((x - 1) % map.size[0], (y - 1) % map.size[1]),  # Верх-левый
                (x % map.size[0], (y - 1) % map.size[1]),        # Верх
                ((x + 1) % map.size[0], (y - 1) % map.size[1])   # Верх-правый
            ]
        elif cell.rotation == 1:  # Вправо
            check_positions = [
                ((x + 1) % map.size[0], (y - 1) % map.size[1]),  # Правый-верх
                ((x + 1) % map.size[0], y % map.size[1]),        # Правый
                ((x + 1) % map.size[0], (y + 1) % map.size[1])   # Правый-низ
            ]
        elif cell.rotation == 2:  # Вниз
            check_positions = [
                ((x - 1) % map.size[0], (y + 1) % map.size[1]),  # Низ-левый
                (x % map.size[0], (y + 1) % map.size[1]),        # Низ
                ((x + 1) % map.size[0], (y + 1) % map.size[1])   # Низ-правый
            ]
        elif cell.rotation == 3:  # Влево
            check_positions = [
                ((x - 1) % map.size[0], (y - 1) % map.size[1]),  # Левый-верх
                ((x - 1) % map.size[0], y % map.size[1]),        # Левый
                ((x - 1) % map.size[0], (y + 1) % map.size[1])   # Левый-низ
            ]
        
        for cx, cy in check_positions: # Глаза
            visible_cells += "1" if map.get_cor_map(cx, cy) != '' else "0"
        
        object_input = float(f'0.{visible_cells}')
        action = cell.brain(iteration, object_input, map.size)
        
        if action == 0:  # Движение
            old_x, old_y = cell.x, cell.y
            new_x, new_y = old_x, old_y
            
            if cell.rotation == 0:  # Вверх
                new_y = (old_y - 1) % map.size[1]
            elif cell.rotation == 1:  # Вправо
                new_x = (old_x + 1) % map.size[0]
            elif cell.rotation == 2:  # Вниз
                new_y = (old_y + 1) % map.size[1]
            elif cell.rotation == 3:  # Влево
                new_x = (old_x - 1) % map.size[0]
            
            target_cell = map.get_cor_map(new_x, new_y)
            if target_cell == '':
                map.move(old_x, old_y, new_x, new_y)
                cell.energy = max(0, cell.energy - 1)
            else:
                cell.energy = max(0, cell.energy - 1)
        
        elif action == 1:  # Фотосинтез
            brightness = ((x + y) // 5) % 10  # Циклический паттерн
            cell.energy = min(MAX_ENERGY, cell.energy + 2 + brightness)
        
        elif action == 2:  # Размножение
            if cell.can_reproduce():
                directions = [
                    (-1, -1), (0, -1), (1, -1),   # Верхний ряд
                    (-1, 0),           (1, 0),    # По бокам (без текущей позиции)
                    (-1, 1),  (0, 1),  (1, 1)     # Нижний ряд
                ]
                
                for dx, dy in directions:
                    child_x = (cell.x + dx) % map.size[0]
                    child_y = (cell.y + dy) % map.size[1]
                    
                    if map.get_cor_map(child_x, child_y) == '':
                        child = cell.reproduce(child_x, child_y)
                        map.map[child_y][child_x] = child
                        break
        
        elif action == 3:  # поворот
            cell.rotation = (cell.rotation + 1) % 4
            cell.energy -= 1
        
        elif action == 4:  # атака или питание, если растение
            target_x, target_y = cell.x, cell.y
            
            if cell.rotation == 0:  # Вверх
                target_y = (cell.y - 1) % map.size[1]
            elif cell.rotation == 1:  # Вправо
                target_x = (cell.x + 1) % map.size[0]
            elif cell.rotation == 2:  # Вниз
                target_y = (cell.y + 1) % map.size[1]
            elif cell.rotation == 3:  # Влево
                target_x = (cell.x - 1) % map.size[0]
            
            target_cell = map.get_cor_map(target_x, target_y)
            if isinstance(target_cell, Entity):
                cell.energy = min(MAX_ENERGY, cell.energy + target_cell.energy // 2)
                map.map[target_y][target_x] = ''
                cell.energy = max(0, cell.energy - 2)
        
        if cell.energy <= 0:
            map.map[y][x] = ''

    for y in range(map.size[1]):
        for x in range(map.size[0]):
            cell = map.get_cor_map(x, y)
            if cell != '' and isinstance(cell, Entity):
                DrawEntity(screen, cell.color, BORDER, cell.x, cell.y, SIZE, cell.rotation)

    entity_count = sum(1 for y in range(map.size[1]) for x in range(map.size[0])  if isinstance(map.get_cor_map(x, y), Entity))
    print('Количество сущностей:', entity_count)

    pygame.display.update()
    clock.tick(30)
    
    iteration += 1

pygame.quit()
