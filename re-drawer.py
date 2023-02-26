from tkinter import *
import customtkinter as ct
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter import filedialog
import webbrowser
import cv2
import shutil
import random
import math
from ascii_magic import AsciiArt

icon = 'files\icon.ico'
gitimg = "files\\git.png"
openPath = ""
savePath = ""
defaultPath = "files\\cartoonIMG.jpg"
defaultTextPath = "files\\ascii_image.txt"

def WinProperties(win):
    win.geometry("700x550+560+240")  # place and scale
    win.title("Image modificator")  # name of the window
    win.resizable(False, False)  # deformation of the window
    win.minsize(700,550)
    win.iconbitmap(f'{icon}')  # icon
    ct.set_appearance_mode('dark')
    ct.set_default_color_theme('green')


def ThemeChanger(choice):
    if choice == "dark":
        ct.set_appearance_mode('dark')
        canvas.configure(background='#262626')
    if choice == "light":
        ct.set_appearance_mode('light')
        canvas.configure(background='#C8C8C8')


def Git():
    webbrowser.open('https://github.com/Nick-Vinesmoke', new=2)


def OpenFile():
    global openPath
    openPath = filedialog.askopenfilename()
    if ".jpg" in openPath or ".png" in openPath:
        print(openPath)
        canvas.delete(ALL)
        image = Image.open(f'{openPath}')
        (width, height) = image.size
        while width > 800 or height > 520 :
            image = image.resize((int(width/1.1),int(height/1.1)))
            (width, height) = image.size
        image = ImageTk.PhotoImage(image)
        canvas.create_image(800/2, 529/2, image=image)
        canvas.update(ALL)
    else:
        canvas.delete(ALL)
        error = ct.CTkLabel(master=win, text='I can\' open this file',
                    font=('Arial Rounded MT bold', 36))
        error.place(relx=0.5, rely=0.5, anchor=CENTER)
        error.after(1000, error.destroy)


