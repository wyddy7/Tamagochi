"""Основной модуль игровой логики."""
import pygame
import random
from pathlib import Path
try:
    from .config import (
        BASE_DIR, ASSETS_DIR, IMAGE_RESOLUTION, FONT_PATH, FONT_SIZE,
        TRANSLUCENT_COORDINATES, TRANSLUCENT_SIZES, 
        HUNGER_FULL_THRESHOLD, HUNGER_BIT_HUNGRY_THRESHOLD,
        PARAMETERS_BUTTON_SCALE, LAMP_IMAGE_SCALE, FOOD_IMAGE_SCALE,
        SLEEPING_ANIMATION_INTERVAL, JOY_ANIMATION_INTERVAL,
        STATS_INCREASE_RATES, STATS_DECREASE_RATES,
        HUNGER_DECREASE_RATE, SLEEP_DECREASE_RATE, JOY_DECREASE_RATE,
        DEFAULT_MUSIC_VOLUME, DEFAULT_SOUND_VOLUME
    )
    from .data import (
        get_image_paths, get_food_paths, get_lamp_paths, 
        get_background_paths, get_other_image_paths, get_hand_paths,
        get_sound_paths, get_music_folder, get_font_path
    )
    from .game_state import GameState
except ImportError:
    # Прямой запуск
    from config import (
        BASE_DIR, ASSETS_DIR, IMAGE_RESOLUTION, FONT_PATH, FONT_SIZE,
        TRANSLUCENT_COORDINATES, TRANSLUCENT_SIZES, 
        HUNGER_FULL_THRESHOLD, HUNGER_BIT_HUNGRY_THRESHOLD,
        PARAMETERS_BUTTON_SCALE, LAMP_IMAGE_SCALE, FOOD_IMAGE_SCALE,
        SLEEPING_ANIMATION_INTERVAL, JOY_ANIMATION_INTERVAL,
        STATS_INCREASE_RATES, STATS_DECREASE_RATES,
        HUNGER_DECREASE_RATE, SLEEP_DECREASE_RATE, JOY_DECREASE_RATE,
        DEFAULT_MUSIC_VOLUME, DEFAULT_SOUND_VOLUME
    )
    from data import (
        get_image_paths, get_food_paths, get_lamp_paths, 
        get_background_paths, get_other_image_paths, get_hand_paths,
        get_sound_paths, get_music_folder, get_font_path
    )
    from game_state import GameState


