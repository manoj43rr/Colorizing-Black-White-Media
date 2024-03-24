import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import numpy as np
import cv2

root = tk.Tk()
root.title("CONVERT-WHITE")
root.iconbitmap(r"C:\my documents\my works\project\icons8-torch-64.ico")
root.configure(bg="#0C1A1A")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Set the size and position of the window to fit the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

def img():
    os.system("python img.py")

def vid():
    os.system("python vid.py")

# Main Title
title_label = tk.Label(root, text="Convert-White", fg="#6ACFC7", bg="#0C1A1A", font=("Algerian", 65, "underline"))
title_label.place(x=40, y=60)

# Description
description_label = tk.Label(root, text="Convert your Black & White images and videos here",fg="#6ACFC7", bg="#0C1A1A", font=("times", 36, "underline"))
description_label.place(x=140, y=230)

# Image Conversion Section
image_label = tk.Label(root, text="If you want to convert images", fg="#6ACFC7", bg="#0C1A1A", font=("times", 28))
image_label.place(x=180, y=370)

img_button = tk.Button(root, text="Click me", bg="#6ACFC7", fg="#0C1A1A", command=img, font = ("times", 18))
img_button.place(x=355, y=500)

# Video Conversion Section
video_label = tk.Label(root, text="If you want to convert videos", fg="#6ACFC7", bg="#0C1A1A", font=("times", 28))
video_label.place(x=860, y=370)

vid_button = tk.Button(root, text="Click me", bg="#6ACFC7", fg="#0C1A1A", command = vid,font = ("times", 18))
vid_button.place(x=1055, y=500)

root.mainloop()
