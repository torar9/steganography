import tkinter as tk
from tkinter import *
from tkinter import filedialog, Label
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
#import cv2
import numpy as np
import math

class Window:
    def __init__(self, root):
        self.fileButton = Button(app, text="Nahrát obrázek", bg='white', fg='black', command=self.fButton_click)
        self.fileButton.place(x=250, y=10)

        self.encryptButton = Button(app, text="Šifrovat", bg='white', fg='black', command=self.encrButton_click)
        self.encryptButton.place(x=340, y=220)

        self.decryptButton = Button(app, text="Dešifrovat", bg='white', fg='black', command=self.decrButton_click)
        self.decryptButton.place(x=420, y=220)

        self.textField = Text(app, wrap=WORD, width=30)
        self.textField.place(x=340, y=55, height=165)

        self.imlabel = tk.Label()
        self.imlabel.place(x=20, y=50)

        self.thumb_size = 300,300

    def fButton_click(self):
        try:
            # Otevři dialogové okno pro nahrání souboru
            self.image_path = filedialog.askopenfilename(title="Vyber obrázek", filetypes=
            [
                ('image files', ('.png', '.jpg', '.jpeg', '.webp', '.pjpeg', '.pjp'))
            ])
            print(self.image_path)
            if not self.image_path:
                return

            # Načti obrázek a vytvoř jeho miniaturu
            image = Image.open(self.image_path)
            image.thumbnail(self.thumb_size, Image.ANTIALIAS)
            thumb = ImageTk.PhotoImage(image)

            self.imlabel.image = thumb
            self.imlabel.configure(image=thumb)

        except Exception as e:
            raise Exception("Nepovedlo se načíst soubor" + str(e))

    def encrButton_click(self):
        # Získej zprávu k zašifrování
        msg = self.textField.get(1.0, "end-1c")
        # Načti obrázek
        # img = cv2.imread(path_image)
        print(msg)

    def decrButton_click(self):
        print("Todo")


if __name__ == '__main__':
    app = Tk()
    app.title = "KOSBD - Úkol č. 2"
    app.geometry('600x600')

    #Chybové okno
    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=str(val))
    tk.Tk.report_callback_exception = report_callback_exception

    myWindows = Window(app)

    app.mainloop()
