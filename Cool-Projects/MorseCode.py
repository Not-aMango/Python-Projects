import pyperclip
import customtkinter as ctk
app = ctk.CTk()
ctk.set_appearance_mode('dark')
app.geometry('900x1000')

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
rev = {}
for key,value in morse.items(): rev.update({value:key})
class MorseCode():
    def __init__(self):
        #title
        self.title = ctk.CTkLabel(app,text='𝕄𝕠𝕣𝕤𝕖ℂ𝕠𝕕𝕖 𝔾𝕖𝕟𝕖𝕣𝕒𝕥𝕠𝕣',font=ctk.CTkFont(size=50,weight='bold'))
        self.bar = ctk.CTkProgressBar(app,progress_color='magenta',width=700)
        self.title.place(relx=0.5,rely=0.02,anchor='n')
        self.bar.place(relx=0.5,rely=0.08,anchor='center')

        #tab
        self.tab = ctk.CTkTabview(app,width=800,height=800,segmented_button_font=ctk.CTkFont(size=25),fg_color='transparent')
        self.tab.add('MorseCode to Text')
        self.tab.add('Text to MorseCode')
        self.tab1 = self.tab.tab('MorseCode to Text')
        self.tab2 = self.tab.tab('Text to MorseCode')
        self.tab.place(relx=0.5,rely=0.12,anchor='n')

        #entry tab1
        self.entry1 = ctk.CTkTextbox(self.tab1,width=670,font=ctk.CTkFont(size=20),fg_color='#343638',border_width=2,border_color='#53585b')
        self.entry1.place(relx=0.5,rely=0.1,anchor='n')

        #entry tab2
        self.entry2 = ctk.CTkTextbox(self.tab2, width=670, font=ctk.CTkFont(size=20), fg_color='#343638', border_width=2,border_color='#53585b')
        self.entry2.place(relx=0.5, rely=0.1, anchor='n')

        #error statement
        self.error = ctk.CTkLabel(self.tab,text='Please Input something first')

        #convert button
        self.convert_button1 = ctk.CTkButton(self.tab1,text='Convert',font=ctk.CTkFont(size=40,weight='bold'),width=180,height=45,command=self.error_layer_1)
        self.convert_button1.place(relx=0.5,rely=0.48,anchor='center')

        #convert button 2
        self.convert_button2 = ctk.CTkButton(self.tab2, text='Convert', font=ctk.CTkFont(size=40, weight='bold'),width=180, height=45,command=self.error_layer_2 )
        self.convert_button2.place(relx=0.5, rely=0.48, anchor='center')

        #display tab1
        self.display_box1 = ctk.CTkTextbox(self.tab1,font=ctk.CTkFont(size=20),width=670,fg_color='#343638',border_width=2,border_color='#53585b')
        self.display_box1.place(relx=0.5,rely=0.6,anchor='n')

        #display tab2
        self.display_box2 = ctk.CTkTextbox(self.tab2, font=ctk.CTkFont(size=20), width=670, fg_color='#343638',border_width=2, border_color='#53585b')
        self.display_box2.place(relx=0.5, rely=0.6, anchor='n')

        #copybutton
        self.copy1 = ctk.CTkButton(self.tab1,font=ctk.CTkFont(size=15),width=80,height=30,border_width=2,fg_color='transparent',command= self.clipboard1)
        self.copy2 = ctk.CTkButton(self.tab2,font=ctk.CTkFont(size=15),width=80,height=30,border_width=2,fg_color='transparent',command=self.clipboard2)

    def text_to_morse(self):
        self.copy1.place_forget()
        self.display_box1.configure(state='normal')
        self.display_box1.delete(0.0,'end')
        word = self.entry1.get(0.0,'end').upper()
        morsecode = ''
        for letter in word:
            if letter in morse:
                morsecode = morsecode + morse[letter] + " "
            else:
                morsecode = morsecode + letter + ' '
        self.display_box1.insert(0.0,morsecode)
        self.display_box1.configure(state='disable')
        self.copy1.configure(text='Copy to Clipboard')
        self.tab1.after(200,
                        lambda: self.copy1.place(relx=0.5,rely=0.95,anchor='center'))

    def morse_to_text(self):
        self.copy2.place_forget()
        self.display_box2.configure(state='normal')
        self.display_box2.delete(0.0, 'end')
        morse_statement = self.entry2.get(0.0,'end').strip().split(" ")
        text= ''
        for morse_code in morse_statement:
            if morse_code in rev:
                text = text + rev[morse_code]
            else:
                text = text + morse_code
        self.display_box2.insert(0.0, text)
        self.display_box2.configure(state='disable')
        self.copy2.configure(text='Copy to Clipboard')
        self.tab1.after(200,
                        lambda: self.copy2.place(relx=0.5, rely=0.95, anchor='center'))

    def error_layer_1(self):
        if not self.entry1.get("0.0", "end").strip():
            self.entry1.configure(border_color='red')
            self.error.configure(text_color='red')
            self.error.place(relx=0.5,rely=0.14,anchor='center')
        else:
            self.entry1.configure(border_color='#53585b')
            self.error.configure(text_color='#222222')
            self.text_to_morse()

    def error_layer_2(self):
        if not self.entry2.get("0.0", "end").strip():
            self.entry2.configure(border_color='red')
            self.error.configure(text_color='red')
            self.error.place(relx=0.5,rely=0.14,anchor='center')
        else:
            self.entry2.configure(border_color='#53585b')
            self.error.configure(text_color='#222222')
            self.morse_to_text()

    def clipboard1(self):
        self.display_box1.configure(state='normal')
        pyperclip.copy(self.display_box1.get(0.0,'end'))
        self.copy1.configure(text='MorseCode copied')
        self.display_box1.configure(state='disable')
        self.tab1.after(2000,
                         lambda: self.copy1.place_forget())

    def clipboard2(self):
        self.display_box2.configure(state='normal')
        pyperclip.copy(self.display_box2.get(0.0,'end'))
        self.copy2.configure(text='Text copied')
        self.display_box2.configure(state='disable')
        self.tab2.after(2000,
                        lambda: self.copy2.place_forget())

MorseCode()
app.mainloop()

