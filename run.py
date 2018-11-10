import tkinter as tk
import images as im
from PIL import Image, ImageTk

class CubeApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Welcome to CubeConverter!")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.frames[StartPage] = StartPage(container, self)
        self.frames[ImagePage] = ImagePage(container, self)

        self.show_frame(StartPage)

    def set_title(self, str):
        self.title(str)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name is ImagePage:
            frame.display_img()
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.lbl_upload = tk.Label(self, text="Image:", font=("Fixedsys", 25))
        self.lbl_currentfile = tk.Label(self, text="choose file to convert",
                            font=("Arial Italic", 10), fg="red")
        # BUTTONS
        self.btn_upload = tk.Button(self, width=15, text="Upload",
                        font = ("Fixedsys", 15), bg="white", command=self.upload_image)
        self.btn_go = tk.Button(self, width=5, text="   ",
                    font=("Fixedsys", 15), state="disabled", command=lambda: controller.show_frame(ImagePage))

        # ADD TO GRID
        self.lbl_upload.grid(column=0, row=0)
        self.lbl_currentfile.grid(column=1, row=1)
        self.btn_go.grid(column=2, row=0)
        self.btn_upload.grid(column=1, row=0)

    def upload_image(self):
        self.btn_upload.config(text="Change File")
        self.btn_go.config(state="normal", text="GO!", bg="yellow")
        self.lbl_currentfile.config(text='FILENAME', fg="blue")

class ImagePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.lbl_upload = tk.Label(self, text="Image:", font=("Fixedsys", 25))

    def display_img(self):
        self.canvas = tk.Canvas(self, width=im.DISPLAY.size[0] + 300, height=im.DISPLAY.size[1])
        self.canvas.grid(row=0, column=0)
        img = ImageTk.PhotoImage(im.DISPLAY)
        imglbl = tk.Label(image=img)
        imglbl.image = img
        # images        self.my_images = []
        # set first image on canvas
        self.canvas.create_image((0,0), image = img, anchor='nw')



app = CubeApp()
app.mainloop()
