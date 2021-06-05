# text recognition
import cv2
import pytesseract
import numpy as np
from pytesseract import Output
import os.path
import googletrans 
from googletrans import Translator


def get_directory():
    found_path = False
    while found_path == False:
        mod_path = input("Enter the name of the image you want to read: ")
        if not os.path.isfile("./images/" + mod_path):
            print("The specified file path could not be found, please double check your input (remember to include the file type).")
        else: 
            found_path = True
    return "./images/" + mod_path

#opening
def opening(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


#translates the hiragana/katakana characters for output
def convert_text(text):
    hiragana = {}
    f = open("hiragana.txt", "r", encoding="UTF-8")
    for line in f:
        (key, val) = line.split()
        hiragana[key] = val
    f.close()

    katakana = {}
    f = open("katakana.txt", "r", encoding="UTF-8")
    for line in f:
        (key, val) = line.split()
        katakana[key] = val
    f.close()

    output = []
    for item in text:
        if item in hiragana:
            item = hiragana[item]
        elif item in katakana:
            item = katakana[item]
        output.append(item)

    return output

#writes to the output file
def write_to_output(text):
    f = open("output.txt","a+")
    for item in text:
        f.write(item + "")
    f.write("\n\n")
    return 

e1 = cv2.getTickCount() # start time
# read image
img_name = get_directory()
img = cv2.imread(img_name)
img_output = cv2.imread(img_name)

lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# Split LAB image to different channels
l, a, b = cv2.split(lab)

#Applying CLAHE to L-channel
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
cl = clahe.apply(l)

#Merge the CLAHE enhanced L-channel with the a and b channel
limg = cv2.merge((cl,a,b))

# Transforming the image from LAB to RBG
final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)


#thresholding
th, lab = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)

open_img = opening(lab)
cv2.imshow('Processed', open_img)


# Place bounding boxes around all identified text
d = pytesseract.image_to_data(lab, output_type=Output.DICT, lang="jpn")
n_boxes = len(d['text'])
text = pytesseract.image_to_string(lab, lang="jpn")
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        new_chars = []
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img_output = cv2.rectangle(img_output, (x, y), (x + w, y + h), (0, 0, 0), -1)

for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        new_chars = []
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        for char in d['text'][i]:
            new_chars += convert_text(char)
        new_chars = "".join(new_chars)
        new_chars.strip()
        #print(new_chars)
        font_size = 0.04 * h
        img_output = cv2.putText(img_output, new_chars, (x, h + y), cv2.FONT_HERSHEY_PLAIN, font_size, (0, 0, 255), 3)
# pytesseract
cv2.imshow('Before', img)
cv2.imshow('Final', img_output)
cv2.imwrite('./images/output.jpg', img_output)


cv2.imwrite('./images/capture.jpg', lab)
text = pytesseract.image_to_string(lab, lang="jpn")
text = text.split()
if os.path.exists("output.txt"):
    os.remove("output.txt")

write_to_output(" ".join(text))
print(" ".join(text) + "\n")

symbol_text = convert_text(text)
symbol_text = " ".join(symbol_text)
write_to_output(symbol_text)
print(symbol_text + "\n")


translator = Translator(service_urls=['translate.googleapis.com'])
eng_text = translator.translate("".join(text)).text
print(eng_text)
write_to_output(eng_text)

e2 = cv2.getTickCount()
time_taken = (e2 - e1)/cv2.getTickFrequency()
print("Time Taken: ", time_taken)

roi = ()

cv2.waitKey(0)