from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Label, Entry, StringVar, Button, Toplevel
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt

from model import get_model
from utills import rearrange, load_data, extract_piece, swap_piece

model_pkl_file = "celeb_classifier_model.pkl"
base_path = 'data/celeb_2x2/'

x_test, y_test = load_data(base_path, 'test')


def resize_and_join(top_left_path, top_right_path, bottom_left_path, bottom_right_path, output_path):
    top_left = Image.open(top_left_path).resize((100, 100))
    top_right = Image.open(top_right_path).resize((100, 100))
    bottom_left = Image.open(bottom_left_path).resize((100, 100))
    bottom_right = Image.open(bottom_right_path).resize((100, 100))

    new_image = Image.new("RGB", (200, 200))
    new_image.paste(top_left, (0, 0))
    new_image.paste(top_right, (100, 0))
    new_image.paste(bottom_left, (0, 100))
    new_image.paste(bottom_right, (100, 100))

    new_image.save(output_path)


def open_file(entry_var):
    file_path = filedialog.askopenfilename()
    entry_var.set(file_path)


def process_images(top_left_path, top_right_path, bottom_left_path, bottom_right_path, output_path, entry_var1, entry_var2, entry_var3, entry_var4):
    resize_and_join(top_left_path, top_right_path,
                    bottom_left_path, bottom_right_path, output_path)
    entry_var1.set(top_left_path)
    entry_var2.set(top_right_path)
    entry_var3.set(bottom_left_path)
    entry_var4.set(bottom_right_path)

    with open(model_pkl_file, 'rb') as file:
        model = pickle.load(file)

    im = os.listdir("data/celeb_2x2/test")
    im.sort()
    im = im[0]

    im = Image.open(f"data/celeb_2x2/test/{im}")
    im = np.array(im).astype('float16')
    im = im / 255 - 0.5
    out = np.argmax(model.predict(np.expand_dims(
        extract_piece(im), axis=0))[0], axis=1)
    new_im = rearrange(np.array(im)+.5, out)

    # Display the image using matplotlib
    plt.imshow(new_im.astype('float64'))
    plt.show()


def display_result(output_path):
    result_window = tk.Toplevel(root)
    result_window.title("Result")

    output_image = Image.open(output_path)
    photo = ImageTk.PhotoImage(output_image)

    label = tk.Label(result_window, image=photo)
    label.photo = photo
    label.pack()


root = tk.Tk()
root.title("Snap Stitcher")
root.configure(bg="#0099cc")

entry_var1 = StringVar()
entry1 = Entry(root, textvariable=entry_var1, state='disabled', width=50)
entry1.grid(row=0, column=0, padx=10, pady=10)

entry_var2 = StringVar()
entry2 = Entry(root, textvariable=entry_var2, state='disabled', width=50)
entry2.grid(row=1, column=0, padx=10, pady=10)

entry_var3 = StringVar()
entry3 = Entry(root, textvariable=entry_var3, state='disabled', width=50)
entry3.grid(row=2, column=0, padx=10, pady=10)

entry_var4 = StringVar()
entry4 = Entry(root, textvariable=entry_var4, state='disabled', width=50)
entry4.grid(row=3, column=0, padx=10, pady=10)

button1 = Button(root, text="Upload 1st image piece",
                 command=lambda: open_file(entry_var1))
button1.grid(row=0, column=1, padx=10, pady=10)

button2 = Button(root, text="Upload 2nd image piece",
                 command=lambda: open_file(entry_var2))
button2.grid(row=1, column=1, padx=10, pady=10)

button3 = Button(root, text="Upload 3rd image piece",
                 command=lambda: open_file(entry_var3))
button3.grid(row=2, column=1, padx=10, pady=10)

button4 = Button(root, text="Upload 4th image piece",
                 command=lambda: open_file(entry_var4))
button4.grid(row=3, column=1, padx=10, pady=10)

process_button = Button(root, text="Stitch the image", command=lambda: process_images(
    entry_var1.get(), entry_var2.get(), entry_var3.get(), entry_var4.get(), 'data/celeb_2x2/test/0.jpg', entry_var1, entry_var2, entry_var3, entry_var4))
process_button.grid(row=4, column=0, columnspan=2, pady=10)


def help():
    newWindow = Toplevel(root)
    newWindow.title("Help")
    newWindow.geometry("400x200")
    msg = ("To reassemble your fragmented photo, please upload the pieces in the respective drop boxes one by one."'\n'"Only image files are accepted. Other input formats will be rejected"'\n'
           "If you have less than 4 pieces, please upload a blank image full of white or black"'\n'"After uploading click on stitch to get your final image all stitched up!")
    Label(newWindow, text=msg, wraplength=400).pack()


Button(root, text="Help!", command=help).grid(row=5, column=6, pady=10)

root.mainloop()
