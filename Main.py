import random
import pickle

from core.Interface import *
from core.Settings import *
from core.Entity import *
from core.Map import *


def save(matrix): # Сохраняем
    with open('save/save.save', 'wb') as f:
        pickle.dump(matrix, f)


def load(): # Загружаем
    with open('save/save.save', 'rb') as f:
        loaded_matrix = pickle.load(f)
    return loaded_matrix


def new_map(): # Создает новое чистое поле и расставляет ботов
    map = Map(213, 125)
    for y in range(map.size[1]):
        for x in range(map.size[0]):
            if random.random() <= 0.05:
                entity = Entity(x, y)
                map.map[y][x] = entity
    return map


pygame.init()
pygame.font.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])

icon = pygame.image.load('gfx/1.ico')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
clock = pygame.time.Clock()
front = pygame.font.Font('gfx/ProggyClean.ttf', 30)
map = new_map()

running = True
paused = False # Просчет итерации
iteration = 0
copy_entity = None # Копия бота
old_age = True # Смерть от старости
rendering = True # Отрисовка
rendering_mode = 0 # Режим отрисовки


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
                iteration = 0
                print('Мир пересоздан')
            elif event.key == pygame.K_c: # Включить/выключить смерть от старости
                old_age = not(old_age)
                print('Смерть от старости:', old_age)
            elif event.key == pygame.K_x: # Включить/выключить отрисовку
                rendering = not(rendering)
                print('Отрисовка:', rendering)
            elif event.key == pygame.K_s: # Сохранение мира 
                save(map)
                print('Мир сохранен')
            elif event.key == pygame.K_l: # Загрузка мира
                map = load()
                print('Мир загружен')
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS: # Увеличение просчета за одну итерацию
                NUMBER_OF_ITERATIONS_PER_DRAWING += 1
                print('Увеличено итераций за одну отрисовку:', NUMBER_OF_ITERATIONS_PER_DRAWING)
            elif event.key == pygame.K_MINUS: # Уменьшено просчета за одну итерацию
                if NUMBER_OF_ITERATIONS_PER_DRAWING != 1:
                    NUMBER_OF_ITERATIONS_PER_DRAWING -= 1
                    print('Уменьшено итераций за одну отрисовку:', NUMBER_OF_ITERATIONS_PER_DRAWING)

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

    entities_to_process1 = [] # Потоки
    # entities_to_process2 = []
    # entities_to_process3 = []
    # entities_to_process4 = []

    for i in range(NUMBER_OF_ITERATIONS_PER_DRAWING):
        for y in range(map.size[1]):
            for x in range(map.size[0]):
                cell = map.get_cor_map(x, y)
                if cell != None and isinstance(cell, Entity):
                    if not(paused): # Добавляем сущность в список действий
                        entities_to_process1.append((x, y, cell))
                        # if x < 2 and y < 2:
                        #     entities_to_process1.append((x, y, cell))
                        # elif x < 2 and y > 2:
                        #     entities_to_process2.append((x, y, cell))
                        # elif x > 2 and y > 2:
                        #     entities_to_process3.append((x, y, cell))
                        # else:
                        #     entities_to_process4.append((x, y, cell))

                    if rendering and pygame.display.get_active() and i == 0: # Отрисовка
                        DrawEntity(screen, cell.color, BORDER, cell.x, cell.y, SIZE, cell.rotation)

        if not paused: # Просчет мозгов
            iteration += 1
            
            Entity_processing_function(map, entities_to_process1, old_age)

            entity_count = sum(1 for y in range(map.size[1]) for x in range(map.size[0]) if isinstance(map.get_cor_map(x, y), Entity))
            print('Количество сущностей:', entity_count, 'Итераций: ', iteration)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
