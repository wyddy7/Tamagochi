import pygame
import sys
import pygame_menu
import PussyLogicFile

def start_the_game(screen):
    main_game(screen, new_game_flag=True)

def continue_the_game(screen):
    main_game(screen, new_game_flag=False)

def main_game(screen, new_game_flag):
    clock = pygame.time.Clock()

    # Создаем экземпляр класса Tamagochi
    pussy = PussyLogicFile.Tamagochi(screen)

    if not new_game_flag:
        # Загружаем сохраненные данные при запуске игры
        pussy.load_game_state('pet_info.txt')

    pussy.music()

    m_key_pressed = False
    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pussy.save_game_state('pet_info.txt')
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:  # Сохраняем данные перед закрытием игры
                print("Key Esc")
                pussy.save_game_state('pet_info.txt')
                pussy.music_off()
                game_on = False
            if keys[pygame.K_m] and not m_key_pressed:
                print("Key M was pressed")
                m_key_pressed = True
            elif keys[pygame.K_m]:
                m_key_pressed = False
                pussy.mute()

        screen.blit(pussy.current_background, (0, 0))
        # screen.fill((253,244,227)) тут бежевым заливалось вроде
        pussy.update()
        pussy.draw()

        # Передаем текущие координаты мыши и состояние кнопки мыши
        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Be kind while playin' with Puss")

    #  доп данные для темы меню
    current_menu_font = 'comicsansms'
    current_menu_font_size = 30


    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False

        # Отображаем экран меню только если игра продолжается
        if game_on:
            # Создание темы с заданным шрифтом
            current_theme = pygame_menu.themes.THEME_DARK.copy()
            current_theme.title_font = pygame_menu.font.get_font(current_menu_font, current_menu_font_size)
            current_theme.widget_font = pygame_menu.font.get_font(current_menu_font, current_menu_font_size)

            # Создание меню с заданной темой
            menu = pygame_menu.Menu('Главное меню', width, height, theme=current_theme)

            # Добавление кнопок с заданным шрифтом
            menu.add.button('Вернуться к Puss', continue_the_game, screen, font_name=current_menu_font, font_size=current_menu_font_size)
            menu.add.button('Новая игра', start_the_game, screen, font_name=current_menu_font, font_size=current_menu_font_size)
            menu.add.button('Выход', pygame_menu.events.EXIT, font_name=current_menu_font, font_size=current_menu_font_size)
            # Отображаем меню
            result = menu.mainloop(screen)

            if result == pygame_menu.events.EXIT:
                game_on = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
