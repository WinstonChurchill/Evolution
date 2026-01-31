import pygame

def DrawEntity(screen, color, color_border, cell_x, cell_y, cell_size, direction):
    pixel_x = cell_x * cell_size
    pixel_y = cell_y * cell_size
    
    pygame.draw.rect(screen, color, (pixel_x, pixel_y, cell_size, cell_size))
    
    border_width = max(1, cell_size // 15)
    pygame.draw.rect(screen, color_border, (pixel_x, pixel_y, cell_size, cell_size), border_width)
    
    eye_length = cell_size // 5
    spacing = cell_size // 25
    thickness = max(1, cell_size // 30)
    
    cx = pixel_x + cell_size // 2
    cy = pixel_y + cell_size // 2
    eye_offset = cell_size // 5
    
    if direction == 0: # up
        lx = cx - eye_offset
        pygame.draw.line(screen, color_border, 
                        (lx - spacing//2, pixel_y + border_width), 
                        (lx - spacing//2, pixel_y + border_width + eye_length), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (lx + spacing//2, pixel_y + border_width), 
                        (lx + spacing//2, pixel_y + border_width + eye_length), 
                        thickness)
        
        rx = cx + eye_offset
        pygame.draw.line(screen, color_border, 
                        (rx - spacing//2, pixel_y + border_width), 
                        (rx - spacing//2, pixel_y + border_width + eye_length), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (rx + spacing//2, pixel_y + border_width), 
                        (rx + spacing//2, pixel_y + border_width + eye_length), 
                        thickness)
    
    elif direction == 1: # down
        lx = cx - eye_offset
        pygame.draw.line(screen, color_border, 
                        (lx - spacing//2, pixel_y + cell_size - border_width), 
                        (lx - spacing//2, pixel_y + cell_size - border_width - eye_length), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (lx + spacing//2, pixel_y + cell_size - border_width), 
                        (lx + spacing//2, pixel_y + cell_size - border_width - eye_length), 
                        thickness)
        
        rx = cx + eye_offset
        pygame.draw.line(screen, color_border, 
                        (rx - spacing//2, pixel_y + cell_size - border_width), 
                        (rx - spacing//2, pixel_y + cell_size - border_width - eye_length), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (rx + spacing//2, pixel_y + cell_size - border_width), 
                        (rx + spacing//2, pixel_y + cell_size - border_width - eye_length), 
                        thickness)
    
    elif direction == 2: # right
        ty = cy - eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + border_width, ty - spacing//2), 
                        (pixel_x + border_width + eye_length, ty - spacing//2), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (pixel_x + border_width, ty + spacing//2), 
                        (pixel_x + border_width + eye_length, ty + spacing//2), 
                        thickness)
        
        by = cy + eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + border_width, by - spacing//2), 
                        (pixel_x + border_width + eye_length, by - spacing//2), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (pixel_x + border_width, by + spacing//2), 
                        (pixel_x + border_width + eye_length, by + spacing//2), 
                        thickness)
    
    elif direction == 3: # left
        ty = cy - eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + cell_size - border_width, ty - spacing//2), 
                        (pixel_x + cell_size - border_width - eye_length, ty - spacing//2), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (pixel_x + cell_size - border_width, ty + spacing//2), 
                        (pixel_x + cell_size - border_width - eye_length, ty + spacing//2), 
                        thickness)
        
        by = cy + eye_offset
        pygame.draw.line(screen, color_border, 
                        (pixel_x + cell_size - border_width, by - spacing//2), 
                        (pixel_x + cell_size - border_width - eye_length, by - spacing//2), 
                        thickness)
        pygame.draw.line(screen, color_border, 
                        (pixel_x + cell_size - border_width, by + spacing//2), 
                        (pixel_x + cell_size - border_width - eye_length, by + spacing//2), 
                        thickness)
