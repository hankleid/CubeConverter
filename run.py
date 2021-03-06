import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import images as im
from PIL import Image, ImageTk

B, G, R, O, Y, W = im.BLUE, im.GREEN, im.RED, im.ORANGE, im.YELLOW, im.WHITE

class CubeApp(tk.Tk):
    frames = {}
    subwindows = []

    def __init__(self, title, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(title)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        start = StartPage(container, self)
        start.tkraise()

    def open_window(self, title, dir):
        sub = SubCube(title, dir)
        self.subwindows.append(sub)

class SubCube(tk.Toplevel):
    img = None
    info = None
    colors = [B, G, R, O, Y, W]
    px = 90

    def __init__(self, dir, title, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title(title)
        self.directory = dir
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.img = ImageFrame(container, self)
        self.img.tkraise()
        InfoFrame(container, self).tkraise()

    def apply_changes(self):
        self.info.update_colors(self)
        self.img.refresh_img(self)
        # note: info's "update_size" is called instantaneously when user
        #       interacts with the dropdown menu, hence not called here

    def user_save(self):
        dir = asksaveasfilename(initialdir=os.getcwd())
        self.img.display.save(dir + ".png", "PNG")

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.grid(row=0, column=0, sticky="nsew")
        self.lbl_upload = tk.Label(self, text="Image:", font=("Fixedsys", 25))
        self.lbl_currentfile = tk.Label(self, text="choose file to convert",
                            font=("Arial Italic", 12), fg="red")
        # BUTTONS
        self.btn_upload = tk.Button(self, text="Upload",
                        font = ("Fixedsys", 12), bg="white", command=self.upload_image)
        self.btn_go = tk.Button(self, width=15, text="   ",
                    font=("Fixedsys", 15), state="disabled", bg="gray", command=lambda: self.go(controller))

        # ADD TO GRID
        self.lbl_upload.grid(column=0, row=0)
        self.lbl_currentfile.grid(column=1, row=0)
        self.btn_go.grid(column=1, row=1)
        self.btn_upload.grid(column=2, row=0)

    def upload_image(self):
        def parse_string(str):
            if len(str) == 0:
                return None
            elif str[-1] == '/':
                return ''
            else:
                return parse_string(str[:-1]) + str[-1]

        self.directory = askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("png files","*.png")))
        self.windowname = parse_string(self.directory)
        if self.windowname is not None:
            self.lbl_currentfile.config(text=self.windowname, fg="blue")
            self.btn_upload.config(text="Change File")
            self.btn_go.config(state="normal", text="GO!", bg="yellow")

    def go(self, controller):
        controller.open_window(self.directory, self.windowname)

class ImageFrame(tk.Frame):
    cnvs_display = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.display = self.get_display(controller)
        self.grid(row=0, column=1, sticky="nsew")
        controller.img = self
        self.display_img()

    def get_display(self, controller):
        return im.CubedImage(controller.directory, controller.colors, controller.px).final

    def display_img(self):
        self.cnvs_display = tk.Canvas(self, width=self.display.size[0], height=self.display.size[1])
        self.cnvs_display.grid(row=0, column=0)
        img = ImageTk.PhotoImage(self.display)
        imglbl = tk.Label(image=img)
        imglbl.i = img
        self.cnvs_display.create_image((0,0), image = img, anchor='nw')

    def refresh_img(self, controller):
        self.cnvs_display.delete("all")
        self.display = self.get_display(controller)
        self.display_img()


class InfoFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        controller.info = self
        self.grid(row=0, column=0, sticky="nsew")

        self.checks = {}
        self.gen_checks({"Blue": B, "Green": G, "Red": R, "Orange": O, "Yellow": Y, "White": W})

        self.lbl_choose = tk.Label(self, text="Choose Size:", font=("Fixedsys", 10), fg="gray")
        self.btn_refresh = tk.Button(self, width=15, text="Apply Changes",
                        font = ("Fixedsys", 15), bg="light gray", fg="black", command=controller.apply_changes)
        self.btn_save = tk.Button(self, width=5, text="Save",
                    font = ("Fixedsys", 20), bg="light blue", fg="blue",
                    command= controller.user_save)
        self.cb_sizes = ttk.Combobox(self, state='readonly', width=5, values=("15", "30", "45", "60", "90", "120", "150"))
        self.cb_sizes.set("90")
        self.cb_sizes.bind('<<ComboboxSelected>>', lambda event: self.update_size(event, controller))

        self.lbl_choose.pack()
        self.cb_sizes.pack()
        self.btn_refresh.pack()
        self.btn_save.pack(anchor='s')

    def gen_checks(self, colors):
        for tag, c in colors.items():
            var = tk.BooleanVar()
            check = tk.Checkbutton(self, text=tag, font="Fixedsys 15", bg="white", variable=var,
                onvalue=True, offvalue=False)
            check.var = var
            self.checks[check] = c
            check.select()
            check.pack(anchor='w')

    def update_size(self, event, controller):
        if event: controller.px = int(self.cb_sizes.get())

    def update_colors(self, controller):
        controller.colors = [color for check, color in self.checks.items() if check.var.get()]


app = CubeApp("Welcome to CubeConverter!")
app.mainloop()
