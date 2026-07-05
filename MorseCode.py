morse = {
"A": ".-",
"B": "-...",
"C": "-.-.",
"D": "-..",
"E": ".",
"F": "..-.",
"G": "--.",
"H": "....",
"I": "..",
"J": ".---",
"K": "-.-",
"L": ".-..",
"M": "--",
"N": "-.",
"O": "---",
"P": ".--.",
"Q": "--.-",
"R": ".-.",
"S": "...",
"T": "-",
"U": "..-",
"V": "...-",
"W": ".--",
"X": "-..-",
"Y": "-.--",
"Z": "--..",
" ": "/"
}
def generator():
    print("\n******** Convert String to MorseCode ********")
    word = input("Enter a Word/Statement: ").upper()
    print("\nMorse Code:")
    for letter in word:
        if letter in morse: print(morse[letter],end= " ")
        else: print(letter,end= " ")
def reverser():
    print("\n******** Convert MorseCode to String ********")
    word = input("Enter a Morse Code: ")
    word  = word.strip().split(" ")
    rev = {}
    for key,value in morse.items(): rev.update({value:key})
    print("\nString:")
    for letter in word:
        if letter in rev: print(rev[letter],end="")
        else: print(letter.strip(),end="")
print("Press \"G\" to generate a Morse Code\n","OR".center(30),"\n  Press \"D\" to decode a Morse Code")
choice = input(": ").lower()
if choice == "g":generator()
elif choice == "d":reverser()
else: print("Invalid Input")