class TamagochiGame:
    """Основной класс игры тамагочи."""
    
    def __init__(self, screen, game_state=None):
        """
        Инициализация игры.
        
        Args:
            screen: Pygame Surface для отрисовки
            game_state: Экземпляр GameState для использования
        """
        self.screen = screen
        
        # Используем переданное состояние или создаем новое
        self.game_state = game_state if game_state else GameState()
        
        # Путь к папке с музыкой
        self.music_folder = get_music_folder()
        
        # Получаем список mp3 файлов в папке музыки и перемешиваем его
        try:
            music_files = [f for f in Path(self.music_folder).glob('*.mp3')]
            self.music_bank = [str(f) for f in music_files]
            random.shuffle(self.music_bank)
            self.current_track_index = 0
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")
            self.music_bank = []
            self.current_track_index = 0
        
        self.game_pause = False
        
        # Инициализация слайдеров громкости
        self.volume_slider_rect = pygame.Rect(self.screen.get_width() - 100, 300, 10, 200)
        self.is_volume_dragging = False
        self.mute_flag = False
        
        self.sound_volume_slider_rect = pygame.Rect(self.screen.get_width() - 70, 300, 10, 200)
        self.is_sound_volume_dragging = False
        
        # Флаг отображения параметров
        self.show_parameters = False
        self.prev_mouse_state = True
        
        # Координаты элементов интерфейса
        self.food_position = (50, 250)
        self.hand_position = (30, 400)
        
        # Загрузка всех ресурсов
        self.load_all_resources()
        
        # Инициализация музыки
        self.load_music()
        
    def load_all_resources(self):
        """Загрузка всех изображений и звуков."""
        try:
            # Получаем пути к ресурсам
            image_paths = get_image_paths()
            food_paths = get_food_paths()
            lamp_paths = get_lamp_paths()
            background_paths = get_background_paths()
            other_image_paths = get_other_image_paths()
            hand_paths = get_hand_paths()
            sound_paths = get_sound_paths()
            
            # Загружаем изображения кота
            self.full_image = pygame.image.load(image_paths['cat'])
            self.bit_hungry_image = pygame.image.load(image_paths['cat_bit_hungry'])
            self.bit_hungry_image = pygame.transform.scale(self.bit_hungry_image, IMAGE_RESOLUTION)
            self.hungry_image = pygame.image.load(image_paths['cat_hungry'])
            self.hungry_image = pygame.transform.scale(self.hungry_image, IMAGE_RESOLUTION)
            self.image = self.full_image
            
            # Загружаем изображения спящего кота
            self.sleeping_images = [
                pygame.image.load(image_paths['cat_sleeping1']),
                pygame.image.load(image_paths['cat_sleeping2'])
            ]
            self.sleeping_images = [
                pygame.transform.scale(self.sleeping_images[0], IMAGE_RESOLUTION),
                pygame.transform.scale(self.sleeping_images[1], IMAGE_RESOLUTION)
            ]
            self.current_sleeping_image = 0
            self.sleeping_timer = 0
            
            # Загрузка изображений еды
            self.food_image = pygame.image.load(food_paths['fish'])
            self.food_image = pygame.transform.scale(self.food_image, FOOD_IMAGE_SCALE)
            self.food_rect = self.food_image.get_rect()
            self.is_food_grabbed = False
            
            # Загрузка фонов
            self.background_light = pygame.image.load(background_paths['light'])
            self.background_light = pygame.transform.scale(
                self.background_light,
                (self.screen.get_width(), self.screen.get_height())
            )
            
            self.background_dark = pygame.image.load(background_paths['dark'])
            self.background_dark = pygame.transform.scale(
                self.background_dark,
                (self.screen.get_width(), self.screen.get_height())
            )
            self.current_background = self.background_light
            
            # Загрузка лампы
            self.lamp_image_off = pygame.image.load(lamp_paths['off'])
            self.lamp_image_off = pygame.transform.scale(self.lamp_image_off, LAMP_IMAGE_SCALE)
            self.lamp_image_on = pygame.image.load(lamp_paths['on'])
            self.lamp_image_on = pygame.transform.scale(self.lamp_image_on, LAMP_IMAGE_SCALE)
            self.lamp_image = self.lamp_image_off
            self.lamp_rect = self.lamp_image.get_rect()
            self.lamp_rect.topleft = (self.screen.get_width() - 550, 350)
            self.is_lamp_on = False
            
            # Загрузка изображений настроек
            gear_path = other_image_paths['gear']
            gear2_path = other_image_paths['gear_on']
            
            gear_img = pygame.image.load(gear_path)
            self.gear = pygame.transform.scale(gear_img, PARAMETERS_BUTTON_SCALE)
            
            gear2_img = pygame.image.load(gear2_path)
            self.gear2 = pygame.transform.scale(gear2_img, PARAMETERS_BUTTON_SCALE)
            
            self.parameters_button = self.gear
            self.parameters_button_rect = self.parameters_button.get_rect(
                topleft=(self.screen.get_width() - 130, 15)
            )
            
            # Загрузка изображений руки
            self.hand0 = pygame.image.load(hand_paths['hand0'])
            self.hand0 = pygame.transform.scale(self.hand0, (150, 150))
            
            self.hand1 = pygame.image.load(hand_paths['hand1'])
            self.hand1 = pygame.transform.scale(self.hand1, (150, 150))
            
            self.hand2 = pygame.image.load(hand_paths['hand2'])
            self.hand2 = pygame.transform.scale(self.hand2, (150, 150))
            
            self.hand3 = pygame.image.load(hand_paths['hand3'])
            self.hand3 = pygame.transform.scale(self.hand3, (150, 150))
            
            self.hand4 = pygame.image.load(hand_paths['hand4'])
            self.hand4 = pygame.transform.scale(self.hand4, (150, 150))
            
            self.hand5 = pygame.image.load(hand_paths['hand5'])
            self.hand5 = pygame.transform.scale(self.hand5, (150, 150))
            
            self.hand_images = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5]
            self.hand_image = self.hand0
            self.hand_rect = self.hand_image.get_rect()
            self.is_hand_grabbed = False
            self.current_hand_image = 0
            self.joy_timer = 0
            
            # Коллизия кота
            self.rect = self.image.get_rect()
            
            # Шрифт
            font_path = get_font_path()
            self.font = pygame.font.Font(font_path, FONT_SIZE)
            
        except Exception as e:
            print(f"Ошибка загрузки ресурсов: {e}")
            raise
    
    def load_music(self):
        """Инициализация музыки и звуков."""
        try:
            pygame.mixer.init()
            
            if self.music_bank:
                pygame.mixer.music.load(self.music_bank[self.current_track_index])
            
            # Инициализация звука поедания еды
            food_sound_path = get_sound_paths()['food']
            self.food_sound = pygame.mixer.Sound(food_sound_path)
            
            # Инициализация звука радости кота
            joy_sound_path = get_sound_paths()['joy']
            self.joy_sound = pygame.mixer.Sound(joy_sound_path)
            
        except Exception as e:
            print(f"Ошибка инициализации музыки: {e}")
    
    def adjust_volume(self, delta):
        """Изменение уровня громкости музыки."""
        self.game_state.music_volume += delta
        self.game_state.music_volume = max(0, min(1, self.game_state.music_volume))
        pygame.mixer.music.set_volume(self.game_state.music_volume)
    
    def adjust_sound_volume(self, delta):
        """Изменение уровня громкости звуков."""
        self.game_state.sound_volume += delta
        self.game_state.sound_volume = max(0, min(1, self.game_state.sound_volume))
        self.food_sound.set_volume(self.game_state.sound_volume)
        self.joy_sound.set_volume(self.game_state.sound_volume)
    
    def _draw_slider(self, rect, position, color=(117, 93, 154)):
        """Универсальный метод для отрисовки слайдера громкости."""
        # Отрисовка вертикальной полосы
        pygame.draw.rect(self.screen, color, rect)
        
        # Отрисовка ползунка
        slider_position_y = rect.y + (1 - position) * rect.height
        pygame.draw.circle(
            self.screen, 
            (255, 255, 255),
            (rect.centerx, int(slider_position_y)),
            10
        )
        
        # Обработка событий
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()[0]
        
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
            
            if is_mouse_pressed:
                new_position = 1 - (mouse_pos[1] - rect.y) / rect.height
                return max(0, min(1, new_position))
        
        return position
    
    def draw_volume_slider(self):
        """Отрисовка слайдера громкости музыки."""
        position = self._draw_slider(self.volume_slider_rect, self.game_state.music_volume)
        
        # Обновляем громкость
        delta = position - self.game_state.music_volume
        if abs(delta) > 0.01:
            self.adjust_volume(delta)
    
    def draw_sound_volume_slider(self):
        """Отрисовка слайдера громкости звуков."""
        position = self._draw_slider(self.sound_volume_slider_rect, self.game_state.sound_volume)
        
        # Обновляем громкость
        delta = position - self.game_state.sound_volume
        if abs(delta) > 0.01:
            self.adjust_sound_volume(delta)
    
    def mute(self):
        """Переключение режима без звука."""
        if not self.mute_flag:
            self.game_state.music_volume = 0
            self.game_state.sound_volume = 0
            pygame.mixer.music.set_volume(0)
            self.food_sound.set_volume(0)
            self.joy_sound.set_volume(0)
            self.mute_flag = True
        else:
            self.game_state.music_volume = DEFAULT_MUSIC_VOLUME
            self.game_state.sound_volume = DEFAULT_SOUND_VOLUME
            pygame.mixer.music.set_volume(self.game_state.music_volume)
            self.food_sound.set_volume(self.game_state.sound_volume)
            self.joy_sound.set_volume(self.game_state.sound_volume)
            self.mute_flag = False
    
    def play_next_track(self):
        """Переключение на следующий трек."""
        if not self.music_bank:
            return
        
        self.current_track_index = (self.current_track_index + 1) % len(self.music_bank)
        
        try:
            pygame.mixer.music.load(self.music_bank[self.current_track_index])
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Ошибка воспроизведения музыки: {e}")
    
    def music_off(self):
        """Выключение музыки."""
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.game_pause = True
    
    def start_music(self):
        """Запуск музыки."""
        if self.music_bank and not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Ошибка запуска музыки: {e}")
    
    def check_hunger(self):
        """Проверка и изменение внешнего вида кота в зависимости от голода."""
        if HUNGER_FULL_THRESHOLD < self.game_state.hunger <= 100:
            self.image = self.full_image
        elif HUNGER_BIT_HUNGRY_THRESHOLD < self.game_state.hunger <= HUNGER_FULL_THRESHOLD:
            self.image = self.bit_hungry_image
        elif 0 <= self.game_state.hunger <= HUNGER_BIT_HUNGRY_THRESHOLD:
            self.image = self.hungry_image
    
    def is_food_inside_cat(self):
        """Проверка, находится ли еда внутри области кота."""
        cat_rect = self.rect
        food_rect = pygame.Rect(self.food_position, self.food_image.get_size())
        return cat_rect.collidepoint(food_rect.center)
    
    def is_hand_inside_cat(self):
        """Проверка, находится ли рука внутри области кота."""
        cat_rect = self.rect
        hand_rect = pygame.Rect(self.hand_position, self.hand_image.get_size())
        return cat_rect.collidepoint(hand_rect.center)
    
    def update_hunger(self):
        """Обновление уровня голода."""
        self.game_state.update_hunger(
            STATS_INCREASE_RATES['hunger'],
            STATS_DECREASE_RATES['hunger']
        )
        
        if self.is_food_inside_cat():
            self.game_state.increase_hunger(STATS_INCREASE_RATES['hunger'])
            self.joy_sound.stop()
            
            if not pygame.mixer.get_busy():
                self.food_sound.play()
        else:
            self.food_sound.stop()
    
    def update_joy(self):
        """Обновление уровня радости."""
        self.game_state.update_joy(
            STATS_INCREASE_RATES['joy'],
            STATS_DECREASE_RATES['joy']
        )
        
        if self.is_hand_inside_cat():
            self.game_state.increase_joy(STATS_INCREASE_RATES['joy'])
            self.joy_timer += 1
            
            if self.joy_timer >= JOY_ANIMATION_INTERVAL:
                self.current_hand_image = (self.current_hand_image + 1) % len(self.hand_images)
                self.hand_image = self.hand_images[self.current_hand_image]
                self.joy_timer = 0
            else:
                self.hand_image = self.hand_images[self.current_hand_image]
            
            if not pygame.mixer.get_busy():
                self.joy_sound.play()
        else:
            self.joy_sound.stop()
            self.hand_image = self.hand0
    
    def update_sleeping(self):
        """Обновление состояния сна."""
        self.game_state.update_sleep(
            STATS_INCREASE_RATES['sleep'],
            STATS_DECREASE_RATES['sleep']
        )
        
        if self.is_lamp_on:
            self.lamp_image = self.lamp_image_on
            
            if self.game_state.sleep <= 94:
                self.current_background = self.background_dark
            
            # Увеличиваем сон при включенной лампе
            self.game_state.increase_sleep(STATS_INCREASE_RATES['sleep'])
            
            # Анимация сна
            self.sleeping_timer += 1
            
            if self.sleeping_timer >= SLEEPING_ANIMATION_INTERVAL:
                self.current_sleeping_image = (self.current_sleeping_image + 1) % len(self.sleeping_images)
                self.image = self.sleeping_images[self.current_sleeping_image]
                self.sleeping_timer = 0
            else:
                self.image = self.sleeping_images[self.current_sleeping_image]
        else:
            self.lamp_image = self.lamp_image_off
            self.current_background = self.background_light
    
    def is_cat_sleeping(self):
        """Проверка, включена ли лампа для сна."""
        if self.game_state.sleep <= 100:
            mouse_pos = pygame.mouse.get_pos()
            is_mouse_pressed = pygame.mouse.get_pressed()[0]
            
            if self.lamp_rect.collidepoint(mouse_pos) and is_mouse_pressed:
                self.is_lamp_on = True
            elif not is_mouse_pressed:
                self.is_lamp_on = False
        else:
            self.is_lamp_on = False
    
    def update_parameters_button(self):
        """Обновление состояния кнопки параметров."""
        mouse_state = pygame.mouse.get_pressed()
        is_mouse_pressed = mouse_state[0]
        
        if is_mouse_pressed and not self.prev_mouse_state:
            mouse_pos = pygame.mouse.get_pos()
            if self.parameters_button_rect.collidepoint(mouse_pos):
                self.show_parameters = not self.show_parameters
        
        self.prev_mouse_state = is_mouse_pressed
    
    def update_food_position(self):
        """Обновление позиции еды при перетаскивании."""
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()[0]
        
        if is_mouse_pressed:
            if self.food_rect.collidepoint(mouse_pos) and not self.is_food_grabbed:
                self.is_food_grabbed = True
                self.offset = (
                    self.food_position[0] - mouse_pos[0],
                    self.food_position[1] - mouse_pos[1]
                )
            
            if self.is_food_grabbed:
                self.food_position = (
                    mouse_pos[0] + self.offset[0],
                    mouse_pos[1] + self.offset[1]
                )
        else:
            self.is_food_grabbed = False
            self.food_position = (50, 250)
        
        self.food_rect.topleft = self.food_position
    
    def update_hand_position(self):
        """Обновление позиции руки при перетаскивании."""
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()[0]
        
        if is_mouse_pressed:
            if self.hand_rect.collidepoint(mouse_pos) and not self.is_hand_grabbed:
                self.is_hand_grabbed = True
                self.offset = (
                    self.hand_position[0] - mouse_pos[0],
                    self.hand_position[1] - mouse_pos[1]
                )
            
            if self.is_hand_grabbed:
                self.hand_position = (
                    mouse_pos[0] + self.offset[0],
                    mouse_pos[1] + self.offset[1]
                )
        else:
            self.is_hand_grabbed = False
            self.hand_position = (30, 400)
        
        self.hand_rect.topleft = self.hand_position
    
    def draw_stats(self):
        """Отрисовка статистики питомца."""
        # Голод
        hunger_text = self.font.render(f'Голод: {int(self.game_state.hunger)}', True, (255, 255, 255))
        hunger_rect = hunger_text.get_rect(
            center=(self.screen.get_width() // 3, self.screen.get_height() - 30)
        )
        self.screen.blit(hunger_text, hunger_rect)
        
        # Сон
        sleep_text = self.font.render(f'Энергия: {int(self.game_state.sleep)}', True, (255, 255, 255))
        sleep_rect = sleep_text.get_rect(
            center=(self.screen.get_width() // 3 + 200, self.screen.get_height() - 30)
        )
        self.screen.blit(sleep_text, sleep_rect)
        
        # Радость
        joy_text = self.font.render(f'Радость: {int(self.game_state.joy)}', True, (255, 255, 255))
        joy_rect = joy_text.get_rect(
            center=(self.screen.get_width() // 3 + 420, self.screen.get_height() - 30)
        )
        self.screen.blit(joy_text, joy_rect)
    
    def draw(self):
        """Отрисовка всех элементов игры."""
        # Кот
        self.rect.center = (self.screen.get_width() // 2 - 180, self.screen.get_height() // 2 + 70)
        self.screen.blit(self.image, self.rect)
        
        # Статистика
        self.draw_stats()
        
        # Устанавливаем громкость
        pygame.mixer.music.set_volume(self.game_state.music_volume)
        self.food_sound.set_volume(self.game_state.sound_volume)
        self.joy_sound.set_volume(self.game_state.sound_volume)
        
        # Кнопка параметров
        if self.show_parameters:
            self.draw_volume_slider()
            self.draw_sound_volume_slider()
            self.parameters_button = self.gear2
        else:
            self.parameters_button = self.gear
        
        # Полупрозрачные прямоугольники
        translucent_surface = pygame.Surface(TRANSLUCENT_SIZES['stuff'], pygame.SRCALPHA)
        translucent_surface.fill((0, 0, 0, 128))
        self.screen.blit(translucent_surface, TRANSLUCENT_COORDINATES['stuff'])
        
        # UI элементы
        self.screen.blit(self.parameters_button, self.parameters_button_rect)
        self.screen.blit(self.lamp_image, self.lamp_rect)
        self.screen.blit(self.food_image, self.food_position)
        self.screen.blit(self.hand_image, self.hand_position)
    
    def update(self):
        """Обновление игрового состояния."""
        # Обновляем радость
        self.update_joy()
        self.update_hand_position()
        
        # Обновляем голод
        self.update_hunger()
        self.update_food_position()
        
        # Обновляем сон
        self.is_cat_sleeping()
        self.update_sleeping()
        
        # Обновляем параметры
        self.update_parameters_button()
        
        # Переключение музыки
        if self.music_bank and not pygame.mixer.music.get_busy() and not self.game_pause:
            self.play_next_track()
    
    def save_game_state(self, filename=None):
        """Сохранение состояния игры."""
        self.game_state.save(filename)
    
    def load_game_state(self, filename=None):
        """Загрузка состояния игры."""
        self.game_state.load(filename)

