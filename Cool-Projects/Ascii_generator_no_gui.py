from PIL import Image
from tkinter import filedialog
from pathlib import Path

class Image_Ascii():
    def __init__(self):
        print('Enter Image Path')
        image_path = filedialog.askopenfilename(title='Enter Image directory', initialdir=Path.home(),
                                                filetypes=[('Image files', '*.jpg *.png *.jpeg *.webp'),
                                                           ('All files', '*.*')])
        print(f"Image_Path: {image_path}")

        self.image = Image.open(image_path).convert('RGBA')
        self.new_size = None

        self.version = input('Do you want a colored version [y/N]: ').lower()

        self.brightness_values = []
        self.chars = " .'`^,:;Il!i<~+_-?[}{1)(|/tfjrxuvczXYJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        self.colors = []


    def resizer(self):
        size = self.image.size
        self.new_size = (300,round(300/size[0] * size[1] * 0.45))
        self.image = self.image.resize(self.new_size).convert('RGBA')

    def get_brightness(self):
        for y in range(self.new_size[1]):
            for x in range(self.new_size[0]):
                pixel = self.image.getpixel((x,y))
                r,g,b,a = pixel
                self.colors.append((r,g,b))
                brightness = 0.299*r + 0.587*g + 0.114*b
                self.brightness_values.append(round(brightness))

    def ascii_generator_uncolored(self):
        i = 0
        for y in range(self.new_size[1]):
            for x in range(self.new_size[0]):
                pixel = self.brightness_values[i]
                char = pixel // 4
                print(self.chars[char], end='')
                i += 1
            print()

    def ascii_generator_colored(self):
        i = 0
        for y in range(self.new_size[1]):
            for x in range(self.new_size[0]):
                pixel = self.brightness_values[i]
                r,g,b,a = self.colors[i]
                char = pixel//4
                print(f'\033[38;2;{r};{g};{b}m{self.chars[char]}',end='')
                i+=1
            print()
        print('\033[0m', end='')


    def run(self):
        self.resizer()
        self.get_brightness()
        if self.version == 'y':self.ascii_generator_colored()
        else:self.ascii_generator_uncolored()

if __name__ == '__main__':
    Image_Ascii().run()
