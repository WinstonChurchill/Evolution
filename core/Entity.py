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
            self.brain_weights = [                  # Архитектура: 6 входов → 8 нейронов → 6 нейронов → 5 выходов
                                np.random.uniform(-1, 1, (6, 8)),   # Входной слой (6 нейронов) → Скрытый слой 1 (8 нейронов)
                                np.random.uniform(-1, 1, (8, 6)),   # Скрытый слой 1 → Скрытый слой 2 (6 нейронов)
                                np.random.uniform(-1, 1, (6, 5))]    # Скрытый слой 3 → Выходной слой (5 действий)


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
        self.age += 1

        entrance = np.array([
            self.energy / MAX_ENERGY, # Сколько энергии у сущности
            self.rotation / 4.0, # Куда сущность смотрит
            float(f'0.{self.x}{self.y}'),  # Нормализованное значение координат
            look_brain,  # Нормализовать процентное различие
            object_input, # Что видит сущность
            1 / self.age  # Добавили возраст как 6-й вход
        ], dtype = np.float32)
        
        layer1 = np.maximum(0, np.dot(entrance, self.brain_weights[0]))
        layer2 = np.maximum(0, np.dot(layer1, self.brain_weights[1]))
        output = 1 / (1 + np.exp(-np.dot(layer2, self.brain_weights[2])))
        action = np.argmax(output)

        return action
    

    def can_reproduce(self):
        return self.energy >= RESTRICTION_ON_REPRODUCTION_ENERGY and self.age > RESTRICTION_ON_REPRODUCTION_AGE
    

    def reproduce(self, x, y):
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
    