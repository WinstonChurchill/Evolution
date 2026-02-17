from dataclasses import dataclass
from typing import Tuple


@dataclass
class Colors:
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    GREEN: Tuple[int, int, int] = (153, 229, 80)
    GREEN_ENERGY: Tuple[int, int, int] = (50, 205, 50)
    YELLOW_ENERGY: Tuple[int, int, int] = (255, 200, 0)
    RED_ENERGY: Tuple[int, int, int] = (220, 20, 60)
    BORDER: Tuple[int, int, int] = (30, 30, 30)
    BLACK: Tuple[int, int, int] = (0, 0, 0)



@dataclass
class GameConfig:
    # Размеры
    SIZE: int = 8  # Размер клетки в пикселях
    WIDTH: int = 1904
    HEIGHT: int = 1000
    SIZE_GUI: int = 300  # Ширина GUI панели
    
    @property
    def WIGTH_GAME_MAP(self) -> int:
        """Ширина игрового поля в клетках"""
        return (self.WIDTH - self.SIZE_GUI) // self.SIZE
    
    @property
    def HEIGHT_GAME_MAP(self) -> int:
        """Высота игрового поля в клетках"""
        return self.HEIGHT // self.SIZE
    
    # Параметры эволюции
    MAX_ENERGY: int = 15  # максимальное количество энергии
    RESTRICTION_ON_REPRODUCTION_AGE: int = 10  # репродуктивный возраст
    RESTRICTION_ON_REPRODUCTION_ENERGY: int = 15  # предел энергия нужный для размножения
    MUTATION_COEFFICIENT: float = 0.01  # сила изменения весов при мутации
    MUTATION_COEFFICIENT_COLOR: int = 10  # сила изменения цвета при мутации
    CHANCE_OF_MUTATION: float = 0.1  # процент мутации
    PHOTOSYNTHESIS_COEFFICIENT: int = 5  # коэфицент силы фотосинтеза
    CHANCE_OF_BOTS_APPERING: float = 0.05  # шанс появление ботов в начале
    
    # Прочее
    VERSION: str = '0.5v'
    FPS: int = 30
    NUMBER_OF_ITERATIONS_PER_DRAWING: int = 1  # количество итераций за одну отрисовку


# Создаём глобальный экземпляр конфига
config = GameConfig()
colors = Colors()
