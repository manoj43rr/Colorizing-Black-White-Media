import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from PIL import Image, ImageTk 
import os
import numpy as np
import cv2
from skimage.color import rgb2lab, deltaE_cie76

st = int(40)
ed = int(46)

def button1():
    open_file_dialog()
    display_image(file_path, 300, 300)
    
def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("*.jpg","*.jpeg")])

def display_image(image_path, width, height):
    global best_image
    image = Image.open(image_path)
    image = image.resize((width, height))
    photo = ImageTk.PhotoImage(image=image)
    img_label.config(image=photo)
    img_label.image = photo

def calculate_color_quality(img):
    # Convert the image to Lab color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    
    # Compute the mean and standard deviation of the 'a' and 'b' channels
    (l, a, b) = cv2.split(lab)
    l_mean = np.mean(l)
    a_mean = np.mean(a)
    b_mean = np.mean(b)
    l_stddev = np.std(l)
    a_stddev = np.std(a)
    b_stddev = np.std(b)
    
    # Compute the colorfulness using the formula
    # Colorfulness = sqrt( (a_stddev^2) + (b_stddev^2) )
    colorfulness = np.sqrt((a_stddev ** 2) + (b_stddev ** 2))
    
    return colorfulness

def find_best_image_with_color_quality(folder_path):
    best_image_path = None
    best_color_quality = 0.0
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join(folder_path, filename)
            img = cv2.imread(image_path)
            color_quality = calculate_color_quality(img)
            
            if color_quality > best_color_quality:
                best_color_quality = color_quality
                best_image_path = image_path
    
    return best_image_path

def display_best_image_with_color_quality():
    folder_path = (r"project\img_folder")
    best_image_path = find_best_image_with_color_quality(folder_path)
    print(best_image_path)
    
    if best_image_path:        
        # Load the best image and display it in a label
        best_image = Image.open(best_image_path)
        best_image = best_image.resize((300, 300))
        photo = ImageTk.PhotoImage(best_image)
        label.config(image=photo)
        label.image = photo
    else:
        print("No valid images found in the folder.")

def color_more():
    global st, ed
    st = st + 5
    ed = ed + 5
    if st == 70:
        print("Colorized to max level")
        exit()
    else:
        dser(st,ed)

def dser(start, end):
    global resized, net, bw_image
    L = cv2.split(resized)[0]
    for i in range(start, end):
        L -= i
        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1,2,0))

        ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
        L = cv2.split(lab)[0]

        colorized = np.concatenate((L[:,:,np.newaxis], ab), axis=2)
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = (255.0 * colorized).astype("uint8")
        cv2.imwrite(r"img_folder\%d.jpg" % i, colorized)
        print(i ," Completed")
    display_best_image_with_color_quality()

def main():
    global st,ed,resized,net,bw_image,lab
    
    prototxt_path = (r"colorization_deploy_v2.prototxt")
    model_path = (r"colorization_release_v2.caffemodel" )
    kernel_path = (r"pts_in_hull.npy")

    image_path =(file_path)

    net  = cv2.dnn.readNetFromCaffe(prototxt_path,model_path)
    points = np.load(kernel_path)

    points = points.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    bw_image = cv2.imread(image_path)
    normalized = bw_image.astype("float32")/ 255.0

    lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)

    #224X224

    resized = cv2.resize(lab, (224, 224))

    dser(st,ed)
    
root = tk.Tk()
root.title("Image Colorizer")
root.iconbitmap(r"C:\my documents\my works\python stuff\stack.ico")
root.configure(bg="#0C1A1A")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Set the size and position of the window to fit the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Main Title-----------------
title_label = tk.Label(root, text="Image Colorizer", fg="#6ACFC7", bg="#0C1A1A", font=("Algerian", 50, "underline"))
title_label.place(x=40, y=60)

# Description
description_label = tk.Label(root, text="Convert your black & white images here",fg="#6ACFC7", bg="#0C1A1A", font=("times", 30, "underline"))
description_label.place(x=140, y=200)

# Image Conversion Section
image_label = tk.Label(root, text="Select the image you want to colorize", fg="#6ACFC7", bg ="#0C1A1A", font=("times", 18))
image_label.place(x=200, y=300)

sel_button = tk.Button(root, text="Select", bg="#6ACFC7", fg="#0C1A1A", command = button1, width = 10, height = 2,font=("times", 14))
sel_button.place(x=330, y=380)

load_button = tk.Button(root, text="Colorize", bg="#6ACFC7", fg="#0C1A1A",command = main, width = 10, height = 2,font=("times", 14))
load_button.place(x=1120, y=380)

load_button2 = tk.Button(root, text="Colorize More", bg="#6ACFC7", fg="#0C1A1A",command = color_more, width = 12, height = 5,font=("times", 14))
load_button2.place(x=1340, y=340)

img_label = tk.Label(root, bg = "#0C1A1A")
img_label.place(x=230, y=470)

label = Label(root, bg = "#0C1A1A")
label.place(x = 1020, y= 470)

root.mainloop()
