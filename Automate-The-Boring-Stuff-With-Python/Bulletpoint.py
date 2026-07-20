#!/home/notamango/PyCharmMiscProject/Python_files/.venv/bin/python3

import pyperclip, sys

if len(sys.argv) != 2:
    print("Usage: bullet -a | -r")
    sys.exit(1)

points = [item for item in pyperclip.paste().split('\n') if item!= '']

if sys.argv[1] == '-a':result = '\n'.join(f'• {statement}' for statement in points)
elif sys.argv[1] == '-r':result = '\n'.join(statement[2:] for statement in points)
else:
    print("Wrong Format")
    sys.exit(1)

pyperclip.copy(result)
print("Clipboard Updated")
