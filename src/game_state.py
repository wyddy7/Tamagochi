"""Модуль для управления состоянием игры."""
import json
from pathlib import Path
from config import DEFAULT_HUNGER, DEFAULT_SLEEP, DEFAULT_JOY, SAVES_DIR, SAVE_FILENAME


class GameState:
    """Класс для управления состоянием питомца в игре."""
    
    def __init__(self):
        """Инициализация параметров питомца."""
        self.hunger = DEFAULT_HUNGER
        self.sleep = DEFAULT_SLEEP
        self.joy = DEFAULT_JOY
        self.music_volume = 0.32
        self.sound_volume = 0.71
    
    def update_hunger(self, increase_rate=0.2, decrease_rate=0.01):
        """
        Обновление уровня голода.
        
        Args:
            increase_rate: Скорость увеличения при кормлении
            decrease_rate: Скорость уменьшения со временем
        """
        if self.hunger > 0:
            self.hunger -= decrease_rate
    
    def increase_hunger(self, rate=0.2):
        """Увеличить уровень голода при кормлении."""
        if self.hunger < 100:
            self.hunger += rate
            self.hunger = min(100, self.hunger)
    
    def update_sleep(self, increase_rate=0.2, decrease_rate=0.003):
        """
        Обновление уровня сна/энергии.
        
        Args:
            increase_rate: Скорость увеличения при отдыхе
            decrease_rate: Скорость уменьшения со временем
        """
        if self.sleep > 0:
            self.sleep -= decrease_rate
    
    def increase_sleep(self, rate=0.2):
        """Увеличить уровень сна при отдыхе."""
        if self.sleep < 100:
            self.sleep += rate
            self.sleep = min(100, self.sleep)
    
    def update_joy(self, increase_rate=0.15, decrease_rate=0.02):
        """
        Обновление уровня радости.
        
        Args:
            increase_rate: Скорость увеличения при поглаживании
            decrease_rate: Скорость уменьшения со временем
        """
        if self.joy > 0:
            self.joy -= decrease_rate
    
    def increase_joy(self, rate=0.15):
        """Увеличить уровень радости при поглаживании."""
        if self.joy < 100:
            self.joy += rate
            self.joy = min(100, self.joy)
    
    def save(self, filename=None):
        """
        Сохранить состояние игры в JSON файл.
        
        Args:
            filename: Путь к файлу сохранения. Если None, используется default.
        """
        if filename is None:
            filename = SAVES_DIR / SAVE_FILENAME
        
        # Убедимся, что папка существует
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'hunger': round(self.hunger, 2),
            'sleep': round(self.sleep, 2),
            'joy': round(self.joy, 2),
            'music_volume': round(self.music_volume, 2),
            'sound_volume': round(self.sound_volume, 2),
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            print(f'Game state saved to {filename}')
        except IOError as e:
            print(f'Ошибка сохранения игры: {e}')
    
    def load(self, filename=None):
        """
        Загрузить состояние игры из JSON файла.
        
        Args:
            filename: Путь к файлу сохранения. Если None, используется default.
        """
        if filename is None:
            filename = SAVES_DIR / SAVE_FILENAME
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                self.hunger = data.get('hunger', DEFAULT_HUNGER)
                self.sleep = data.get('sleep', DEFAULT_SLEEP)
                self.joy = data.get('joy', DEFAULT_JOY)
                self.music_volume = data.get('music_volume', 0.32)
                self.sound_volume = data.get('sound_volume', 0.71)
                
                print(f'Game state loaded from {filename}')
                print(f'  Hunger: {self.hunger:.2f}')
                print(f'  Sleep: {self.sleep:.2f}')
                print(f'  Joy: {self.joy:.2f}')
                print(f'  Music volume: {self.music_volume:.2f}')
                print(f'  Sound volume: {self.sound_volume:.2f}')
                
        except FileNotFoundError:
            print(f'Файл сохранения {filename} не найден. Используются значения по умолчанию.')
        except json.JSONDecodeError as e:
            print(f'Ошибка чтения файла сохранения: {e}. Используются значения по умолчанию.')
        except IOError as e:
            print(f'Ошибка загрузки игры: {e}')
    
    def load_legacy(self, filename):
        """
        Загрузить состояние из старого текстового формата pet_info.txt.
        
        Args:
            filename: Путь к файлу pet_info.txt
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        try:
                            value = float(value.strip())
                            
                            if key == 'hunger':
                                self.hunger = value
                            elif key == 'sleep':
                                self.sleep = value
                            elif key == 'joy':
                                self.joy = value
                            elif key == 'music_volume':
                                self.music_volume = value
                            elif key == 'sound_volume':
                                self.sound_volume = value
                        except ValueError:
                            print(f'Неверное значение для {key}: {value}')
                            continue
                
                print(f'Legacy save loaded from {filename}')
        except FileNotFoundError:
            print(f'Файл {filename} не найден.')
        except IOError as e:
            print(f'Ошибка загрузки: {e}')

