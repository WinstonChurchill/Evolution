# Evolution

[Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

## [Lib:](requirements.txt) <!-- Версия библиотек см. requirements.txt -->
numpy 2.4.1  
pygame 2.5.2

Для компиляции: `pyinstaller --onefile --distpath . --icon=gfx/1.ico --name Evolution main.py`

## Клавиши:  
    space - пауза  
    r - пересоздать мир  
    с - вкл/выкл смерть от старости  
    x - вкл/выкл отрисовки сущностей  
    left mouse button - скопировать сущность  
    right mouse button - вставить сущность  
    s - сохранить мир  
    l - загрузить мир  
    +/= - увеличение итераций за один кадр  
    - - уменьшение количество итераций за один кадр  
    