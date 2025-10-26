"""Главный файл приложения."""
import pygame
import sys
import pygame_menu
from pathlib import Path

# Импорт игровой логики и состояния
from game_logic import TamagochiGame
from game_state import GameState
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS, SAVES_DIR, SAVE_FILENAME
from config import MENU_FONT, MENU_FONT_SIZE, MENU_THEME


def start_the_game(screen):
    """Запуск новой игры."""
    main_game(screen, new_game_flag=True)


def continue_the_game(screen):
    """Продолжение сохраненной игры."""
    main_game(screen, new_game_flag=False)


def main_game(screen, new_game_flag):
    """
    Основной игровой цикл.
    
    Args:
        screen: Pygame Surface для отрисовки
        new_game_flag: True для новой игры, False для продолжения
    """
    clock = pygame.time.Clock()
    
    # Создаем экземпляр состояния игры
    game_state = GameState()
    
    if not new_game_flag:
        # Загружаем сохраненное состояние
        try:
            game_state.load(SAVES_DIR / SAVE_FILENAME)
        except Exception as e:
            print(f"Ошибка загрузки сохранения: {e}")
    
    # Создаем экземпляр игры
    try:
        game = TamagochiGame(screen, game_state)
    except Exception as e:
        print(f"Ошибка инициализации игры: {e}")
        return
    
    # Запускаем музыку
    game.start_music()
    
    mute_key_pressed = False
    game_on = True
    
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save_game_state(SAVES_DIR / SAVE_FILENAME)
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        
        # Выход из игры по ESC
        if keys[pygame.K_ESCAPE]:
            print("Key Esc")
            game.save_game_state(SAVES_DIR / SAVE_FILENAME)
            game.music_off()
            game_on = False
        
        # Переключение звука по M (исправленная логика)
        if keys[pygame.K_m] and not mute_key_pressed:
            print("Key M was pressed")
            mute_key_pressed = True
            game.mute()
        elif not keys[pygame.K_m]:
            mute_key_pressed = False
        
        # Отрисовка фона
        screen.blit(game.current_background, (0, 0))
        
        # Обновление и отрисовка игры
        game.update()
        game.draw()
        
        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)


def main():
    """Главная функция приложения."""
    try:
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Создание темы меню один раз
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font = pygame_menu.font.get_font(MENU_FONT, MENU_FONT_SIZE)
        theme.widget_font = pygame_menu.font.get_font(MENU_FONT, MENU_FONT_SIZE)
        
        game_on = True
        
        while game_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_on = False
            
            # Отображаем экран меню только если игра продолжается
            if game_on:
                # Создание меню с заданной темой
                menu = pygame_menu.Menu(
                    'Главное меню', 
                    WINDOW_WIDTH, 
                    WINDOW_HEIGHT, 
                    theme=theme
                )
                
                # Добавление кнопок с заданным шрифтом
                menu.add.button(
                    'Вернуться к Puss',
                    continue_the_game,
                    screen,
                    font_name=MENU_FONT,
                    font_size=MENU_FONT_SIZE
                )
                menu.add.button(
                    'Новая игра',
                    start_the_game,
                    screen,
                    font_name=MENU_FONT,
                    font_size=MENU_FONT_SIZE
                )
                menu.add.button(
                    'Выход',
                    pygame_menu.events.EXIT,
                    font_name=MENU_FONT,
                    font_size=MENU_FONT_SIZE
                )
                
                # Отображаем меню
                result = menu.mainloop(screen)
                
                if result == pygame_menu.events.EXIT:
                    game_on = False
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
