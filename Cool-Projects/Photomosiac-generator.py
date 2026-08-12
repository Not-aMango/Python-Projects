from PIL import Image,ImageStat
import time
from pathlib import Path
from shutil import rmtree
import numpy

start = time.perf_counter()

print('This program converts any given image into a Photo-Mosaic made entirely from tiny tiles/pieces of another image.\n'
      '(Code viewers note - anything with shrek written on it is just the second image :) )\n')

img = Image.open(input('Enter an Image dir. you want to refrence from: ')).convert('RGB')
size_img = img.size

shrek_img = Image.open(input('Enter the Image dir., you want the above Image to look like: ')).convert('RGB')
size_shrek = shrek_img.size

Path.mkdir(Path.home()/'image_converter/crops/',parents=True)

print()
print(size_img,size_shrek)
d = int(input('Enter how dense you want the image to be (ideal-20): '))
print('\nProcessing...')

def image():
    print('\nGetting first image rgb values and saving crops...')
    img_dic = {}
    i=1
    for x in range(0,size_img[0] - (d-1),d):
        for y in range(0,size_img[1] - (d-1),d):
            crop_img = img.crop((x,y , x+d,y+d))

            crop_img.save(Path.home() / f'image_converter/crops/{i}.jpg')

            mean_img = tuple(int(x) for x in ImageStat.Stat(crop_img).mean)

            img_dic.update({i:mean_img})

            i+=1
    print('Got first image rgb values')
    print(f'Crops Saved at: {Path.home()}/image_converter/crops')
    return  img_dic

def shrek():
    print('\nGetting second image rgb values')
    shrek_dic = {}
    i = 1
    for x in range(0,size_shrek[0] - (d-1),d):
        for y in range(0,size_shrek[1] - (d-1),d):
            crop_shrek = shrek_img.crop((x,y , x+d,y+d))

            mean_shrek = tuple(int(x) for x in ImageStat.Stat(crop_shrek).mean)

            shrek_dic.update({i:mean_shrek})

            i+=1

    print('Got second image rgb values')
    return  shrek_dic

def closest_rgb(shrek_dic, img_dic):
    print('\nComparing RGB values (this process may take time)')

    match = {}

    img_array = numpy.array(list(img_dic.values()))
    shrek_array = numpy.array(list(shrek_dic.values()))

    img_tiles = list(img_dic.keys())
    shrek_tiles = list(shrek_dic.keys())

    for i, rgb in enumerate(shrek_array):
        distance = numpy.sum((img_array - rgb) ** 2, axis=1)

        closest = numpy.argmin(distance)

        shrek_tile = shrek_tiles[i]
        tile = img_tiles[closest]

        match[shrek_tile] = tile

    print('Compared RGB values')
    return match

def crafter():
    print('\nCrafting a new Image')
    craft = Image.new("RGB", size_shrek)
    craft_size = craft.size

    i=1
    for x in range(0, craft_size[0] - (d-1), d):
        for y in range(0, craft_size[1] - (d-1), d):
            tile = match[i]
            tile_img = Image.open(Path(Path.home() / f'image_converter/crops/{tile}.jpg'))

            craft.paste(tile_img, (x,y))

            i+=1

    print('Crafted a new Image')
    return craft

img_dic = image()
shrek_dic = shrek()
match = closest_rgb(shrek_dic, img_dic)
craft = crafter()

craft.save(Path(Path.home()/'image_converter/converted_img.jpg'))
craft.show()
print(f'Image Saved at: {Path.home()}/image_converter/converted_img.jpg')
rmtree(Path.home()/'image_converter/crops/')

stop = time.perf_counter()
print(f'Execution Time: {(stop-start)/60} mins')
