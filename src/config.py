"""Конфигурационный файл для игры Tamagochi."""
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
SAVES_DIR = BASE_DIR / "saves"

# Настройки окна
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Be kind while playin' with Puss"
FPS = 60

# Разрешение изображений
IMAGE_RESOLUTION = (300, 300)
HAND_SCALE = (150, 150)
PARAMETERS_BUTTON_SCALE = (100, 100)
LAMP_IMAGE_SCALE = (150, 150)
FOOD_IMAGE_SCALE = (100, 100)

# Пути к спрайтам
SPRITE_PATHS = {
    'cat': 'cat.png',
    'cat_bit_hungry': 'cat-bit-hungry.png',
    'cat_hungry': 'cat-hungry.png',
    'cat_sleeping1': 'cat-sleeping1.png',
    'cat_sleeping2': 'cat-sleeping2.png',
}

# Пути к еде
FOOD_PATHS = {
    'dumplings': 'dumplings.png',
    'fish': 'fish1.png',
}

# Пути к лампе
LAMP_PATHS = {
    'on': 'lamp_on.png',
    'off': 'lamp_off.png',
}

# Пути к фонам
BACKGROUND_PATHS = {
    'light': 'фон днем.png',
    'dark': 'фон ночью.png',
}

# Пути к другим изображениям
OTHER_IMAGE_PATHS = {
    'gear': 'parameters_button.png',
    'gear_on': 'gear2_on.png',
}

# Пути к изображениям руки
HAND_PATHS = {
    'hand0': 'рука.png',
    'hand1': 'рука1.png',
    'hand2': 'рука2.png',
    'hand3': 'рука3.png',
    'hand4': 'рука4.png',
    'hand5': 'рука5.png',
}

# Пути к звукам
SOUND_PATHS = {
    'food': 'Звук еды Майнкрафт1.mp3',
    'joy': 'cat purr1.mp3',
}

# Путь к шрифту
FONT_PATH = 'TLHeader-Regular-RUS.otf'
FONT_SIZE = 28

# Координаты элементов интерфейса (относительно экрана)
UI_COORDINATES = {
    'food_position': (50, 250),
    'hand_position': (30, 400),
    'parameters_button': None,  # Будет установлено динамически
    'lamp_position': None,  # Будет установлено динамически
    'stats_position': None,  # Будет установлено динамически
}

# Размеры прозрачных прямоугольников
TRANSLUCENT_SIZES = {
    'stuff': (150, 720),
    'parameters': (110, 100),
}

# Координаты прозрачных прямоугольников
TRANSLUCENT_COORDINATES = {
    'stuff': (25, 0),
    'parameters': None,  # Будет установлено динамически
}

# Параметры изменения состояний питомца
STATS_INCREASE_RATES = {
    'hunger': 0.2,
    'sleep': 0.2,
    'joy': 0.15,
}

STATS_DECREASE_RATES = {
    'hunger': 0.01,
    'sleep': 0.003,
    'joy': 0.02,
}

# Константы для совместимости
HUNGER_DECREASE_RATE = STATS_DECREASE_RATES['hunger']
SLEEP_DECREASE_RATE = STATS_DECREASE_RATES['sleep']
JOY_DECREASE_RATE = STATS_DECREASE_RATES['joy']

# Пороги состояний
HUNGER_FULL_THRESHOLD = 80
HUNGER_BIT_HUNGRY_THRESHOLD = 40

# Начальные параметры питомца
DEFAULT_HUNGER = 100
DEFAULT_SLEEP = 100
DEFAULT_JOY = 100

# Настройки громкости
DEFAULT_MUSIC_VOLUME = 0.32
DEFAULT_SOUND_VOLUME = 0.71

# Настройки анимации
SLEEPING_ANIMATION_INTERVAL = 30
JOY_ANIMATION_INTERVAL = 10

# Сохранение игры
SAVE_FILENAME = 'game_save.json'

# Настройки меню
MENU_FONT = 'comicsansms'
MENU_FONT_SIZE = 30
MENU_THEME = 'THEME_DARK'

