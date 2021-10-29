import tkinter as tk
from tkinter import *
from tkinter import filedialog, Label
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import cv2
import numpy as np
import math

class Window:
    def __init__(self, root):
        #Nastavení GUI prvků v okně
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
        # Získej řetězec k zašifrování
        msg = self.textField.get(1.0, "end-1c")
        img = cv2.imread(self.image_path)
        print(msg)

        #Transformuj text do ASCII a následně do binární podoby
        msg = [format(ord(i), '08b') for i in msg]
        _, width, _ = img.shape
        print(img.shape)
        print(msg)

        #Spočítám kolik pixelů potřebuji -> pro každý znak potřebuji 3 pixely -> počet znaků * 3
        PixReq = len(msg) * 3

        #Spočítám počet řádků které budou potřeba
        RowReq = PixReq / width
        #Zaokrouhlím výsledek
        RowReq = math.ceil(RowReq)

        #pomocné čítače
        count = 0
        charCount = 0

        # Procházím přes řádky v obrázku
        for i in range(RowReq + 1):
            #Procházím přes pole znaků
            while (count < width and charCount < len(msg)):
                char = msg[charCount]
                charCount += 1

                #Procházím bity jednotlivých znaků
                for index_k, k in enumerate(char):

                    #Pokud je hodnota bitu 1 a hodnota pixelu je sudá, pak odečtu z pixelu 1, abych udělal lichou hodnotu pixelu
                    if ((k == '1' and img[i][count][index_k % 3] % 2 == 0) or
                            (#Stejně tak pokud je hodnota bitu 0 a hodnota pixelu je lichá, pak opět odečtu 1 od hodnoty pixelu a získám tak sudou hodnotu pixelu
                            k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                        img[i][count][index_k % 3] -= 1 #Odečet 1 od hodnoty pixelu v obrázku

                    if (index_k % 3 == 2):
                        count += 1

                    #Kontroluji zda index bitu je 7 (předposlední bit znaku)
                    if (index_k == 7):
                        #Zkontroluji zda zbývá další znak k zakódování
                        if (charCount * 3 < PixReq and img[i][count][2] % 2 == 1):
                            img[i][count][2] -= 1
                        if (charCount * 3 >= PixReq and img[i][count][2] % 2 == 0):
                            img[i][count][2] -= 1
                        count += 1

            count = 0
        cv2.imwrite("img/encrypted_image.png", img)

    def decrButton_click(self):
        #Načtení miniatury obrázku
        load = Image.open("img/encrypted_image.png")
        load.thumbnail(self.thumb_size, Image.ANTIALIAS)
        load = np.asarray(load)
        load = Image.fromarray(np.uint8(load))
        render = ImageTk.PhotoImage(load)

        #Nastavení miniatury v GUI
        self.imlabel.image = render
        self.imlabel.configure(image=render)

        #Načtení obrázku
        img = cv2.imread("img/encrypted_image.png")
        data = []
        stop = False
        #Procházím řádky obrázku
        for index_i, i in enumerate(img):
            i.tolist()
            #Procházím přes jednotlivé hodnoty v pixelu
            for index_j, j in enumerate(i):
                #Kontroluji vždy binární hodnoty 3 pixelů, které reprezentují jeden znak
                if ((index_j) % 3 == 2):
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])

                    #Zkontroluji zda se jedná o ukončující pixel, pokud ano pak ukončím dešifrování
                    if (bin(j[2])[-1] == '1'):
                        stop = True
                        break
                else:
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    data.append(bin(j[2])[-1])
            if (stop):
                break

        message = []

        #Transformuj bity do ASCII hodnot po 8 bitech -> 8 bitů = 1 znak
        for i in range(int((len(data) + 1) / 8)):
            message.append(data[i * 8:(i * 8 + 8)])

        #Spoj znaky do řetězce
        message = [chr(int(''.join(i), 2)) for i in message]
        message = ''.join(message)

        print("Decrypted:" + message)


if __name__ == '__main__':
    app = Tk()
    app.title = "KOSBD - Úkol č. 2"
    app.geometry('600x600')

    #Nastavení chybového okna
    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=str(val))
    tk.Tk.report_callback_exception = report_callback_exception

    myWindows = Window(app)

    app.mainloop()
