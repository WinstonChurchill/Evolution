from core.Settings import *

import numpy as np
import random

class Entity:
    def __init__(self, x, y, energy = 20, color = GREEN, rotation = None, brain_weights = None, parent_weights = None):
        self.energy = energy
        self.x = x
        self.y = y
        self.age = 0
        self.color = color

        if rotation is not None: # 0 вверх, 1 вправо, 2 вниз, 3 влево
            self.rotation = rotation
        else:
            self.rotation = random.randint(0, 3)

        if brain_weights is not None:
            self.brain_weights = brain_weights
        elif parent_weights is not None:
            if random.random() < CHANCE_OF_MUTATION:
                self.brain_weights = []
                for weight in parent_weights:
                    mutation = np.random.normal(0, MUTATION_COEFFICIENT, weight.shape)  # Изменяем каждый вес
                    self.brain_weights.append(weight + mutation)
            else:
                self.brain_weights = parent_weights
        else:
            self.brain_weights = [
            np.random.randn(6, 16) * np.sqrt(2.0 / 6),
            np.random.randn(16, 8) * np.sqrt(2.0 / 16),
            np.random.randn(8, 6) * np.sqrt(2.0 / 8),
            np.random.randn(6, 5) * np.sqrt(2.0 / 6)
        ]


    def get_color(self):
        all_weights = np.concatenate([w.flatten() for w in self.brain_weights])
        weights_count = len(all_weights)
        
        np.random.seed(42)
        proj_r = np.random.randn(weights_count)
        proj_g = np.random.randn(weights_count)
        proj_b = np.random.randn(weights_count)
        
        weighted_r = np.dot(all_weights, proj_r)
        weighted_g = np.dot(all_weights, proj_g)
        weighted_b = np.dot(all_weights, proj_b)
        
        magic_r = np.tanh(weighted_r / weights_count)
        magic_g = np.tanh(weighted_g / weights_count)
        magic_b = np.tanh(weighted_b / weights_count)
        
        r = int(((magic_r + 1) / 2) * 255)
        g = int(((magic_g + 1) / 2) * 255)
        b = int(((magic_b + 1) / 2) * 255)
        
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        return (r, g, b)


    def __str__(self):
        return f'Energy: {self.energy}, Rotation: {self.rotation}, XY: {self.x} {self.y}, Color: {self.color}, Age: {self.age}, Brain: {self.brain_weights}'


    def brain(self, look_brain, object_input) -> int: # Одна итерация ИИ
        """Одна итерация бота"""
        self.age += 1

        layer = np.array([
            self.energy / MAX_ENERGY, # Сколько энергии у сущности
            self.rotation / 4.0, # Куда сущность смотрит
            float(f'0.{self.x}{self.y}'),  # Нормализованное значение координат
            look_brain,  # Нормализовать процентное различие
            object_input, # Что видит сущность
            1 / self.age  # Возраст
        ], dtype = np.float32)

        for i in self.brain_weights[:-1]:
            layer = np.maximum(0, np.dot(layer, i))

        output = 1 / (1 + np.exp(-np.dot(layer, self.brain_weights[-1]))) # Сигмоида для активации
        action = np.argmax(output)

        return action
    

    def can_reproduce(self):
        """Может, ли бот размножиться"""
        return self.energy >= RESTRICTION_ON_REPRODUCTION_ENERGY and self.age // 2 > RESTRICTION_ON_REPRODUCTION_AGE
    

    def reproduce(self, x, y):
        """Размножение"""
        child_energy = self.energy // 2
        self.energy = self.energy // 2
        
        if isinstance(self.color, tuple) and len(self.color) >= 3:
            r, g, b = self.color[0], self.color[1], self.color[2]
            r = max(0, min(255, r + random.randint(-MUTATION_COEFFICIENT_COLOR, MUTATION_COEFFICIENT_COLOR)))
            g = max(0, min(255, g + random.randint(-MUTATION_COEFFICIENT_COLOR, MUTATION_COEFFICIENT_COLOR)))
            b = max(0, min(255, b + random.randint(-MUTATION_COEFFICIENT_COLOR, MUTATION_COEFFICIENT_COLOR)))
            child_color = (r, g, b)

        child = Entity( # Создаем потомка с другими весами
            x, y,
            energy = child_energy,
            color = child_color,
            parent_weights = self.brain_weights
        )
        
        return child
    

def Entity_processing_function(map, entities_to_process, old_age):
    random.shuffle(entities_to_process)
    for x, y, cell in entities_to_process:
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

        if look_position is not None: # Проверяем перед сущностью, сущность
            front_cell = map.get_cor_map(look_position[0], look_position[1])
            if front_cell is not None:
                brain_look = gen(cell.color, front_cell.color) + 0.0001
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
                cell.energy -= 1
            else:
                cell.energy -= 1
        
        elif action == 1:  # Фотосинтез
            brightness = 1
            # brightness = ((x + y) // 5) % 10  # Циклический паттерн
            # brightness =  0.75 + np.sin(cell.y + cell.x)
            # brightness = ((x / max(1, map.size[0]) + y / max(1, map.size[1])) / 2)
            cell.energy = min(MAX_ENERGY, cell.energy + int(PHOTOSYNTHESIS_COEFFICIENT * brightness))

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
            else:
                cell.energy -= 5

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
            else:
                cell.energy -= 2


        if cell.energy <= 0: # Смерть от истощения
            map.map[y][x] = None
            continue

        if random.randint(0, 100) < cell.age // 10 and old_age: # Смерть от старости
            map.map[y][x] = None
            continue


def gen(color1, color2): # процентное различие сущностей
        return np.sqrt(np.power(color1[0] - color2[0], 2) + np.power(color1[1] - color2[1], 2) + np.power(color1[2] - color2[2], 2)) / 441.67
