import pyperclip
a = pyperclip.paste().split('\n')
c=''
for i in a:
    c+='• '+i+'\n'
pyperclip.copy(c)
