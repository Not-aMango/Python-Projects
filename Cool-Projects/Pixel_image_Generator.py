from PIL import Image,ImageStat
from pathlib import Path

print('This program pixelates any given image to make it look like pixelated retro-style image.\n')

directory = input("Enter an absolute image dir. : ")
image = Image.open(directory).convert('RGBA')
size = image.size

d = int(input('Enter pixel density(ideal 10 -> less number means more detailed image) : '))

def pixelify(image):
    print('\nProcessing Image\n')
    pixel_image = Image.new('RGBA', size)

    for x in range(0, size[0] - (d-1), d):
        for y in range(0, size[1] - (d-1), d):
            crop = image.crop((x,y , x+d,y+d))

            stat = ImageStat.Stat(crop)
            mean = tuple(int(x) for x in stat.mean)

            tile = Image.new('RGBA',crop.size,mean)

            pixel_image.paste(tile,(x,y))
    print('Done\n')
    return pixel_image

pixel_image = pixelify(image)
pixel_image.show()
pixel_image.save(Path.home()/f'pixel_image.{directory[-3:]}')
print(f"Image saved in : {Path.home()}/pixel_image.{directory[-3:]}")
