# Evolution

[Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

## [Lib:](requirements.txt) <!-- Версия библиотек см. requirements.txt -->
numpy 2.4.1  
pygame 2.5.2
pygame_gui 0.6.14

Для компиляции: `pyinstaller --onefile --distpath . --icon=gfx/1.ico --name Evolution main.py`

Клавиши:
    space - пауза  
    r - пересоздать мир  
    с - вкл/выкл смерть от старости
    x - вкл/выкл отрисовки сущностей
    left mouse button - скопировать сущность  
    right mouse button - вставить сущность