def ReDrow():

    global openPath
    global setStyle
    print(setStyle.get())
    if (setStyle.get() == "cartoon"):
        img = cv2.imread(f"{openPath}")# reading image
        # Edges
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        # Cartoonization
        color = cv2.bilateralFilter(img, 6, 250, 250)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        cv2.imwrite(defaultPath, cartoon)
    if (setStyle.get() == "pixel art"):
        def pixelate(input_file_path, pixel_size):
            image = Image.open(input_file_path)
            rgb_im = image.convert('RGB')
            rgb_im = rgb_im.resize(
                (rgb_im.size[0] // pixel_size, rgb_im.size[1] // pixel_size),
                Image.NEAREST
            )
            rgb_im = rgb_im.resize(
                (rgb_im.size[0] * pixel_size, rgb_im.size[1] * pixel_size),
                Image.NEAREST
            )

            rgb_im.save(f"{defaultPath}")

        pixelate(f"{openPath}", 8)
    if (setStyle.get() == "ascii color art"):
        BACK_COLOR = "BLACK"
        IN_IMG = openPath
        FNT = ImageFont.truetype('files/font.TTF', 7)

        im = Image.open(IN_IMG)
        (width, height) = im.size

        line = math.ceil(im.size[0] / 50 * 13 * 1.2)
        row = math.ceil(im.size[1] / 50 * 6 * 1.2)

        string = ''
        for i in range(row):
            for j in range(line):
                string += str(random.choice([0, 1]))
            string += '\n'

        img = Image.new('RGBA', (im.size[0], im.size[1]), BACK_COLOR)
        draw_text = ImageDraw.Draw(img)
        draw_text.text((1, 1), string, spacing=1, font=FNT, fill=0)
        img2 = Image.open(IN_IMG)
        try:
            alphaComposited = Image.alpha_composite(img2, img)

            image = alphaComposited
            new_image = Image.new("RGBA", image.size, BACK_COLOR)
            new_image.paste(image, (0, 0), image)
            new_image.convert('RGB').save(defaultPath, "JPEG")
        except:
            error = ct.CTkLabel(master=win, text='Image has wrong mode', font=('Arial Rounded MT bold', 36))
            error.place(relx=0.5, rely=0.5, anchor=CENTER)
            error.after(3000, error.destroy)
        else:
            alphaComposited = Image.alpha_composite(img2, img)

            image = alphaComposited
            new_image = Image.new("RGBA", image.size, BACK_COLOR)
            new_image.paste(image, (0, 0), image)
            new_image.convert('RGB').save(defaultPath, "JPEG")



    if (setStyle.get() == "ascii art"):
            # pass the image as command line argument
            image_path = openPath
            img = Image.open(image_path)

            # resize the image
            width, height = img.size
            aspect_ratio = height / width
            new_width = 120
            new_height = aspect_ratio * new_width * 0.55
            img = img.resize((new_width, int(new_height)))
            # new size of image
            # print(img.size)

            # convert image to greyscale format
            img = img.convert('L')

            pixels = img.getdata()

            # replace each pixel with a character from array
            chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."]
            new_pixels = [chars[pixel // 25] for pixel in pixels]
            new_pixels = ''.join(new_pixels)

            # split string of chars into multiple strings of length equal to new width and create a list
            new_pixels_count = len(new_pixels)
            ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
            ascii_image = "\n".join(ascii_image)
            print(ascii_image)

            # write to a text file.
            with open(defaultTextPath, "w") as f:
                f.write(ascii_image)

    # add to canvas
    canvas.delete(ALL)
    if (setStyle.get() != "ascii art"):
        image = Image.open(f'{defaultPath}')
        (width, height) = image.size
        while width > 800 or height > 520:
            image = image.resize((int(width / 1.1), int(height / 1.1)))
            (width, height) = image.size
        image = ImageTk.PhotoImage(image)
        canvas.create_image(800 / 2, 529 / 2, image=image)
        canvas.update(ALL)
    else:
        success = ct.CTkLabel(master=win, text='File.txt created successfully',font=('Arial Rounded MT bold', 36))
        success.place(relx=0.5, rely=0.5, anchor=CENTER)
        success.after(2000, success.destroy)



def SaveImage():
    global savePath
    global defaultPath
    if (setStyle.get() != "ascii art"):
        savePath = filedialog.asksaveasfilename(initialdir="files\\",
                                                filetypes=[("jpeg files", ".jpg .jpeg"), ("png files", ".png")],
                                                initialfile="cartoonIMG.jpg")
        try:
            shutil.move(defaultPath, savePath)
        except:
            error = ct.CTkLabel(master=win, text='Error', font=('Arial Rounded MT bold', 36))
            error.place(relx=0.5, rely=0.5, anchor=CENTER)
            error.after(1000, error.destroy)
        else:
            shutil.move(defaultPath, savePath)
            canvas.delete(ALL)
            error = ct.CTkLabel(master=win, text='Saved', font=('Arial Rounded MT bold', 36))
            error.place(relx=0.5, rely=0.5, anchor=CENTER)
            error.after(1000, error.destroy)
    else:
        savePath = filedialog.asksaveasfilename(initialdir="files\\",initialfile="ascii_image.txt")
        try:
            shutil.move(defaultTextPath, savePath)
        except:
            error = ct.CTkLabel(master=win, text='Error', font=('Arial Rounded MT bold', 36))
            error.place(relx=0.5, rely=0.5, anchor=CENTER)
            error.after(1000, error.destroy)
        else:
            shutil.move(defaultPath, savePath)
            canvas.delete(ALL)
            error = ct.CTkLabel(master=win, text='Saved', font=('Arial Rounded MT bold', 36))
            error.place(relx=0.5, rely=0.5, anchor=CENTER)
            error.after(1000, error.destroy)


win = ct.CTk()
setTheme = ct.StringVar(value="dark")
setStyle = ct.StringVar(value="cartoon")

WinProperties(win)
canvas = Canvas(master=win,width=800, height=520, background='#262626', highlightthickness=0)
ct.CTkFrame(master=win, width= 690,height=50,fg_color = "#242424").place(relx= 0.5,rely= 0.95,anchor=CENTER)
ct.CTkFrame(master=win, width= 690,height=69,fg_color = "#242424").place(relx= 0.5,rely=0.065,anchor=CENTER)
canvas.place(relx=0.5, rely=0.52, anchor=CENTER)
gitimage = ct.CTkImage(light_image=Image.open(gitimg),dark_image=Image.open(gitimg),size=(30, 30))
ct.CTkLabel(master=win,text = 'AI which redraw your photos in selected style',font=('Arial Rounded MT bold', 24)).place(relx= 0.5,rely= 0.03,anchor=CENTER)
ct.CTkButton(master=win,text = 'load image',font=('Arial Rounded MT bold', 18),command=OpenFile).place(relx= 0.2,rely= 0.1,anchor=CENTER)
ct.CTkButton(master=win,text = 'save image',font=('Arial Rounded MT bold', 18),command=SaveImage).place(relx= 0.5,rely= 0.1,anchor=CENTER)
ct.CTkButton(master=win,text = 'redraw',font=('Arial Rounded MT bold', 18),command=ReDrow).place(relx= 0.8,rely= 0.1,anchor=CENTER)
ct.CTkComboBox(master=win,values=["dark","light"],variable=setTheme,command=ThemeChanger,height = 40).place(relx= 0.186,rely= 0.95,anchor=CENTER)
ct.CTkButton(master=win,text = '',image=gitimage,font=('Arial Rounded MT bold', 18),width = 1,command=Git,corner_radius = 8).place(relx= 0.05,rely= 0.95,anchor=CENTER)
ct.CTkLabel(master=win,text = 'Select style:',font=('Arial Rounded MT bold', 18)).place(relx= 0.7,rely= 0.95,anchor=CENTER)
ct.CTkComboBox(master=win,values=["cartoon","pixel art","ascii color art","ascii art"],variable=setStyle,height = 40).place(relx= 0.88,rely= 0.95,anchor=CENTER)

win.mainloop()
