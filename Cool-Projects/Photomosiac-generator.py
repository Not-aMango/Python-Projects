from PIL import Image,ImageStat
import time
from pathlib import Path
import numpy
from tkinter import filedialog

start = time.perf_counter()

print('This program converts any given image into a Photo-Mosaic made entirely from tiny tiles/pieces of another image.\n'
      '(Code viewers note - anything with shrek written on it is just the second image :) )\n')

print('Select Reference Image: ')
img_path = filedialog.askopenfilename(
    title= 'Select Reference Image',
    initialdir=Path.home(),
    filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp"),
            ("All files", "*.*")
        ]
)
print('Referenced Image dir. : '+img_path)
img = Image.open(img_path).convert('RGB')
size_img = img.size

print('\nSelect Target Image:')
shrek_path = filedialog.askopenfilename(
    title='Select Target Image',
    initialdir=Path.home(),
    filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp"),
            ("All files", "*.*")
     ]
)

print('Targeted Image Dir. : '+shrek_path)
shrek_img = Image.open(shrek_path).convert('RGB')
size_shrek = shrek_img.size

print()
print(size_img,size_shrek)
d = int(input('Enter how dense you want the image to be (ideal-20) - (More number means less clear image but fast output time and vice versa)\n : '))
print('\nProcessing...')

def image():
    print('\nGetting first image rgb values and saving crops...')
    img_dic = {}
    img_tiles = {}
    i=1
    for x in range(0,size_img[0] - (d-1),d):
        for y in range(0,size_img[1] - (d-1),d):
            crop_img = img.crop((x,y , x+d,y+d))

            img_tiles[i] = crop_img

            mean_img = tuple(int(x) for x in ImageStat.Stat(crop_img).mean)

            img_dic.update({i:mean_img})

            i+=1
    print('Got first image rgb values')
    return  img_dic, img_tiles

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

    img_tile_numbers = list(img_dic.keys())
    shrek_tiles = list(shrek_dic.keys())

    for i, rgb in enumerate(shrek_array):
        distance = numpy.sum((img_array - rgb) ** 2, axis=1)

        closest = numpy.argmin(distance)

        shrek_tile = shrek_tiles[i]
        tile = img_tile_numbers[closest]

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
            tile_img = img_tiles[tile]

            craft.paste(tile_img, (x,y))

            i+=1

    print('Crafted a new Image')
    return craft

img_dic, img_tiles = image()
shrek_dic = shrek()
match = closest_rgb(shrek_dic, img_dic)
craft = crafter()

output_dir = Path.home() / 'image_converter'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / 'converted_img.jpg'

craft.save(output_path)
craft.show()
print(f'Image Saved at: {Path.home()}/image_converter/converted_img.jpg')

stop = time.perf_counter()
print(f'Execution Time: {(stop-start)/60} mins')
