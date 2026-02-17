import pickle

class SaveSystem:
    @staticmethod
    def save(world_map, iteration, filename='save/save.save'):
        """Сохраняем мир и номер итерации"""
        try:
            with open(filename, 'wb') as f:
                pickle.dump([world_map, iteration], f)
            print('Мир сохранен')
            return True
        except Exception as e:
            print(f"Не удалось сохранить: {e}")
            return False


    @staticmethod
    def load(filename='save/save.save'):
        """Загружаем мир и номер итерации"""
        try:
            with open(filename, 'rb') as f:
                loaded_list = pickle.load(f)
            print('Мир загружен')
            return loaded_list
        except FileNotFoundError:
            print("Файл не найден")
            return None
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return None
        