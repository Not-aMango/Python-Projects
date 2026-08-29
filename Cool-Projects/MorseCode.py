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

        #convert button
        self.convert_button = ctk.CTkButton(self.tab,text='Convert',font=ctk.CTkFont(size=40,weight='bold'),width=180,height=45,command=self.morse_to_text)
        self.convert_button.place(relx=0.5,rely=0.52,anchor='center')

        #display tab1
        self.display_box1 = ctk.CTkTextbox(self.tab1,font=ctk.CTkFont(size=20),width=670,fg_color='#343638',border_width=2,border_color='#53585b')
        self.display_box1.place(relx=0.5,rely=0.6,anchor='n')

        #display tab2
        self.display_box2 = ctk.CTkTextbox(self.tab2, font=ctk.CTkFont(size=20), width=670, fg_color='#343638',border_width=2, border_color='#53585b')
        self.display_box2.place(relx=0.5, rely=0.6, anchor='n')

    def morse_to_text(self):
        self.display_box1.insert(0.0,'')
        word = self.entry1.get(0.0,'end').upper()
        morsecode = ''
        for letter in word:
            if letter in morse:
                morsecode = morsecode + morse[letter] + " "
            else:
                morsecode = morsecode + letter + ' '
        self.display_box1.insert(0.0,morsecode)



MorseCode()


app.mainloop()

#⇆
