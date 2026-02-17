import pygame

from core.Settings import colors, config

def DrawEntity(screen, color, color_border, cell_x, cell_y, cell_size, direction):
    """
    Отрисовка одной сущности с глазами, указывающими направление
    :param direction: 0 вверх, 1 вправо, 2 вниз, 3 влево
    """
    pixel_x = cell_x * cell_size
    pixel_y = cell_y * cell_size
    
    # Рисуем тело
    pygame.draw.rect(screen, color, (pixel_x, pixel_y, cell_size, cell_size))
    
    # Рисуем границу
    border_width = max(1, cell_size // 15)
    pygame.draw.rect(screen, color_border, (pixel_x, pixel_y, cell_size, cell_size), border_width)
    
    # Параметры для глаз
    eye_length = cell_size // 5
    spacing = max(2, cell_size // 25)
    thickness = max(1, cell_size // 15)
    
    cx = pixel_x + cell_size // 2
    cy = pixel_y + cell_size // 2
    eye_offset = cell_size // 5
    
    # Рисуем глаза в зависимости от направления
    if direction == 0:  # вверх
        lx = cx - eye_offset
        pygame.draw.line(screen, color_border, 
                        (lx - spacing // 2, pixel_y + border_width), 
                        (lx - spacing // 2, pixel_y + border_width + eye_length), 
                        thickness)
        
        rx = cx + eye_offset
        pygame.draw.line(screen, color_border, 
                        (rx - spacing // 2, pixel_y + border_width), 
                        (rx - spacing // 2, pixel_y + border_width + eye_length), 
                        thickness)
    
    elif direction == 1:  # вправо
        ty = cy - eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + cell_size - border_width, ty - spacing // 2), 
                        (pixel_x + cell_size - border_width - eye_length, ty - spacing // 2), 
                        thickness)
        
        by = cy + eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + cell_size - border_width, by - spacing // 2), 
                        (pixel_x + cell_size - border_width - eye_length, by - spacing // 2), 
                        thickness)

    elif direction == 2:  # вниз
        lx = cx - eye_offset
        pygame.draw.line(screen, color_border, 
                        (lx - spacing // 2, pixel_y + cell_size - border_width), 
                        (lx - spacing // 2, pixel_y + cell_size - border_width - eye_length), 
                        thickness)

        rx = cx + eye_offset
        pygame.draw.line(screen, color_border, 
                        (rx - spacing // 2, pixel_y + cell_size - border_width), 
                        (rx - spacing // 2, pixel_y + cell_size - border_width - eye_length), 
                        thickness)

    elif direction == 3:  # влево
        ty = cy - eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + border_width, ty - spacing // 2), 
                        (pixel_x + border_width + eye_length, ty - spacing // 2), 
                        thickness)

        by = cy + eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + border_width, by - spacing // 2), 
                        (pixel_x + border_width + eye_length, by - spacing // 2), 
                        thickness)


class Renderer:
    """Класс для управления отрисовкой"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.rendering = True  # Включена ли отрисовка
        self.rendering_mode = 0  # Режим отрисовки: 0 - естественный цвет, 1 - по энергии
    
    def draw_world(self, world_map, iteration, fps, paused):
        """Отрисовка всего мира"""
        active_display = pygame.display.get_active()
        
        if not active_display:
            return
        
        entity_count = 0
        
        for y in range(world_map.size[1]):
            for x in range(world_map.size[0]):
                cell = world_map.get_cor_map(x, y)
                if cell is not None:
                    entity_count += 1
                    
                    if self.rendering_mode == 0:  # Естественный цвет
                        DrawEntity(self.screen, cell.color, colors.BORDER, 
                                  cell.x, cell.y, config.SIZE, cell.rotation)
                    
                    elif self.rendering_mode == 1:  # Количество энергии
                        if cell.energy >= config.MAX_ENERGY * 0.66:
                            DrawEntity(self.screen, colors.GREEN_ENERGY, colors.BORDER, 
                                      cell.x, cell.y, config.SIZE, cell.rotation)
                        elif cell.energy >= config.MAX_ENERGY * 0.33:
                            DrawEntity(self.screen, colors.YELLOW_ENERGY, colors.BORDER, 
                                      cell.x, cell.y, config.SIZE, cell.rotation)
                        else:
                            DrawEntity(self.screen, colors.RED_ENERGY, colors.BORDER, 
                                      cell.x, cell.y, config.SIZE, cell.rotation)
        
        # Обновляем заголовок окна
        pygame.display.set_caption(f"Evolution Version: {config.VERSION} "
                                   f"Iteration: {iteration} FPS: {int(fps)} "
                                   f"Entities: {entity_count} {'PAUSED' if paused else ''}")
        