"""Модуль с данными игры."""
from pathlib import Path
from config import ASSETS_DIR


def get_image_paths():
    """Получить пути к изображениям спрайтов."""
    sprites_dir = ASSETS_DIR / 'sprites'
    return {
        'cat': str(sprites_dir / 'кот.png'),
        'cat_bit_hungry': str(sprites_dir / 'cat-bit-hungry.png'),
        'cat_hungry': str(sprites_dir / 'cat-hungry.png'),
        'cat_sleeping1': str(sprites_dir / 'cat-sleeping1.png'),
        'cat_sleeping2': str(sprites_dir / 'cat-sleeping2.png'),
    }


def get_food_paths():
    """Получить пути к изображениям еды."""
    sprites_dir = ASSETS_DIR / 'sprites'
    return {
        'dumplings': str(sprites_dir / 'dumplings.png'),
        'fish': str(sprites_dir / 'fish1.png'),
    }


def get_lamp_paths():
    """Получить пути к изображениям лампы."""
    sprites_dir = ASSETS_DIR / 'sprites'
    return {
        'on': str(sprites_dir / 'lamp_on.png'),
        'off': str(sprites_dir / 'lamp_off.png'),
    }


def get_background_paths():
    """Получить пути к фонам."""
    sprites_dir = ASSETS_DIR / 'sprites'
    return {
        'light': str(sprites_dir / 'фон днем.png'),
        'dark': str(sprites_dir / 'фон ночью.png'),
    }


def get_other_image_paths():
    """Получить пути к другим изображениям UI."""
    sprites_dir = ASSETS_DIR / 'sprites'
    return {
        'gear': str(sprites_dir / 'parameters_button.png'),
        'gear_on': str(sprites_dir / 'gear2_on.png'),
    }


def get_hand_paths():
    """Получить пути к изображениям руки."""
    sprites_dir = ASSETS_DIR / 'sprites'
    return {
        'hand0': str(sprites_dir / 'рука.png'),
        'hand1': str(sprites_dir / 'рука1.png'),
        'hand2': str(sprites_dir / 'рука2.png'),
        'hand3': str(sprites_dir / 'рука3.png'),
        'hand4': str(sprites_dir / 'рука4.png'),
        'hand5': str(sprites_dir / 'рука5.png'),
    }


def get_sound_paths():
    """Получить пути к звуковым файлам."""
    sounds_dir = ASSETS_DIR / 'sounds'
    return {
        'food': str(sounds_dir / 'Звук еды Майнкрафт1.mp3'),
        'joy': str(sounds_dir / 'cat purr1.mp3'),
    }


def get_music_folder():
    """Получить путь к папке с музыкой."""
    return str(ASSETS_DIR / 'music')


def get_font_path():
    """Получить путь к шрифту."""
    fonts_dir = ASSETS_DIR / 'fonts'
    return str(fonts_dir / 'TLHeader-Regular-RUS.otf')

