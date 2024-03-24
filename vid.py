import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk 
import os
import numpy as np
import cv2
import re

def play_video1():
    file_path1 = (r"output.mp4")
    cap = cv2.VideoCapture(file_path1)
    
    def update_frame():
        nonlocal cap
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            img_label2.config(image=photo)
            img_label2.image = photo
            img_label2.after(10, update_frame)
        else:
            print("Video playback finished")
            cap.release()

    update_frame()
    
def play_video():
    global file_path
    cap = cv2.VideoCapture(file_path)
    
    def update_frame():
        nonlocal cap
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            img_label.config(image=photo)
            img_label.image = photo
            img_label.after(10, update_frame)
        else:
            print("Video playback finished")
            cap.release()

    update_frame()

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def merge():
    frames_directory = (r"colorimages")

    # Get a list of all image files in the directory
    frame_files = sorted([f for f in os.listdir(frames_directory) if f.endswith('.jpg')], key = natural_sort_key)
    frame = cv2.imread(os.path.join(frames_directory, frame_files[0]))
    height, width, layers = frame.shape

    # Define the codec and create a VideoWriter object
    output_video_path = (r"output.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs as well
    out = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))  # Change 30 to desired FPS

    # Loop through each frame and add it to the video
    for frame_file in frame_files:
        frame_path = os.path.join(frames_directory, frame_file)
        frame = cv2.imread(frame_path)
        out.write(frame)

    # Release the VideoWriter
    out.release()

    print("Video creation completed.")
    
def convert():
    prototxt_path = os.path.join(r"colorization_deploy_v2.prototxt")
    model_path = os.path.join(r"colorization_release_v2.caffemodel")
    kernel_path = os.path.join(r"pts_in_hull.npy")

    net  = cv2.dnn.readNetFromCaffe(prototxt_path,model_path)
    points = np.load(kernel_path)

    points = points.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    folder_path = os.path.join(r"bwimges")
    image_extensions = ['.jpg']

    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.jpg'))], key = natural_sort_key)
    count = 0  # Initialize count here
    for image_file in image_files:
        print(count)
        bw_image = cv2.imread(os.path.join(folder_path, image_file))
        normalized = bw_image.astype('float32') / 255.0

        lab = cv2.cvtColor(normalized, cv2.COLOR_BGR2LAB)
        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1,2,0))
        ab = cv2.resize(ab, (bw_image.shape[1], bw_image.shape[0]))
        L = cv2.split(lab)[0]

        colorized = np.concatenate((L[:,:,np.newaxis], ab), axis=2)
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = (255.0 * colorized).astype("uint8")

        cv2.imwrite(r"colorimages\%d.jpg" % count, colorized)
        count = count + 1
    label_signify1 = tk.Label(root, text="coloured Frames collected...!", fg="#6ACFC7", bg="#0C1A1A", font=("Algerian", 36, "underline"))
    print("Completed successfully")

def start_function():
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Error opening video")
    print("started1")
    count = 0
    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            cv2.imwrite(r"bwimges\%d.jpg" % count, image)
            count += 1
        else:
            break

    cap.release()# Release the VideoCapture object
    print("Completed successfully")

def button1():
    open_file_dialog()
    play_video()

def button2():
    start_function()
    convert()
    merge()
    play_video1()
    
def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
        

    
root = tk.Tk()
root.title("CONVERT-WHITE")
root.iconbitmap(r"C:\my documents\my works\python stuff\stack.ico")
root.configure(bg="#0C1A1A")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Set the size and position of the window to fit the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Main Title-----------------
title_label = tk.Label(root, text="Video Colorizer", fg="#6ACFC7", bg="#0C1A1A", font=("Algerian", 50, "underline"))
title_label.place(x=40, y=60)

# Description
description_label = tk.Label(root, text="Convert your black & white Videos here",fg="#6ACFC7", bg="#0C1A1A", font=("times", 30, "underline"))
description_label.place(x=140, y=200)

# Image Conversion Section
image_label = tk.Label(root, text="Select the video you want to colorize", fg="#6ACFC7", bg="#0C1A1A", font=("times", 18))
image_label.place(x=200, y=300)

sel_button = tk.Button(root, text="Select", bg="#6ACFC7", fg="#0C1A1A", command = button1, width = 10, height = 2, font = ("times",14))
sel_button.place(x=330, y=380)

#label = tk.Label(root)
#label.place()
# Video Conversion Section
#video_label = tk.Label(root, text="If you want to convert videos", fg="#6ACFC7", bg="#0C1A1A", font=("times", 14))
#video_label.place(x=960, y=340)

load_button = tk.Button(root, text="Colorize", bg="#6ACFC7", fg="#0C1A1A", command = button2, width = 10, height = 2, font = ("times",14))
load_button.place(x=1120, y=380)

global img_label
global img_label2
img_label = tk.Label(root, height = 300, bg="#0C1A1A")
img_label.place(x=230, y=470)

img_label2 = tk.Label(root, height = 300, bg = "#0C1A1A")
img_label2.place(x=1020, y=470)

root.mainloop()
