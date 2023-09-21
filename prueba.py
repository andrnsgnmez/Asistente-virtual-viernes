import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import threading
import os

class ImageLabel(tk.Label):

    def load(self, im: object) -> object:
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
#tktgkgtltltglltgl
def abrirGif():
    root = tk.Tk()
    root.title = 'Comparando Imagenes'
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(os.getcwd() + 'Viernesg.gif')
    root.mainloop()

t = threading.Thread(target = abrirGif)
t.daemon = True
t.start()

# AQUI EL RESTO DEL CODIGO QUE SIGUE CORRIENDO
