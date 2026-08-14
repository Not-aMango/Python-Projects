#!/home/notamango/PyCharmMiscProject/Python_files/.venv/bin/python3
from PIL import Image
import sys
from pathlib import Path

try:
    inp = sys.argv
    img = Image.open(inp[1])

    print('Processing...')
    print(f'Size of image: {img.size[0]}x{img.size[1]}')

    suffix = Path(inp[1]).suffix

    if inp[2] == '-s':
        img = img.resize((1920, 1080))

        save_path = Path.home() / f'resized_img{suffix}'
        img.save(save_path)
        print(f'Save Path: {save_path}')

    else:
        img = img.resize((int(inp[2]), int(inp[4])))

        if inp[5] == '-s':
            save_path = Path.home() / f'resized_img{suffix}'
            img.save(save_path)
            print(f'Save Path: {save_path}')

    print('Done.')

except Exception:
    print('Usage :\n => resize image-directory width x height (in pixels - default = 1920 x 1080) -s (-s = save / optional)')
