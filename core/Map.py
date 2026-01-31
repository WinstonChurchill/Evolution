from core.Settings import *

class Map:
    def __init__(self, x = 100, y = 100, map = []):
        self.size = [x, y]
        self.size_window = [x * SIZE, y * SIZE]
        self.map = [[None for i in range(x)] for i in range(y)]

    def get_map(self):
        return self.map
    
    def move(self, x, y, new_x, new_y):
        new_x = new_x % self.size[0]
        new_y = new_y % self.size[1]
        
        if self.map[new_y][new_x] != None and self.map[new_y][new_x] is not None:
            return False
        entity = self.map[y][x]

        if entity == None or entity is None:
            return False
        
        self.map[y][x] = None
        self.map[new_y][new_x] = entity
        
        entity.x = new_x
        entity.y = new_y
        
        return True

    def get_cor_map(self, x, y):
        x_itog = x % self.size[0]
        y_itog = y % self.size[1]
        return self.map[y_itog][x_itog]


if __name__ == '__main__':
    a = Map(100, 100)
    print(a.get_map())
