#!/home/notamango/PyCharmMiscProject/Python_files/.venv/bin/python3
import webbrowser, sys, pyperclip

url = 'https://www.google.com/maps/search/'

if len(sys.argv) > 1:
    location = url + "+".join(sys.argv[1:])
else:
    location = url + pyperclip.paste().replace(" ", "+")

webbrowser.open(location)

