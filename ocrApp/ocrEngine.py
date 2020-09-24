import cv2
import pytesseract
import numpy as np


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread("static/uploads/example_01.png")


def wordBox(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB )
    boxes = pytesseract.image_to_data(image, lang="eng+swe")


    for x, b in enumerate(boxes.splitlines()):
        # print(b)
        if x != 0:
            b = b.split()
            # print(b)
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(rgb, (x, y), (w + x, h + y), (0, 0, 255, 3))
                cv2.putText(rgb, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 255), 1)
    return rgb

def detectChars(image):
    result = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB )
    hImg, wImg,_ = result.shape
    boxes = pytesseract.image_to_boxes(image, lang="eng+swe")


    for b in boxes.splitlines():
            #print(b)
            b = b.split(' ')
            #print(b)
            x,y,w,h =int(b[1]),int(b[2]),int(b[3]),int(b[4])
            cv2.rectangle(result,(x,hImg-y),(w,hImg-h),(0,0,255,3))
            cv2.putText(result, b[0],(x,hImg-y+25), cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),1)
    return result



def resizeW(w, image):
    # resizes image to specific pixel width while keeping proportions
    wSize = w
    height, width, channels = img.shape
    wSizeMultiplier = wSize / width
    image = cv2.resize(img, (wSize, int(height * wSizeMultiplier)))
    return image

# def string_to_pdf(string):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt=string, ln=1, align="C")
#     pdf.output("simple_demo.pdf")


img = resizeW(1500, img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 15)

text = pytesseract.image_to_string(adaptive_threshold, lang='eng+swe')

print(text)

cv2.imshow('Result', gray)
cv2.imshow('box', wordBox(gray))
cv2.imshow('chars', detectChars(gray))
cv2.waitKey(0)
with open('static/textFiles/file.text', mode ='w') as f:
    f.write(text)