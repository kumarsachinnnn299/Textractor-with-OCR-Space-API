from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import boto3
import cv2
from http import client
import requests
import io
import json
import numpy as np

my_font1 = ('calibri', 20, 'bold')
my_font2 = ('calibri', 10)
root = Tk()
root.geometry('1920x1080')
root.title('AWS-Textract')
root.iconbitmap('aws_icon_137928.ico')
l1 = Label(root, text="Upload the Photo", width=30, font=my_font1).pack(pady=5)
b1 = Button(root, text='Upload Image', width=10, command=lambda: open()).pack(pady=10)

#Loading the file
def open():
    global GUIimg
    root.filename = filedialog.askopenfilename(initialdir="D:\Study\College\Year 3\Sem 5\Mini Project", title='Choose Image', filetypes=(
        ("All Files", "*.*"), ("PNG Files", "*.png"), ("Jpg files", "*.jpg")))
    GUIimg = ImageTk.PhotoImage(Image.open(root.filename).resize((400, 200)))
    my_img_label = Label(image=GUIimg).pack()
    print(type(root.filename))
    print(root.filename)
    b2 = Button(root, text='Get Text',
                command=lambda: ocr(root.filename)).pack(pady=10)


# Ocr
def ocr(location):
    docimg = cv2.imread(location)
    height, width, _ = docimg.shape
    roi = docimg

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
    file_bytes = io.BytesIO(compressedimage)

    result = requests.post(url_api,
                           files={"docimg.jpg": file_bytes},
                           data={"apikey": "helloworld",
                                 "language": "eng"})
    result = result.content.decode()
    result = json.loads(result)

    parsed_results = result.get("ParsedResults")[0]
    text_detected = parsed_results.get("ParsedText")
    l2 = Label(root, text="Output", width=30, font=my_font1).pack()
    l2 = Label(root, text=text_detected, width=30, font=my_font2).pack()


root.mainloop()
