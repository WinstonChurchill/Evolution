from core.Settings import *

import numpy as np
import random

class Entity:
    def __init__(self, x, y, energy = 20, color = GREEN, brain_weights = None, parent_weights = None):
        self.energy = energy
        self.rotation = random.randint(0, 3)  # 0 вверх, 1 вправо, 2 вниз, 3 влево
        self.x = x
        self.y = y
        self.color = color  # Цвет сущности кортеж
        self.age = 0
        
        if brain_weights is not None:
            self.brain_weights = brain_weights
        elif parent_weights is not None:
            self.brain_weights = []
            for weight in parent_weights:
                mutation = np.random.normal(0, 0.1, weight.shape)  # Изменяем каждый вес
                self.brain_weights.append(weight + mutation)
        else:
            self.brain_weights = [                  # Архитектура: 5 входов → 8 нейронов → 6 нейронов → 5 выходов
                np.random.uniform(-1, 1, (5, 8)),   # Входной слой (5 нейронов) → Скрытый слой 1 (8 нейронов)
                np.random.uniform(-1, 1, (8, 6)),   # Скрытый слой 1 → Скрытый слой 2
                np.random.uniform(-1, 1, (6, 5))    # Скрытый слой 2 → Выходной слой (5 действий)
            ]
    
    def brain(self, gen, object_input, map_size) -> int:
        self.age += 1
        if map_size[0] > 1:
            normalized_x = self.x / (map_size[0] - 1)
        else:
            normalized_x = 0.5
            
        if map_size[1] > 1:
            normalized_y = self.y / (map_size[1] - 1)
        else:
            normalized_y = 0.5

        entrance = np.array([
            self.energy / MAX_ENERGY,
            self.rotation / 4.0,
            normalized_x,
            normalized_y,
            object_input + 0.001
        ])
        
        layer1 = np.maximum(0, np.dot(entrance, self.brain_weights[0])) # Первый скрытый слой
        layer2 = np.maximum(0, np.dot(layer1, self.brain_weights[1])) # Второй скрытый слой
        output = 1 / (1 + np.exp(-np.dot(layer2, self.brain_weights[2]))) # Сигмоида
        action = np.argmax(output) # Вероятность нейронов
        
        return action
    

    def can_reproduce(self):
        return self.energy >= 30 and self.age > 10
    

    def reproduce(self, x, y):
        child_energy = self.energy // 2
        self.energy = self.energy // 2
      
        if isinstance(self.color, tuple) and len(self.color) >= 3:
            r, g, b = self.color[0], self.color[1], self.color[2]
            r = max(0, min(255, r + random.randint(-20, 20)))
            g = max(0, min(255, g + random.randint(-20, 20)))
            b = max(0, min(255, b + random.randint(-20, 20)))
            child_color = (r, g, b)
        
        child = Entity( # Создаем потомка с другими весами
            x, y,
            energy = child_energy,
            color = child_color,
            parent_weights = self.brain_weights
        )
        
        return child
    