import pyperclip
import customtkinter as ctk
from customtkinter import CTkFont

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Morse Code Studio")
app.geometry("1150x760")
app.minsize(950, 650)

morse = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..", " ": "/"
}

rev = {}
for key,value in morse.items(): rev.update({value:key})

class MorseCode():
    def __init__(self):
        #Title
        self.title = ctk.CTkLabel(app,text='MorseCode Generator',font=ctk.CTkFont(size=35,weight='bold'))
        self.title.place(relx=0.18,rely=0.03,anchor='center')
        self.subtitle = ctk.CTkLabel(app,text='Translate between MorseCode and Text',font=ctk.CTkFont(size=15,weight='bold'),text_color='#767575')
        self.subtitle.place(relx=0.155,rely=0.065,anchor='center')

        #MorseCode to Text
        #frame1
        self.frame1 = ctk.CTkFrame(app,width=520,height=660,corner_radius=22)
        self.frame1.place(relx=0.26,rely=0.53,anchor='center')

        #frame-text1
        self.farmetext1 = ctk.CTkLabel(self.frame1,text='Text → Morse',font=ctk.CTkFont(size=27,weight='bold'))
        self.farmetext1.place(relx=0.22,rely=0.05,anchor='center')
        self.frame_subtext1= ctk.CTkLabel(self.frame1,text='Generate MorseCode from Text',text_color='#9e9e9e')
        self.frame_subtext1.place(relx=0.23,rely=0.09,anchor='center')

        #textbox1
        self.textbox1 = ctk.CTkTextbox(self.frame1,font=CTkFont(size=18),width=470,height=180,border_width=1,border_color='#5d5d5d',corner_radius=10,text_color='#a4a4a4')
        self.textbox1.place(relx=0.5,rely=0.28,anchor='center')
        self.textbox1.bind("<KeyRelease>", self.update_characters1)

        #characters1
        self.character_label1 = ctk.CTkLabel(self.frame1,text='Characters: 0',text_color='#8b8b8b')
        self.character_label1.place(relx=0.12,rely=0.425,anchor='n')
        self.result_label1 = ctk.CTkLabel(self.frame1,text='Result:',text_color='#8b8b8b')
        self.result_label1.place(relx=0.056,rely=0.57,anchor='w')

        #convert button 1
        self.convert1 = ctk.CTkButton(self.frame1,text='Convert',width=380,height=40,font=ctk.CTkFont(size=25,weight='bold'),command=self.error_fallback1)
        self.convert1.place(relx=0.05,rely=0.5,anchor='w')

        #clear button 1
        self.clear1 = ctk.CTkButton(self.frame1,text='Clear',width=80,height=40,font=ctk.CTkFont(size=20),fg_color='transparent',border_width=2,text_color='#a4a4a4',command= self.clearfunc1)
        self.clear1.place(relx=0.95,rely=0.5,anchor='e')

        #display box 1
        self.displaybox1 = ctk.CTkTextbox(self.frame1,font=CTkFont(size=18),width=470,height=180,border_width=1,border_color='#5d5d5d',corner_radius=10,text_color='#a4a4a4',state='disable')
        self.displaybox1.place(relx=0.5,rely=0.739,anchor='center')

        #copy button1
        self.copy1 = ctk.CTkButton(self.frame1,text='Copy',font=CTkFont(size=20),fg_color='transparent',border_width=1,text_color='#a4a4a4',width=80,
                                   command= self.copy1_func)
        self.copy1.place(relx=0.87,rely=0.93,anchor='center')

        # fancy texts 1
        self.generated = ctk.CTkLabel(self.frame1, text_color='#60a66a', text='● Generated')
        self.enter_text_1 = ctk.CTkLabel(self.frame1,text_color='#ff2727',text= '● Enter Text')

        #Text to MorseCode
        # frame2
        self.frame2 = ctk.CTkFrame(app, width=520, height=660,corner_radius=22)
        self.frame2.place(relx=0.74, rely=0.53, anchor='center')

        # frame-text2
        self.farmetext2 = ctk.CTkLabel(self.frame2, text='Morse → Text', font=CTkFont(size=27, weight='bold'))
        self.farmetext2.place(relx=0.22, rely=0.05, anchor='center')
        self.frame_subtext2 = ctk.CTkLabel(self.frame2, text='Generate Text from MorseCode', text_color='#9e9e9e')
        self.frame_subtext2.place(relx=0.23, rely=0.09, anchor='center')

        #textbox2
        self.textbox2 = ctk.CTkTextbox(self.frame2, font=CTkFont(size=18), width=470, height=180, border_width=1,border_color='#5d5d5d', corner_radius=10,text_color='#a4a4a4')
        self.textbox2.place(relx=0.5, rely=0.28, anchor='center')
        self.textbox2.bind("<KeyRelease>", self.update_characters2)

        # characters2
        self.character_label2 = ctk.CTkLabel(self.frame2, text='Morses: 0',text_color='#8b8b8b')
        self.character_label2.place(relx=0.1, rely=0.425, anchor='n')
        self.result_label2 = ctk.CTkLabel(self.frame2, text='Result:', text_color='#8b8b8b')
        self.result_label2.place(relx=0.056, rely=0.57, anchor='w')

        # convert button 2
        self.convert2 = ctk.CTkButton(self.frame2, text='Convert', width=380, height=40,font=ctk.CTkFont(size=25, weight='bold'),command=self.error_fallback2)
        self.convert2.place(relx=0.05, rely=0.5, anchor='w')

        # clear button 2
        self.clear2 = ctk.CTkButton(self.frame2, text='Clear', width=80, height=40,font=ctk.CTkFont(size=20), fg_color='transparent', border_width=2,text_color='#a4a4a4',command= self.clearfunc2)
        self.clear2.place(relx=0.95, rely=0.5, anchor='e')

        # display box 2
        self.displaybox2 = ctk.CTkTextbox(self.frame2, font=CTkFont(size=18), width=470, height=180, border_width=1,border_color='#5d5d5d', corner_radius=10,text_color='#a4a4a4',state='disable')
        self.displaybox2.place(relx=0.5, rely=0.739, anchor='center')

        # copy button 2
        self.copy2 = ctk.CTkButton(self.frame2, text='Copy', font=CTkFont(size=20), fg_color='transparent',border_width=1, text_color='#a4a4a4', width=80,
                                   command= self.copy2_func)
        self.copy2.place(relx=0.87, rely=0.93, anchor='center')

        #fancy texts 2
        self.generated2 = ctk.CTkLabel(self.frame2,text_color='#60a66a',text= '● Generated')
        self.enter_text_2 = ctk.CTkLabel(self.frame2,text_color='#ff2727',text= '● Enter MorseCode')

    def text_to_morse(self):
        self.displaybox1.configure(state='normal')
        self.displaybox1.delete(0.0,'end')
        word = self.textbox1.get(0.0, 'end').upper()

        morsecode = ''
        for letter in word:
            if letter in morse: morsecode = morsecode + morse[letter] + ' '
            else: morsecode = morsecode + letter + ' '
        self.displaybox1.insert(0.0, morsecode)
        self.displaybox1.configure(state='disable')

        self.generated.place(relx=0.11, rely=0.92, anchor='center')

    def morse_to_text(self):
        self.displaybox2.configure(state='normal')
        self.displaybox2.delete(0.0, 'end')
        morse_statement = self.textbox2.get(0.0, 'end').strip().split(" ")

        text = ''
        for morse_code in morse_statement:
            if morse_code in rev: text = text + rev[morse_code]
            else: text = text + morse_code
        self.displaybox2.insert(0.0, text)
        self.displaybox2.configure(state='disable')

        self.generated2.place(relx=0.11, rely=0.92, anchor='center')

    def error_fallback1(self):
        self.copy1.configure(text='Copy')
        if self.textbox1.get(1.0,'end').strip() == '':
            self.textbox1.configure(border_color='red')
            self.generated.place_forget()
            self.enter_text_1.place(relx=0.13, rely=0.92, anchor='center')
            self.displaybox1.configure(state='normal')
            self.displaybox1.delete(0.0,'end')
            self.displaybox1.configure(state='disable')
        else:
            self.enter_text_1.place_forget()
            self.textbox1.configure(border_color='#5d5d5d')
            self.text_to_morse()
    def error_fallback2(self):
        self.copy2.configure(text='Copy')
        if self.textbox2.get(1.0,'end').strip() == '':
            self.textbox2.configure(border_color='red')
            self.generated2.place_forget()
            self.enter_text_2.place(relx=0.13, rely=0.92, anchor='center')
            self.displaybox2.configure(state='normal')
            self.displaybox2.delete(0.0,'end')
            self.displaybox2.configure(state='disable')
        else:
            self.enter_text_2.place_forget()
            self.textbox2.configure(border_color='#5d5d5d')
            self.morse_to_text()

    def copy1_func(self):
        if self.textbox1.get(0.0,'end').strip() == '':
            self.textbox1.configure(border_color='red')
            self.generated.place_forget()
            self.enter_text_1.place(relx=0.13, rely=0.92, anchor='center')
            self.displaybox1.configure(state='normal')
            self.displaybox1.delete(0.0, 'end')
            self.displaybox1.configure(state='disable')
        else:
            self.enter_text_1.place_forget()
            pyperclip.copy(self.displaybox1.get('1.0', 'end'))
            self.copy1.configure(text='Copied')
    def copy2_func(self):
        if self.textbox2.get(0.0, 'end').strip() == '':
            self.textbox2.configure(border_color='red')
            self.generated2.place_forget()
            self.enter_text_2.place(relx=0.13, rely=0.92, anchor='center')
            self.displaybox2.configure(state='normal')
            self.displaybox2.delete(0.0, 'end')
            self.displaybox2.configure(state='disable')
        else:
            self.enter_text_2.place_forget()
            pyperclip.copy(self.displaybox2.get('1.0', 'end'))
            self.copy2.configure(text='Copied')

    def clearfunc1(self):
        self.textbox1.delete(0.0,'end')
        self.displaybox1.configure(state='normal')
        self.displaybox1.delete(0.0, 'end')
        self.displaybox1.configure(state='disable')
        self.update_characters1()
        self.copy1.configure(text='Copy')
        self.generated.place_forget()
        self.textbox1.configure(border_color='#5d5d5d')
    def clearfunc2(self):
        self.textbox2.delete(0.0, 'end')
        self.displaybox2.configure(state='normal')
        self.displaybox2.delete(0.0, 'end')
        self.displaybox2.configure(state='disable')
        self.update_characters2()
        self.copy2.configure(text='Copy')
        self.generated2.place_forget()
        self.textbox2.configure(border_color='#5d5d5d')

    def update_characters1(self,event=None):
        characters = len(self.textbox1.get('1.0','end')) - 1
        self.character_label1.configure(text=f'Characters: {characters}')
    def update_characters2(self,event=None):
        characters = len(self.textbox2.get('1.0','end').split())
        self.character_label2.configure(text=f'Morses: {characters}')

MorseCode()
app.mainloop()
