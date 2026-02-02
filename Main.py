import random

from core.Interface import *
from core.Settings import *
from core.Entity import *
from core.Map import *


def new_map(): # Создает новое чистое поле и расставляет ботов
    map = Map(162, 125)
    for y in range(map.size[1]):
        for x in range(map.size[0]):
            if random.random() <= 0.05:
                entity = Entity(x, y)
                map.map[y][x] = entity
    return map


def gen(w1_list, w2_list): # процентное различие сущностей
    total_diff = 0
    total_elements = 0
    
    for w1, w2 in zip(w1_list, w2_list):
        total_diff += np.sum(np.abs(w1 - w2))
        total_elements += w1.size
    
    avg_abs_diff = total_diff / total_elements
    
    max_possible_diff = 2.0  # от -1 до 1 = разница 2
    percentage = (avg_abs_diff / max_possible_diff)
    
    return percentage + 0.0001



pygame.init()
pygame.font.init()

icon = pygame.image.load('gfx/1.ico')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
front = pygame.font.Font('gfx/ProggyClean.ttf', 30)
map = new_map()

running = True
paused = False # Просчет итерации
iteration = 0
copy_entity = None # Копия бота
old_age = True # Смерть от старости
rendering = True # Отрисовка


while running:
    for event in pygame.event.get(): # Обработка клавиш
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Поставить на паузу
                paused = not(paused)
                print('Пауза:', paused)
            elif event.key == pygame.K_r: # Пересоздать мир
                map = new_map()
                rendering = True
                print('Мир пересоздан')
            elif event.key == pygame.K_c: # Включить/выключить смерть от старости
                old_age = not(old_age)
                print('Смерть от старости:', old_age)
            elif event.key == pygame.K_x: # Включить/выключить отрисовку
                rendering = not(rendering)
                print('Отрисовка:', rendering)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] < map.size_window[0] and event.pos[1] < map.size_window[1]:
                cell_x = event.pos[0] // SIZE
                cell_y = event.pos[1] // SIZE
                print(cell_x, cell_y)
                
                if event.button == 1 and rendering:  # ЛКМ - копирование
                    a = map.get_cor_map(cell_x, cell_y)
                    if a is not None and isinstance(a, Entity):
                        copy_entity = Entity(a.x, a.y, a.energy, a.color, a.rotation, a.brain_weights.copy())
                        print(a)

                elif event.button == 3 and rendering:  # ПКМ - вставка
                    if map.get_cor_map(cell_x, cell_y) is None and copy_entity is not None:
                        map.map[cell_y][cell_x] = Entity(cell_x, cell_y, copy_entity.energy, copy_entity.color, copy_entity.rotation, copy_entity.brain_weights.copy())
                        print(f"Вставлена сущность {cell_x} {cell_y}")


    pygame.display.set_caption(f"Evolution Version: {VERSION} Iteration: {iteration} FPS: {int(clock.get_fps())}")

    if rendering: # Отрисовка
        screen.fill(WHITE)
        for y in range(map.size[1]):
            for x in range(map.size[0]):
                cell = map.get_cor_map(x, y)
                if cell != None and isinstance(cell, Entity):
                    DrawEntity(screen, cell.color, BORDER, cell.x, cell.y, SIZE, cell.rotation)


    if not(paused): # Просчет мозгов
        iteration += 1

        entities_to_process = []
        for y in range(map.size[1]):
            for x in range(map.size[0]):
                cell = map.get_cor_map(x, y)
                if cell != None and isinstance(cell, Entity):
                    entities_to_process.append((x, y, cell))

        for x, y, cell in entities_to_process:
            if map.get_cor_map(x, y) != cell:
                continue

            check_positions = []
            
            if cell.rotation == 0:  # Вверх
                check_positions = [
                    ((x - 1) % map.size[0], (y - 1) % map.size[1]),  # Верх-левый
                    (x % map.size[0], (y - 1) % map.size[1]),        # Верх
                    ((x + 1) % map.size[0], (y - 1) % map.size[1])   # Верх-правый
                ]
                look_position = (x % map.size[0], (y - 1) % map.size[1])
            elif cell.rotation == 1:  # Вправо
                check_positions = [
                    ((x + 1) % map.size[0], (y - 1) % map.size[1]),  # Правый-верх
                    ((x + 1) % map.size[0], y % map.size[1]),        # Правый
                    ((x + 1) % map.size[0], (y + 1) % map.size[1])   # Правый-низ
                ]
                look_position = ((x + 1) % map.size[0], y % map.size[1])
            elif cell.rotation == 2:  # Вниз
                check_positions = [
                    ((x - 1) % map.size[0], (y + 1) % map.size[1]),  # Низ-левый
                    (x % map.size[0], (y + 1) % map.size[1]),        # Низ
                    ((x + 1) % map.size[0], (y + 1) % map.size[1])   # Низ-правый
                ]
                look_position = (x % map.size[0], (y + 1) % map.size[1])
            elif cell.rotation == 3:  # Влево
                check_positions = [
                    ((x - 1) % map.size[0], (y - 1) % map.size[1]),  # Левый-верх
                    ((x - 1) % map.size[0], y % map.size[1]),        # Левый
                    ((x - 1) % map.size[0], (y + 1) % map.size[1])   # Левый-низ
                ]
                look_position = ((x - 1) % map.size[0], y % map.size[1])
            
            visible_cells = ""
            for cx, cy in check_positions: # Взгляд
                visible_cells += "1" if map.get_cor_map(cx, cy) != None else "0"
            
            object_input = float(f'0.{visible_cells}')

                        # Изменяем получение brain_look:
            if look_position is not None: # Проверяем перед сущностью, сущность
                front_cell = map.get_cor_map(look_position[0], look_position[1])
                if front_cell is not None and hasattr(front_cell, 'brain_weights'):
                    # Вычисляем различие весов через функцию gen
                    brain_look = gen(cell.brain_weights, front_cell.brain_weights)
                else:
                    brain_look = 0
            else:
                brain_look = 0

            action = cell.brain(brain_look, object_input) # Итерация ИИ
            
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
                if target_cell == None:
                    map.move(old_x, old_y, new_x, new_y)
                    cell.energy = max(0, cell.energy - 1)
                else:
                    cell.energy = max(0, cell.energy - 1)
            
            elif action == 1:  # Фотосинтез
                brightness =  ((x + y) // 5) % 10  # Циклический паттерн
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
                        
                        if map.get_cor_map(child_x, child_y) == None:
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
                    cell.energy = min(MAX_ENERGY, cell.energy + int(target_cell.energy * 0.1)) # Правило 10%
                    map.map[target_y][target_x] = None
                    cell.energy = max(0, cell.energy - 2)
            

            if cell.energy <= 0: # Смерть от истощения
                map.map[y][x] = None

            if old_age: # Смерть от старости
                if random.randint(0, 100) < cell.age // 10:
                    map.map[y][x] = None


        entity_count = sum(1 for y in range(map.size[1]) for x in range(map.size[0]) if isinstance(map.get_cor_map(x, y), Entity))
        print('Количество сущностей:', entity_count, 'Итераций: ', iteration)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()
