import pygame
import random
import os
from tamagochi_data import TamagochiData

# Alpha 1.2 06.02.2024
# - Добавлено выключение и включение музыки по клавише М.
# - Добавлен показатель радости и соответственно.
# - Добавлено поглаживание для повышения показателя радости.
# - Изменена структура получения данных через дополнительный класс значений.
# - Общие мелкие изменения.

class Tamagochi:
    def __init__(self, screen):
        # Получаем текущую директорию, в которой находится исполняемый файл
        current_dir = os.path.dirname(__file__)
        # Устанавливаем текущий рабочий каталог
        os.chdir(current_dir)
        # класс с данными
        self.data = TamagochiData(screen)
        
        # Инициализация данных
        self.screen = screen
        self.image_resolution = self.data.image_resolution
        self.image_paths = self.data.image_paths
        self.image_food = self.data.image_food
        self.lamp_bank = self.data.lamp_bank
        self.background_bank = self.data.background_bank
        self.translucent_coordinates = self.data.translucent_coordinates
        self.translucent_sizes = self.data.translucent_sizes
        self.other_images = self.data.other_images
        self.other_coordinates = self.data.other_coordinates
        self.scale_res = self.data.scale_res
        self.hand_bank = self.data.hand_bank
        self.update_plus_numbers = self.data.update_plus_numbers
        self.update_minus_numbers = self.data.update_minus_numbers

        # параметры кота изначальные
        self.hunger = 100  # чтобы при пустом файле всё равно работал
        self.sleep = 100
        self.joy = 100

        # Флаг игровой паузы
        self.game_pause = False

        # Путь к папке с музыкой (предполагаем, что она находится в той же директории, что и скрипт)
        self.music_folder = os.path.join(current_dir, 'music')

        # Получаем список mp3 файлов в папке музыки и перемешиваем его
        self.music_bank = [os.path.join(self.music_folder, file) for file in os.listdir(self.music_folder) if
                           file.endswith('.mp3')]
        random.shuffle(self.music_bank)

        self.current_track_index = 0
        self.load_music()

        self.volume_level = self.data.volume_level
        self.sound_volume_level = self.data.sound_volume_level
        self.temp_volume_level = self.volume_level
        self.temp_sound_volume_level = self.sound_volume_level

        # ползунок громкости музыки
        self.volume_slider_rect = pygame.Rect(self.screen.get_width() - 100, 300, 10, 200)
        self.is_volume_dragging = False
        self.mute_flag = False

        self.sound_volume_slider_rect = pygame.Rect(self.screen.get_width() - 70, 300, 10, 200)
        self.is_sound_volume_dragging = False
        self.volume_slider_position = self.volume_level
        self.sound_volume_slider_position = self.sound_volume_level

        # Установка начального уровня громкости для музыки и звуков
        pygame.mixer.music.set_volume(self.volume_level)
        self.food_sound.set_volume(self.sound_volume_level)

        # корды еды
        self.food_position = self.other_coordinates['food_position']

        self.load_images()

        self.sleeping_images = [pygame.image.load(self.image_paths['sleeping1']),
                                pygame.image.load(self.image_paths['sleeping2'])]
        self.sleeping_images = [pygame.transform.scale(self.sleeping_images[0], self.image_resolution), pygame.transform.scale(self.sleeping_images[1], self.image_resolution)]
        self.current_sleeping_image = 0
        self.sleeping_timer = 0
        self.sleeping_image_interval = 30

        # коллизия и флаг лампы
        self.lamp_rect = self.lamp_image.get_rect()
        self.lamp_rect.topleft = self.other_coordinates['lamp_rect']
        self.is_lamp_on = False

        # коллизия кота
        self.rect = self.image.get_rect()

        # шрифт текста основной
        self.font = pygame.font.Font("TLHeader-Regular-RUS.otf", 28)

        # коллизия руки для радости
        self.is_hand_grabbed = False
        self.hand_rect = self.hand_image.get_rect()
        self.hand_position = self.other_coordinates['hand_position']
        self.current_hand_image = 0
        self.joy_timer = 0
        self.joy_image_interval = 10

        # коллизия и флаг удерживания еды
        self.food_rect = self.food_image.get_rect()
        self.is_food_grabbed = False

        # Добавление кнопки параметров в конструкторе
        self.show_parameters = False
        self.prev_mouse_state = True
        self.parameters_button = self.gear
        self.parameters_button = pygame.transform.scale(self.parameters_button, self.scale_res['parameters_button'])
        self.parameters_button_rect = self.parameters_button.get_rect(topleft=self.other_coordinates['parameters_button_rect'])
        self.show_parameters_button_rect = self.parameters_button_rect

    def adjust_sound_volume(self, delta):
        # Изменение уровня громкости звука в зависимости от переданного значения delta
        self.sound_volume_slider_position += delta

        # Ограничиваем уровень громкости звука в пределах от 0 до 1
        self.sound_volume_level = max(0, min(1, self.sound_volume_slider_position))

        # Устанавливаем уровень громкости для звука
        self.food_sound.set_volume(self.sound_volume_level)
        self.joy_sound.set_volume(self.sound_volume_level)

    def draw_sound_volume_slider(self):
        self.sound_volume_slider_position = self.sound_volume_level
        self.adjust_sound_volume(0)
        # Отрисовка вертикальной полосы для звука
        pygame.draw.rect(self.screen, (117, 93, 154), self.sound_volume_slider_rect)

        # Отрисовка ползунка громкости звука в текущем положении
        slider_position_y = self.sound_volume_slider_rect.y + (
                1 - self.sound_volume_slider_position) * self.sound_volume_slider_rect.height
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (self.sound_volume_slider_rect.centerx, int(slider_position_y)), 10)

        # Обработка событий ползунка звука
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.sound_volume_slider_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (255, 255, 255), self.sound_volume_slider_rect, 2)

            if is_mouse_pressed:
                # Если мышь нажата над ползунком, обновляем положение ползунка
                self.is_sound_volume_dragging = True
                self.sound_volume_slider_position = 1 - (
                        mouse_pos[1] - self.sound_volume_slider_rect.y) / self.sound_volume_slider_rect.height
        else:
            self.is_sound_volume_dragging = False

        # Обновление уровня громкости звука, если ползунок перетаскивается
        if self.is_sound_volume_dragging:
            new_position = 1 - (mouse_pos[1] - self.sound_volume_slider_rect.y) / self.sound_volume_slider_rect.height
            delta = max(0, new_position) - self.sound_volume_slider_position
            self.adjust_sound_volume(delta)
            self.sound_volume_slider_position = max(0, min(1, new_position))

    def adjust_volume(self, delta):
        # Изменение уровня громкости в зависимости от переданного значения delta
        self.volume_slider_position += delta
        # print("volume_slider: ", self.volume_slider_position, " Delta:", delta)
        # Ограничиваем уровень громкости в пределах от 0 до 1
        self.volume_level = max(0, min(1, self.volume_slider_position))

        # Устанавливаем уровень громкости для музыки и звуков
        pygame.mixer.music.set_volume(self.volume_level)

    def draw_volume_slider(self):
        self.volume_slider_position = self.volume_level
        self.adjust_volume(0)
        # Отрисовка вертикальной полосы
        pygame.draw.rect(self.screen, (117, 93, 154), self.volume_slider_rect)

        # Отрисовка ползунка громкости в текущем положении
        slider_position_y = self.volume_slider_rect.y + (
                    1 - self.volume_slider_position) * self.volume_slider_rect.height
        pygame.draw.circle(self.screen, (255, 255, 255), (self.volume_slider_rect.centerx, int(slider_position_y)), 10)

        # Обработка событий ползунка
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.volume_slider_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, (255, 255, 255), self.volume_slider_rect, 2)

            if is_mouse_pressed:
                # Если мышь нажата над ползунком, обновляем положение ползунка
                self.is_volume_dragging = True
                self.volume_slider_position = 1 - (
                            mouse_pos[1] - self.volume_slider_rect.y) / self.volume_slider_rect.height
        else:
            self.is_volume_dragging = False

        # Обновление уровня громкости, если ползунок перетаскивается
        if self.is_volume_dragging:
            new_position = 1 - (mouse_pos[1] - self.volume_slider_rect.y) / self.volume_slider_rect.height
            delta = max(0, new_position) - self.volume_slider_position
            self.adjust_volume(delta)
            self.volume_slider_position = max(0, min(1, new_position))

    def save_game_state(self, filename):
        with open(filename, 'w') as file:
            file.write(f'hunger: {round(self.hunger, 2)}\n')
            file.write(f'sleep: {round(self.sleep, 2)}\n')
            file.write(f'joy: {round(self.joy, 2)}\n')
            file.write(f'music_volume: {round(self.volume_level, 2)}\n')
            file.write(f'sound_volume: {round(self.sound_volume_level, 2)}\n')

        print('Game state saved.')

    def load_game_state(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
                # Обработка содержимого файла, извлечение необходимых данных
                try:
                    print('Loading game states.')
                    lines = content.split('\n')
                    for line in lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = float(value.strip())

                            if key == 'hunger':
                                self.hunger = value
                                print(f'Loaded hunger level: {self.hunger}')
                            elif key == 'sleep':
                                self.sleep = value
                                print(f'Loaded sleep level: {self.sleep}')
                            elif key == 'joy':
                                self.joy = value
                                print(f'Loaded joy level: {self.joy}')
                            elif key == 'music_volume':
                                self.volume_level = value
                                print(f'Loaded volume_level level: {self.volume_level}')
                            elif key == 'sound_volume':
                                self.sound_volume_level = value
                                print(f'Loaded sound_volume_level level: {self.sound_volume_level}')
                            else:
                                print('Some parameters got to original values.')
                except IndexError:
                    print('Invalid file format or wrong text typed.')
        except FileNotFoundError:
            print('File not found. Using default values.')

    def load_images(self):
        # Загрузка изображений кота
        self.full_image = pygame.image.load(self.image_paths['full'])
        self.bit_hungry_image = pygame.image.load(self.image_paths['a bit hungry'])
        self.bit_hungry_image = pygame.transform.scale(self.bit_hungry_image, self.image_resolution)
        self.hungry_image = pygame.image.load(self.image_paths['hungry'])
        self.hungry_image = pygame.transform.scale(self.hungry_image, self.image_resolution)
        self.image = self.full_image

        # Загрузка изображений еды
        self.food_image = pygame.image.load(self.image_food['fish'])
        self.food_image = pygame.transform.scale(self.food_image, (100, 100))

        # Загрузка фона в светлое и темное время
        self.background_light = pygame.image.load(self.background_bank["light"])
        self.background_light = pygame.transform.scale(self.background_light,
                                                       (self.screen.get_width(), self.screen.get_height()))

        self.background_dark = pygame.image.load(self.background_bank["dark"])
        self.background_dark = pygame.transform.scale(self.background_dark,
                                                      (self.screen.get_width(), self.screen.get_height()))
        # Изначальное положение фона
        self.current_background = self.background_light

        # загрузка изображения лампы в выключенном состоянии
        self.lamp_image_off = pygame.image.load(self.lamp_bank['off'])
        self.lamp_image_off = pygame.transform.scale(self.lamp_image_off, (150, 150))

        # Загрузка изображения лампы во включенном состоянии
        self.lamp_image_on = pygame.image.load(self.lamp_bank['on'])
        self.lamp_image_on = pygame.transform.scale(self.lamp_image_on, (150, 150))

        # Начальное изображение лампы
        self.lamp_image = self.lamp_image_off

        # Инициализация изображений настроек
        self.gear = pygame.image.load(self.other_images['gear'])
        self.gear = pygame.transform.scale(self.gear, self.scale_res['parameters_button'])
        self.gear2 = pygame.image.load(self.other_images['gear_on'])
        self.gear2 = pygame.transform.scale(self.gear2, self.scale_res['parameters_button'])

        # Инициализация изображений кадров рук
        self.hand0 = pygame.image.load(self.hand_bank['hand0'])
        self.hand0 = pygame.transform.scale(self.hand0, self.scale_res['hand'])

        self.hand1 = pygame.image.load(self.hand_bank['hand1'])
        self.hand1 = pygame.transform.scale(self.hand1, self.scale_res['hand'])

        self.hand2 = pygame.image.load(self.hand_bank['hand2'])
        self.hand2 = pygame.transform.scale(self.hand2, self.scale_res['hand'])

        self.hand3 = pygame.image.load(self.hand_bank['hand3'])
        self.hand3 = pygame.transform.scale(self.hand3, self.scale_res['hand'])

        self.hand4 = pygame.image.load(self.hand_bank['hand4'])
        self.hand4 = pygame.transform.scale(self.hand4, self.scale_res['hand'])

        self.hand5 = pygame.image.load(self.hand_bank['hand5'])
        self.hand5 = pygame.transform.scale(self.hand5, self.scale_res['hand'])

        self.hand_images = [self.hand1, self.hand2, self.hand3, self.hand4, self.hand5]

        # начальное изображение ладони
        self.hand_image = self.hand0

    def draw_stats(self):
        # hunger
        hunger_level_text = self.font.render(f'Голод: {int(self.hunger)}', True, (255, 255, 255))
        hunger_level_text_rect = hunger_level_text.get_rect(
            center=(self.screen.get_width() // 3, self.screen.get_height() - 30))
        self.screen.blit(hunger_level_text, hunger_level_text_rect)

        # sleep
        sleep_level_text = self.font.render(f'Энергия: {int(self.sleep)}', True, (255, 255, 255))
        sleep_level_text_rect = sleep_level_text.get_rect(
            center=(self.screen.get_width() // 3 + 200, self.screen.get_height() - 30))
        self.screen.blit(sleep_level_text, sleep_level_text_rect)

        # joy
        joy_level_text = self.font.render(f'Радость: {int(self.joy)}', True, (255, 255, 255))
        joy_level_text_rect = joy_level_text.get_rect(
            center=(self.screen.get_width() // 3 + 420, self.screen.get_height() - 30))
        self.screen.blit(joy_level_text, joy_level_text_rect)

    def draw(self):
        self.rect.center = (self.screen.get_width() // 2 - 180, self.screen.get_height() // 2 + 70)
        self.screen.blit(self.image, self.rect)

        self.draw_stats()

        pygame.mixer.music.set_volume(self.volume_level)
        self.food_sound.set_volume(self.sound_volume_level)
        if self.show_parameters:
            # Отрисовка ползунка громкости
            self.draw_volume_slider()
            self.draw_sound_volume_slider()
            self.parameters_button = self.gear2
        else:
            self.parameters_button = self.gear

        # полупрозрачные прямоугольники как интерфейс
        self.load_translucent_surface(self.translucent_sizes['stuff'], self.translucent_coordinates['stuff'])
        # self.load_translucent_surface(self.translucent_sizes['parameters'], self.translucent_coordinates['parameters'])

        self.screen.blit(self.parameters_button, self.parameters_button_rect)

        self.screen.blit(self.lamp_image, self.lamp_rect)

        self.screen.blit(self.food_image, self.food_position)

        self.screen.blit(self.hand_image, self.hand_position)

    def load_translucent_surface(self, size, coordinates):
        # Создаем поверхность с прозрачностью для левой колонки
        translucent_surface = pygame.Surface(size, pygame.SRCALPHA)
        translucent_surface.fill((0, 0, 0, 128))  # Последнее число - уровень прозрачности

        # Рисуем полупрозрачный прямоугольник сзади еды
        self.screen.blit(translucent_surface, coordinates)

    def load_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_bank[self.current_track_index])

        # Инициализация звука поедания еды
        self.food_sound = pygame.mixer.Sound('Звук еды Майнкрафт1.mp3')
        # Инициализация звука радости кота
        self.joy_sound = pygame.mixer.Sound('cat purr1.mp3')

    def play_next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.music_bank)
        self.load_music()
        pygame.mixer.music.play()

    def music_off(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.game_pause = True

    def music(self):
        if not pygame.mixer.music.get_busy():
            self.play_next_track()

    def update_hunger(self):
        # Проверка голода
        self.check_hunger()
        # Уменьшение уровня голода, если он в пределах [0, 100]
        if self.hunger > 0:
            self.hunger -= self.update_minus_numbers['hunger']

        # Проверка, находится ли еда внутри области кота
        if self.is_food_inside_cat():
            # Увеличиваем уровень голода при наличии еды внутри области кота
            if self.hunger < 100: self.hunger += self.update_plus_numbers['hunger']
            self.joy_sound.stop()
            # Проверка изменения hunger и воспроизведение звука
            if not pygame.mixer.get_busy():
                self.food_sound.play()
        else:
            self.food_sound.stop()

    def update_joy(self):
        # Уменьшение радости потому что котика не гладят
        if self.joy > 0:
            self.joy -= self.update_minus_numbers['joy']

        # Проверка, находится ли еда внутри области кота
        if self.is_hand_inside_cat():
            # Увеличиваем уровень голода при наличии еды внутри области кота
            if self.joy < 100: self.joy += self.update_plus_numbers['joy']
            # Обновление изображения во время сна
            self.joy_timer += 1

            if self.joy_timer >= self.joy_image_interval:
                self.current_hand_image = (self.current_hand_image + 1) % len(self.hand_images)
                self.hand_image = self.hand_images[self.current_hand_image]
                self.joy_timer = 0
            else:
                self.hand_image = self.hand_images[self.current_hand_image]
            # Проверка изменения hunger и воспроизведение звука
            if not pygame.mixer.get_busy():
                self.joy_sound.play()
        else:
            self.joy_sound.stop()
            self.hand_image = self.hand0

    def update_sleeping(self):
        if self.sleep > 0:
            self.sleep -= self.update_minus_numbers['sleep']

        if self.is_lamp_on:
            self.lamp_image = self.lamp_image_on

            if self.sleep <= 94:
                self.current_background = self.background_dark

            # Увеличиваем сон, когда лампа включена
            self.sleep += self.update_plus_numbers['sleep']

            # Обновление изображения во время сна
            self.sleeping_timer += 1

            if self.sleeping_timer >= self.sleeping_image_interval:
                self.current_sleeping_image = (self.current_sleeping_image + 1) % len(self.sleeping_images)
                self.image = self.sleeping_images[self.current_sleeping_image]
                self.sleeping_timer = 0
            else:
                self.image = self.sleeping_images[self.current_sleeping_image]
        else:
            self.lamp_image = self.lamp_image_off
            self.check_hunger()
            self.current_background = self.background_light

    def update_parameters_button(self):
        mouse_state = pygame.mouse.get_pressed()
        is_mouse_pressed = mouse_state[0]  # 0 соответствует левой кнопке мыши

        if is_mouse_pressed and not self.prev_mouse_state:
            mouse_pos = pygame.mouse.get_pos()
            if self.show_parameters_button_rect.collidepoint(mouse_pos):
                self.show_parameters = not self.show_parameters

        self.prev_mouse_state = is_mouse_pressed

    def update(self):

        self.adjust_sound_volume(0)
        self.adjust_volume(0)

        self.update_joy()
        self.update_hand_position()

        self.update_hunger()
        self.update_food_position()

        self.is_cat_sleeping()
        self.update_sleeping()

        self.update_parameters_button()

        # Проверка окончания текущего трека и запуск следующего при необходимости
        if not pygame.mixer.music.get_busy() and not self.game_pause:
            self.play_next_track()

    def update_food_position(self):
        # Обработка событий для кнопки параметров
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()[0]

        if is_mouse_pressed:
            # Если курсор находится над едой и еда не удерживается, начнем удерживать
            if self.food_rect.collidepoint(mouse_pos) and not self.is_food_grabbed:
                self.is_food_grabbed = True
                self.offset = (self.food_position[0] - mouse_pos[0], self.food_position[1] - mouse_pos[1])

            # Если еда удерживается, обновим ее положение в соответствии с положением курсора
            if self.is_food_grabbed:
                self.food_position = (mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1])
        else:
            # Если еда удерживается и кнопка мыши отпущена, прекратим удерживать
            self.is_food_grabbed = False
            # Возвращаем позицию еды в изначальное положение
            self.food_position = self.other_coordinates['food_position']

        # Вне зависимости от состояния мыши, обновим положение прямоугольника
        self.food_rect.topleft = self.food_position

    def update_hand_position(self):
        # Обработка событий для кнопки параметров
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_pressed = pygame.mouse.get_pressed()[0]

        if is_mouse_pressed:
            # Если курсор находится над едой и еда не удерживается, начнем удерживать
            if self.hand_rect.collidepoint(mouse_pos) and not self.is_hand_grabbed:
                self.is_hand_grabbed = True
                self.offset = (self.hand_position[0] - mouse_pos[0], self.hand_position[1] - mouse_pos[1])

            # Если еда удерживается, обновим ее положение в соответствии с положением курсора
            if self.is_hand_grabbed:
                self.hand_position = (mouse_pos[0] + self.offset[0], mouse_pos[1] + self.offset[1])
        else:
            # Если еда удерживается и кнопка мыши отпущена, прекратим удерживать
            self.is_hand_grabbed = False
            # Возвращаем позицию еды в изначальное положение
            self.hand_position = self.other_coordinates['hand_position']

        # Вне зависимости от состояния мыши, обновим положение прямоугольника
        self.hand_rect.topleft = self.hand_position

    def is_food_inside_cat(self):
        # Проверка, находится ли центр еды внутри области картинки кота
        cat_rect = self.rect
        food_rect = pygame.Rect(self.food_position, self.food_image.get_size())
        return cat_rect.collidepoint(food_rect.center)

    def is_hand_inside_cat(self):
        # Проверка, находится ли центр еды внутри области картинки кота
        # print('Joy-')
        cat_rect = self.rect
        hand_rect = pygame.Rect(self.hand_position, self.hand_image.get_size())
        # print(f"Cat Rect: {cat_rect}, Hand Rect: {hand_rect}")
        return cat_rect.collidepoint(hand_rect.center)

    def is_cat_sleeping(self):
        if self.sleep <= 100:
            # Проверка, была ли нажата кнопка лампы
            mouse_pos = pygame.mouse.get_pos()
            is_mouse_pressed = pygame.mouse.get_pressed()[0]

            if self.lamp_rect.collidepoint(mouse_pos) and is_mouse_pressed:
                self.is_lamp_on = True
            elif not is_mouse_pressed:
                self.is_lamp_on = False
        else:
            self.is_lamp_on = False

    def check_hunger(self):
        if 80 < self.hunger <= 100:
            self.image = self.full_image
        elif 40 < self.hunger <= 80:
            self.image = self.bit_hungry_image
        elif -1 < self.hunger <= 40:
            self.image = self.hungry_image

    def mute(self):
        self.mute_flag = not self.mute_flag
        if self.mute_flag:
            self.temp_volume_level = self.volume_level
            self.temp_sound_volume_level = self.sound_volume_level
            zero_music = -float(self.volume_level)
            self.adjust_volume(zero_music)
            zero_sound = -float(self.sound_volume_level)
            self.adjust_sound_volume(zero_sound)
        if not self.mute_flag:
            self.adjust_volume(self.temp_volume_level)
            self.adjust_sound_volume(self.temp_sound_volume_level)
