class TamagochiData:
    def __init__(self, screen):
        self.screen = screen
        self.image_resolution = (300, 300)
        self.image_paths = {
            'full': 'кот.png',
            'a bit hungry': 'cat-bit-hungry.png',
            'hungry': 'cat-hungry.png',
            'sleeping1': 'cat-sleeping1.png',
            'sleeping2': 'cat-sleeping2.png'
        }
        self.image_food = {
            'dumplings': 'dumplings.png',
            'fish': 'fish1.png',
        }
        self.lamp_bank = {
            'on': 'lamp_on.png',
            'off': 'lamp_off.png'
        }
        self.background_bank = {
            'light': 'фон днем.png',
            'dark': 'фон ночью.png'
        }
        self.translucent_coordinates = {
            'stuff': (25, 0),
            'parameters': (self.screen.get_width() - 145, 20)
        }
        self.translucent_sizes = {
            'stuff': (150, 720),
            'parameters': (110, 100)
        }
        self.other_images = {
            'gear': 'parameters_button.png',
            'gear_on': 'gear2_on.png'
        }
        self.other_coordinates = {
            'food_position': (50, 250),
            'lamp_rect': (self.screen.get_width() - 550, 350),
            'parameters_button_rect': (self.screen.get_width() - 130, 15),
            'hand_position': (30, 400)
        }
        self.scale_res = {
            'parameters_button': (100, 100),
            'hand': (150, 150)
        }
        self.hand_bank = {
            'hand0': 'рука.png',
            'hand1': 'рука1.png',
            'hand2': 'рука2.png',
            'hand3': 'рука3.png',
            'hand4': 'рука4.png',
            'hand5': 'рука5.png'
        }
        self.update_plus_numbers = {
            'hunger': 0.2,
            'sleep': 0.2,
            'joy': 0.15
        }
        self.update_minus_numbers = {
            'hunger': 0.01,
            'sleep': 0.003,
            'joy': 0.02
        }
        self.volume_level = 0.32  # Значение по умолчанию (можете установить другое) [0, 1]
        self.sound_volume_level = 0.71  # Значение по умолчанию (можете установить другое) [0, 1]

