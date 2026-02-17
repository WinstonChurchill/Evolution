import pygame

from core.Entity import Entity
from core.Settings import config

class InputHandler:
    """Обработка пользовательского ввода"""

    def __init__(self, game, renderer, world_map):
        self.game = game
        self.renderer = renderer
        self.world_map = world_map
        self.copy_entity = None  # Копия бота для вставки
    

    def handle(self, event):
        """Обработка события"""
        if event.type == pygame.KEYDOWN:
            self._handle_keyboard(event)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse(event)
    

    def _handle_keyboard(self, event):
        """Обработка нажатий клавиш"""
        if event.key == pygame.K_SPACE:  # Поставить на паузу
            self.game.paused = not self.game.paused
            print('Пауза:', self.game.paused)
        
        elif event.key == pygame.K_r:  # Пересоздать мир
            self.game.reset_world()
            print('Мир пересоздан')
        
        elif event.key == pygame.K_c:  # Включить/выключить смерть от старости
            self.game.old_age_enabled = not self.game.old_age_enabled
            print('Смерть от старости:', self.game.old_age_enabled)
        
        elif event.key == pygame.K_x:  # Включить/выключить отрисовку
            self.renderer.rendering = not self.renderer.rendering
            print('Отрисовка:', self.renderer.rendering)
        
        elif event.key == pygame.K_s:  # Сохранение мира 
            self.game.save_world()
        
        elif event.key == pygame.K_l:  # Загрузка мира
            self.game.load_world()
        
        elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):  # Увеличение просчета за одну итерацию
            self.game.iterations_per_frame += 1
            print('Увеличено итераций за одну отрисовку:', self.game.iterations_per_frame)
        
        elif event.key == pygame.K_MINUS:  # Уменьшено просчета за одну итерацию
            if self.game.iterations_per_frame > 1:
                self.game.iterations_per_frame -= 1
                print('Уменьшено итераций за одну отрисовку:', self.game.iterations_per_frame)
        
        elif event.key == pygame.K_e:  # Переключение режима отображения
            self.renderer.rendering_mode = (self.renderer.rendering_mode + 1) % 2
            print("Переключен режим отображения", self.renderer.rendering_mode)
    

    def _handle_mouse(self, event):
        """Обработка кликов мыши"""
        # Проверяем, что клик в пределах игрового поля
        if event.pos[0] < self.world_map.size_window[0] and event.pos[1] < self.world_map.size_window[1]:
            cell_x = event.pos[0] // config.SIZE
            cell_y = event.pos[1] // config.SIZE
            print(f"Клик по клетке: {cell_x}, {cell_y}")
            
            if event.button == 1 and self.renderer.rendering:  # ЛКМ - копирование
                a = self.world_map.get_cor_map(cell_x, cell_y)
                if a is not None and isinstance(a, Entity):
                    # Создаем копию сущности
                    self.copy_entity = Entity(
                        a.x, a.y, a.energy, a.color, a.rotation, 
                        [w.copy() for w in a.brain_weights]  # Глубокое копирование весов
                    )
                    print(f"Скопирована сущность: {a}")

            elif event.button == 3 and self.renderer.rendering:  # ПКМ - вставка
                if self.world_map.get_cor_map(cell_x, cell_y) is None and self.copy_entity is not None:
                    self.world_map.world_map[cell_y][cell_x] = Entity(
                        cell_x, cell_y, 
                        self.copy_entity.energy, 
                        self.copy_entity.color, 
                        self.copy_entity.rotation, 
                        [w.copy() for w in self.copy_entity.brain_weights]
                    )
                    print(f"Вставлена сущность {cell_x} {cell_y}")
