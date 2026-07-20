#!/home/notamango/PyCharmMiscProject/Python_files/.venv/bin/python3

import pyperclip, sys

points = pyperclip.paste().split('\n')
sentences = ''

def yes():
    global sentences
    for sentence in points: sentences = sentences + f'• {sentence}\n'
def no():
    global sentences
    for sentence in points: sentences = sentences + sentence[2:]

if sys.argv[1] == '-a': yes()
elif sys.argv[1] == '-r': no()

pyperclip.copy(sentences)
