import random
import pygame

from core.World import World_Map
from core.Entity import Entity, Entity_processing_function
from core.Settings import config
from core.Save import SaveSystem
from core.Renderer import Renderer
from core.Input_handler import InputHandler

class GameController:
    def __init__(self):
        self.world_map = None
        self.iteration = 0
        self.paused = False
        self.old_age_enabled = True  # Смерть от старости
        self.iterations_per_frame = config.NUMBER_OF_ITERATIONS_PER_DRAWING
        
        # Инициализация PyGame
        pygame.init()
        pygame.font.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        
        # Настройка окна
        icon = pygame.image.load('gfx/1.ico')
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), 
                                              pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('gfx/ProggyClean.ttf', 30)
        
        # Создание мира
        self.reset_world()
        
        # Инициализация компонентов
        self.renderer = Renderer(self.screen, self.font)
        self.input_handler = InputHandler(self, self.renderer, self.world_map)
        self.save_system = SaveSystem()
        
        self.running = True
    

    def reset_world(self):
        """Создает новое чистое поле и расставляет ботов"""
        self.world_map = World_Map()
        for y in range(self.world_map.size[1]):
            for x in range(self.world_map.size[0]):
                if random.random() <= config.CHANCE_OF_BOTS_APPERING:
                    entity = Entity(x, y)
                    self.world_map.world_map[y][x] = entity
        self.iteration = 0
        print("Новый мир создан")
    

    def save_world(self):
        """Сохранение мира"""
        self.save_system.save(self.world_map, self.iteration)
    

    def load_world(self):
        """Загрузка мира"""
        loaded = self.save_system.load()
        if loaded:
            self.world_map, self.iteration = loaded
            # Обновляем ссылку в input_handler
            self.input_handler.world_map = self.world_map
    

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.input_handler.handle(event)
            
            # Обновление мира
            if not self.paused:
                self._update_world()
            
            # Отрисовка
            if self.renderer.rendering:
                self.screen.fill((255, 255, 255))
                self.renderer.draw_world(self.world_map, self.iteration, 
                                        self.clock.get_fps(), self.paused)
                pygame.display.update()
            
            self.clock.tick(config.FPS)
        
        pygame.quit()
    

    def _update_world(self):
        """Обновление мира на несколько итераций"""
        for _ in range(self.iterations_per_frame):
            entities_to_process = []
            entity_count = 0
            
            # Собираем все сущности для обработки
            for y in range(self.world_map.size[1]):
                for x in range(self.world_map.size[0]):
                    cell = self.world_map.get_cor_map(x, y)
                    if cell is not None and isinstance(cell, Entity):
                        entities_to_process.append((x, y, cell))
                        entity_count += 1
            
            # Обрабатываем их
            if entities_to_process:
                self.iteration += 1
                Entity_processing_function(self.world_map, entities_to_process, self.old_age_enabled)
                
                print(f'Количество сущностей: {entity_count}, Итераций: {self.iteration}')
