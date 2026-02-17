from core.Settings import config

class World_Map:
    """Игровое поле с циклическими границами (тор)"""
    
    def __init__(self, x=None, y=None, world_map=None, map_height=None, map_humidity=None):
        """
        Создание карты мира
        :param x: ширина в клетках
        :param y: высота в клетках
        """
        self.size = [x or config.WIGTH_GAME_MAP, y or config.HEIGHT_GAME_MAP]
        self.size_window = [self.size[0] * config.SIZE, self.size[1] * config.SIZE]

        # Создаем пустую карту
        if world_map is None:
            self.world_map = [[None for i in range(self.size[0])] for i in range(self.size[1])]

        # Для будущих фич: карта высот и влажности
        if map_height is None:
            self.map_height = []
        
        if map_humidity is None:
            self.map_humidity = []


    def get_map(self):
        """Получить всю карту"""
        return self.world_map


    def move(self, x, y, new_x, new_y):
        """
        Переместить сущность
        :return: успех операции
        """
        new_x = new_x % self.size[0]
        new_y = new_y % self.size[1]
        
        # Проверяем, свободна ли целевая клетка
        if self.world_map[new_y][new_x] is not None:
            return False
        
        entity = self.world_map[y][x]
        if entity is None:
            return False
        
        # Перемещаем
        self.world_map[y][x] = None
        self.world_map[new_y][new_x] = entity
        
        # Обновляем координаты сущности
        entity.x = new_x
        entity.y = new_y
        
        return True

    def get_cor_map(self, x, y):
        """
        Получить сущность по координатам с циклическими границами
        """
        x_itog = x % self.size[0]
        y_itog = y % self.size[1]
        return self.world_map[y_itog][x_itog]
    