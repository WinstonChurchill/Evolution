import numpy as np
import random

from core.Settings import config, colors

class Entity:
    def __init__(self, x, y, energy = None, color = None, rotation = None, brain_weights = None, parent_weights = None):
        """
        Создание сущности (бота)
        :param x, y: координаты на карте
        :param energy: энергия сущности
        :param color: цвет (RGB)
        :param rotation: направление (0 вверх, 1 вправо, 2 вниз, 3 влево)
        :param brain_weights: веса нейросети
        :param parent_weights: веса родителя (для наследования)
        """
        self.energy = energy or config.MAX_ENERGY
        self.x = x
        self.y = y
        self.age = 0
        self.color = color or colors.GREEN
        self.type = 0  # тип сущности (0 - обычный бот)

        # Направление (0 вверх, 1 вправо, 2 вниз, 3 влево)
        if rotation is not None:
            self.rotation = rotation
        else:
            self.rotation = random.randint(0, 3)

        # Инициализация весов мозга
        if brain_weights is not None:
            self.brain_weights = brain_weights
        elif parent_weights is not None:
            # Мутация при наследовании
            if random.random() < config.CHANCE_OF_MUTATION:
                self.brain_weights = []
                for weight in parent_weights:
                    mutation = np.random.normal(0, config.MUTATION_COEFFICIENT, weight.shape)  # Изменяем каждый вес
                    self.brain_weights.append(weight + mutation)
            else:
                self.brain_weights = parent_weights
        else:
            # Случайная инициализация (Xavier initialization)
            self.brain_weights = [
                np.random.randn(7, 16) * np.sqrt(2.0 / 6),
                np.random.randn(16, 8) * np.sqrt(2.0 / 16),
                np.random.randn(8, 6) * np.sqrt(2.0 / 8),
                np.random.randn(6, 5) * np.sqrt(2.0 / 6)
            ]


    def __str__(self):
        return (f'Energy: {self.energy}, Rotation: {self.rotation}, '
                f'XY: {self.x} {self.y}, Color: {self.color}, Age: {self.age}')


    def brain(self, look_brain, object_input):
        """Одна итерация ИИ - обработка входных данных нейросетью"""
        self.age += 1

        # Нормализованные входные данные
        layer = np.array([
            self.energy / config.MAX_ENERGY,  # Сколько энергии у сущности
            self.rotation / 4.0,  # Куда сущность смотрит
            1 / (self.x + 0.0001),  # Координаты (избегаем деления на 0)
            1 / (self.y + 0.0001),
            look_brain,  # Нормализованное процентное различие цветов
            object_input,  # Что видит сущность (битовая маска)
            1 / self.age  # Возраст
        ], dtype=np.float32)

        # Прямое распространение (forward pass) через скрытые слои
        for weights in self.brain_weights[:-1]:
            layer = np.maximum(0, np.dot(layer, weights))  # ReLU активация

        # Выходной слой с сигмоидой
        output = 1 / (1 + np.exp(-np.dot(layer, self.brain_weights[-1])))  # Сигмоида для активации
        action = np.argmax(output)  # Выбираем действие с наибольшей вероятностью

        return action


    def can_reproduce(self):
        """Может ли бот размножиться"""
        return (self.energy >= config.RESTRICTION_ON_REPRODUCTION_ENERGY and 
                self.age // 2 > config.RESTRICTION_ON_REPRODUCTION_AGE)


    def reproduce(self, x, y):
        """Размножение - создание потомка"""
        child_energy = self.energy // 2
        self.energy = self.energy // 2

        # Мутация цвета
        if isinstance(self.color, tuple) and len(self.color) >= 3:
            r, g, b = self.color[0], self.color[1], self.color[2]
            r = max(0, min(255, r + random.randint(-config.MUTATION_COEFFICIENT_COLOR, config.MUTATION_COEFFICIENT_COLOR)))
            g = max(0, min(255, g + random.randint(-config.MUTATION_COEFFICIENT_COLOR, config.MUTATION_COEFFICIENT_COLOR)))
            b = max(0, min(255, b + random.randint(-config.MUTATION_COEFFICIENT_COLOR, config.MUTATION_COEFFICIENT_COLOR)))
            child_color = (r, g, b)
        else:
            child_color = self.color

        # Создаем потомка с мутировавшими весами
        child = Entity(x, y, energy=child_energy, color=child_color, parent_weights=self.brain_weights)
        return child


def calculate_color_difference(color1, color2):
    """Процентное различие между двумя цветами (для взгляда бота)"""
    return np.sqrt(np.power(color1[0] - color2[0], 2) + 
                   np.power(color1[1] - color2[1], 2) + 
                   np.power(color1[2] - color2[2], 2)) / 441.67  # Максимальное возможное расстояние


def Entity_processing_function(world_map, entities_to_process, old_age):
    """Функция обработки всех сущностей на карте"""
    random.shuffle(entities_to_process)  # Случайный порядок для честности
    
    for x, y, cell in entities_to_process:
        # Определяем позиции для обзора в зависимости от направления
        check_positions = []
        
        if cell.rotation == 0:  # Вверх
            check_positions = [
                ((x - 1) % world_map.size[0], (y - 1) % world_map.size[1]),  # Верх-левый
                (x % world_map.size[0], (y - 1) % world_map.size[1]),        # Верх
                ((x + 1) % world_map.size[0], (y - 1) % world_map.size[1])   # Верх-правый
            ]
            look_position = (x % world_map.size[0], (y - 1) % world_map.size[1])
        elif cell.rotation == 1:  # Вправо
            check_positions = [
                ((x + 1) % world_map.size[0], (y - 1) % world_map.size[1]),  # Правый-верх
                ((x + 1) % world_map.size[0], y % world_map.size[1]),        # Правый
                ((x + 1) % world_map.size[0], (y + 1) % world_map.size[1])   # Правый-низ
            ]
            look_position = ((x + 1) % world_map.size[0], y % world_map.size[1])
        elif cell.rotation == 2:  # Вниз
            check_positions = [
                ((x - 1) % world_map.size[0], (y + 1) % world_map.size[1]),  # Низ-левый
                (x % world_map.size[0], (y + 1) % world_map.size[1]),        # Низ
                ((x + 1) % world_map.size[0], (y + 1) % world_map.size[1])   # Низ-правый
            ]
            look_position = (x % world_map.size[0], (y + 1) % world_map.size[1])
        elif cell.rotation == 3:  # Влево
            check_positions = [
                ((x - 1) % world_map.size[0], (y - 1) % world_map.size[1]),  # Левый-верх
                ((x - 1) % world_map.size[0], y % world_map.size[1]),        # Левый
                ((x - 1) % world_map.size[0], (y + 1) % world_map.size[1])   # Левый-низ
            ]
            look_position = ((x - 1) % world_map.size[0], y % world_map.size[1])
        
        # Формируем строку видимости (3 бита - есть ли сущность в каждой из трёх клеток)
        visible_cells = ""
        for cx, cy in check_positions:
            visible_cells += "1" if world_map.get_cor_map(cx, cy) is not None else "0"
        
        object_input = float(f'0.{visible_cells}')  # Преобразуем в число 0.xxx

        # Проверяем, что находится прямо перед сущностью
        if look_position is not None:
            front_cell = world_map.get_cor_map(look_position[0], look_position[1])
            if front_cell is not None:
                brain_look = calculate_color_difference(cell.color, front_cell.color) + 0.0001
            else:
                brain_look = 0
        else:
            brain_look = 0

        # Получаем действие от нейросети
        action = cell.brain(brain_look, object_input)

        # Выполняем действие
        if action == 0:  # Движение
            old_x, old_y = cell.x, cell.y
            new_x, new_y = old_x, old_y
            
            if cell.rotation == 0:  # Вверх
                new_y = (old_y - 1) % world_map.size[1]
            elif cell.rotation == 1:  # Вправо
                new_x = (old_x + 1) % world_map.size[0]
            elif cell.rotation == 2:  # Вниз
                new_y = (old_y + 1) % world_map.size[1]
            elif cell.rotation == 3:  # Влево
                new_x = (old_x - 1) % world_map.size[0]
            
            target_cell = world_map.get_cor_map(new_x, new_y)
            if target_cell is None:
                world_map.move(old_x, old_y, new_x, new_y)
                cell.energy -= 1
            else:
                cell.energy -= 1

        elif action == 1:  # Фотосинтез
            brightness = 1  # Можно добавить более сложную логику освещения
            cell.energy = min(config.MAX_ENERGY, cell.energy + int(config.PHOTOSYNTHESIS_COEFFICIENT * brightness))

        elif action == 2:  # Размножение
            if cell.can_reproduce():
                # Проверяем все соседние клетки (8 направлений)
                directions = [
                    (-1, -1), (0, -1), (1, -1),   # Верхний ряд
                    (-1, 0),           (1, 0),    # По бокам (без текущей позиции)
                    (-1, 1),  (0, 1),  (1, 1)     # Нижний ряд
                ]
                
                for dx, dy in directions:
                    child_x = (cell.x + dx) % world_map.size[0]
                    child_y = (cell.y + dy) % world_map.size[1]
                    
                    if world_map.get_cor_map(child_x, child_y) is None:
                        child = cell.reproduce(child_x, child_y)
                        world_map.world_map[child_y][child_x] = child
                        break
            else:
                cell.energy -= 5  # Штраф за попытку размножения без ресурсов

        elif action == 3:  # Поворот
            cell.rotation = (cell.rotation + 1) % 4
            cell.energy -= 1

        elif action == 4:  # Атака или питание
            target_x, target_y = cell.x, cell.y
            
            if cell.rotation == 0:  # Вверх
                target_y = (cell.y - 1) % world_map.size[1]
            elif cell.rotation == 1:  # Вправо
                target_x = (cell.x + 1) % world_map.size[0]
            elif cell.rotation == 2:  # Вниз
                target_y = (cell.y + 1) % world_map.size[1]
            elif cell.rotation == 3:  # Влево
                target_x = (cell.x - 1) % world_map.size[0]
            
            target_cell = world_map.get_cor_map(target_x, target_y)
            if isinstance(target_cell, Entity):
                cell.energy = min(config.MAX_ENERGY, cell.energy + int(target_cell.energy * 0.1))  # Правило 10%
                world_map.world_map[target_y][target_x] = None  # Съедаем цель
            else:
                cell.energy -= 2  # Штраф за пустую атаку

        # Проверка на смерть от истощения
        if cell.energy <= 0:
            world_map.world_map[y][x] = None
            continue

        # Проверка на смерть от старости (если включено)
        if random.randint(0, 100) < cell.age // 10 and old_age:
            world_map.world_map[y][x] = None
            continue
