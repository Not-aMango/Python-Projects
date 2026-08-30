import customtkinter as ctk
import qrcode
from tkinter import filedialog
from pathlib import Path

app = ctk.CTk()
app.geometry('900x1000')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Qr_gui():
    def __init__(self):
        #title
        self.title = ctk.CTkLabel(app,text='ℚ𝕣𝕚𝕗𝕪',font=ctk.CTkFont(size=50,weight='bold'),fg_color='transparent',text_color='#f2f2f2')
        self.subtext = ctk.CTkLabel(app,text='- 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚎 𝚀𝚁-𝚌𝚘𝚍𝚎𝚜 𝚒𝚗𝚜𝚝𝚊𝚗𝚝𝚕𝚢',font=ctk.CTkFont(size=25,weight='bold'),
                                    fg_color='transparent',text_color='#9da3ae')
        self.title_bar = ctk.CTkProgressBar(app,width=125,progress_color='cyan')

        #entry
        self.entry_frame = ctk.CTkFrame(app,width=600,height=170,fg_color='transparent')
        self.entry = ctk.CTkEntry(self.entry_frame,
                                  width=500,height=45,corner_radius=10,
                                  font=ctk.CTkFont(size=20),placeholder_text='Enter URL: https://example.com')
        self.entry_button = ctk.CTkButton(self.entry_frame,text='Generate QrCode',height=45,corner_radius=7,
                                          font=ctk.CTkFont(size=23,),fg_color='indigo',hover_color='#430371',command=self.qr_generator)
        self.entry_fallback = ctk.CTkLabel(self.entry_frame,text='Please enter a URL or text')

        #qr code card block
        self.qr = None
        self.qr_block = ctk.CTkFrame(app, width=420,height=420)
        self.qr_label = ctk.CTkLabel(self.qr_block,text='Generate a\nQR-code\nto preview it here',font=ctk.CTkFont(size=30),image=None)

        #saving buttons
        self.save_frame = ctk.CTkFrame(app,width=500,height=200,fg_color='transparent')
        self.generated_or_not = ctk.CTkLabel(self.save_frame,text='QR-code Generated',font=ctk.CTkFont(size=20))
        self.save_button = ctk.CTkButton(self.save_frame,text='Save',width=100,height=30,font=ctk.CTkFont(size=25),command=self.saver)
        self.save_path = ctk.CTkLabel(self.save_frame,text='',height=22,font=ctk.CTkFont(size=18))


    def header_placement(self):
        self.title.place(relx=0.05,rely=0.04,anchor='w')
        self.subtext.place(relx=0.2,rely=0.05,anchor='w')
        self.title_bar.place(relx=0.05,rely=0.075)
    def input_cards(self):
        self.entry_frame.place(relx=0.5,rely=0.2,anchor='center')
        self.entry.place(relx=0.5,rely=0.3,anchor='center')
        self.entry_button.place(relx=0.5,rely=0.65,anchor='center')
    def qr_card(self):
        self.qr_block.place(relx=0.5,rely=0.3,anchor='n')
        self.qr_label.place(relx=0.5,rely=0.5,anchor='center')

    def saver_gui(self):
        self.save_frame.after(300,
                              lambda: self.save_frame.place(relx=0.5,rely=0.72,anchor='n'),)
        self.generated_or_not.place(relx=0.5,rely=0.02,anchor='n')
        self.save_frame.after(600,
                              lambda: self.save_button.place(relx=0.5,rely=0.4,anchor='center'))
        self.save_path.place(relx=0.5,rely=0.7,anchor='center')
    def saver(self):
        filepath = filedialog.asksaveasfilename(defaultextension='.png',
                                            filetypes=[("PNG-Image", "*.png")],
                                            initialdir=Path.home())
        self.qr.save(filepath)
        text = f'Saved to: {filepath}'
        self.save_path.configure(text=text)
        self.entry.delete(0, 'end')

    def qr_generator(self):
        self.save_path.configure(text='')
        self.save_path.place_forget()
        self.save_button.place_forget()
        self.generated_or_not.place_forget()

        if self.entry.get() == '':
            self.entry.configure(border_color='red')
            self.entry_fallback.configure(text_color='red')
            self.entry_fallback.place(relx=0.5,rely=0.08,anchor='center')
        if self.entry.get() != '':
            self.entry.configure(border_color='#565b5e')
            self.entry_fallback.configure(text_color='#222222')

            #generating qr code
            self.qr = qrcode.make(self.entry.get())
            qr_gui_image = self.qr.resize((400, 400))
            qr_image_card = ctk.CTkImage(light_image=qr_gui_image, dark_image=qr_gui_image, size=(400, 400))
            self.qr_label.configure(image=qr_image_card, text="")
            self.saver_gui()


    def run(self):
        self.header_placement()
        self.input_cards()
        self.qr_card()

Qr_gui().run()

#loops
app.mainloop()
