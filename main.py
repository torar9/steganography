import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import Label
from tkinter.messagebox import showerror
import PIL
from PIL import ImageTk
from PIL import Image
import cv2
import numpy as np
import math

class Window:
    def __init__(self, root):
        self.root = root
        #Nastavení grafických prvků prvků v okně
        self.fileButton = Button(root, text="Nahrát obrázek", bg='white', fg='black', command=self.fButton_click)
        self.fileButton.place(x=250, y=10)

        self.encryptButton = Button(root, text="Šifrovat", bg='white', fg='black', command=self.encrButton_click)
        self.encryptButton.place(x=340, y=230)

        self.decryptButton = Button(root, text="Dešifrovat", bg='white', fg='black', command=self.decrButton_click)
        self.decryptButton.place(x=420, y=230)

        self.textLabel = Label(root, text="Zpráva:")
        self.textLabel.place(x=340, y=45)
        self.textField = Text(root, wrap=WORD, width=30)
        self.textField.place(x=340, y=65, height=165)

        self.imgLabel = Label(root, text="Obrázek:")
        self.imgLabel.place(x=10, y=45)

        self.imgHolder = Label(root)
        self.imgHolder.place(x=20, y=65)

        self.thumb_size = 300,300
        self.image_path = ""

    #Metoda se zavolá po kliku na tlačítko určené pr
    def fButton_click(self):
        try:
            # Otevři dialogové okno pro nahrání souboru
            self.image_path = filedialog.askopenfilename(title="Vyber obrázek", filetypes=
            [
                ('image files', ('.png', '.jpg', '.jpeg', '.webp', '.pjpeg', '.pjp'))
            ])
            if not self.image_path or self.image_path is None or self.image_path == "":
                return

            # Načti obrázek a vytvoř jeho miniaturu
            image = Image.open(self.image_path)
            image.thumbnail(self.thumb_size, Image.ANTIALIAS)
            thumb = ImageTk.PhotoImage(image)

            self.imgHolder.image = thumb
            self.imgHolder.configure(image=thumb)
            image.close()

        except Exception as e:
            raise Exception("Nepovedlo se načíst soubor" + str(e))

    def encrButton_click(self):
        if not self.image_path or self.image_path is None or self.image_path == "":
            raise Exception("Je nutné nejprve vybrat obrázek")
            return

        # Získej řetězec k zašifrování
        msg = self.textField.get(1.0, "end-1c")
        img = cv2.imread(self.image_path)

        #Transformuj jednotlivé znaky do binární podoby podle ASCII hodnot
        msg = [format(ord(i), '08b') for i in msg]
        _, width, _ = img.shape

        #Spočítám kolik pixelů potřebuji -> pro každý znak potřebuji 3 pixely(do každého pixelu uložím 3 bity) -> počet znaků * 3
        PixReq = len(msg) * 3

        #Spočítám počet řádků které budou potřeba
        RowReq = PixReq / width
        #Zaokrouhlím výsledek
        RowReq = math.ceil(RowReq)

        if((len(img) * len(img[0])) < PixReq):
            raise Exception("Obrázek je pro zakódování zprávy příliš malý")

        #pomocné čítače
        count = 0
        charCount = 0

        # Procházím přes řádky v obrázku
        for i in range(RowReq + 1):
            #Procházím přes pole znaků
            while (count < width and charCount < len(msg)):
                character = msg[charCount]
                charCount += 1
                #Procházím bity ve znaku
                for k_index, k in enumerate(character):

                    #Pokud je hodnota bitu 1 a hodnota pixelu je sudá, pak odečtu z pixelu 1, abych udělal lichou hodnotu pixelu
                    if ((k == '1' and img[i][count][k_index % 3] % 2 == 0) or
                            (#Stejně tak pokud je hodnota bitu 0 a hodnota pixelu je lichá, pak opět odečtu 1 od hodnoty pixelu a získám tak sudou hodnotu pixelu
                            k == '0' and img[i][count][k_index % 3] % 2 == 1)):
                        img[i][count][k_index % 3] -= 1 #Odečet 1 od hodnoty pixelu v obrázku

                    if (k_index % 3 == 2):
                        count += 1

                    #Kontroluji zda index bitu je 7 (poslední bit ve znaku)
                    if (k_index == 7):
                        #Nastavím ukončovací bit
                        if (charCount * 3 < PixReq and img[i][count][2] % 2 == 1):
                            #V případě že musím zakódovat další pixel tak nastavím poslední bit na 0
                            img[i][count][2] -= 1

                        if (charCount * 3 >= PixReq and img[i][count][2] % 2 == 0):
                            # V případě že jsem už zakódoval všechny znaky tak nastavím poslední bit na 1
                            img[i][count][2] -= 1#Změním hodnotu posledního bitu na 1 odečetením 1 od stávající hodnoty
                        count += 1

            count = 0

        save_location = filedialog.asksaveasfile(mode='w', initialfile="encrypted_image", defaultextension=".png", filetypes=
            [
                ('image files', ('.png', '.jpg', '.jpeg', '.webp', '.pjpeg', '.pjp'))
            ])
        if save_location is None or not save_location or save_location == "":
            return
        self.encrypted_image = img

        #Odstraním již existující soubor
        #os.remove(save_location.name)
        #Uložím obrázek na disk
        cv2.imwrite(save_location.name, img)

    def decrButton_click(self):
        if not self.image_path or self.image_path is None or self.image_path == "":
            raise Exception("Je nutné nejprve vybrat obrázek")
            return

        #Načtení miniatury obrázku
        load = Image.open(self.image_path)
        load.thumbnail(self.thumb_size, Image.ANTIALIAS)
        load = np.asarray(load)
        load = Image.fromarray(np.uint8(load))
        render = ImageTk.PhotoImage(load)
        load.close()

        #Nastavení miniatury v GUI
        self.imgHolder.image = render
        self.imgHolder.configure(image=render)

        #Načtení obrázku
        img = cv2.imread(self.image_path)
        data = []
        stop = False
        #Procházím přes řádky v obrázku
        for index_i, i in enumerate(img):
            i.tolist()
            #Procházím přes pixely v řádku
            for index_j, j in enumerate(i):
                if ((index_j) % 3 == 2):
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])

                    #Zkontroluji, zda se jedná o ukončující pixel(poslední bit = 1), pokud ano pak ukončím dešifrování
                    if (bin(j[2])[-1] == '1'):
                        stop = True
                        break
                else:
                    #Přidám do seznamu poslední bit R,G a B hodnot z pixelu
                    data.append(bin(j[0])[-1])
                    data.append(bin(j[1])[-1])
                    data.append(bin(j[2])[-1])
            if (stop):
                break

        result = []

        #Transformuj bity do ASCII hodnot po 8 bitech -> 8 bitů = 1 znak
        for i in range(int((len(data) + 1) / 8)):
            result.append(data[i * 8:(i * 8 + 8)])

        #Spoj znaky do řetězce
        result = [chr(int(''.join(i), 2)) for i in result]
        result = ''.join(result)

        self.textField.delete(1.0, "end")
        self.textField.insert(1.0, result)


if __name__ == '__main__':
    app = Tk()
    app.title = "KOSBD - Úkol č. 2"
    app.geometry('600x300')

    #Nastavení chybového okna
    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=str(val))
    tk.Tk.report_callback_exception = report_callback_exception

    myWindows = Window(app)

    app.mainloop()
