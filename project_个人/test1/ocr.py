from selenium import webdriver
import time
import pytesseract

from PIL import Image
from PIL import ImageOps

imageName = "x.png"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def cleanImage(imagePath):
    image = Image.open(imagePath)  #打开图片
    box = (1430, 485, 1522, 512)
    imageCode = image.crop(box)
    imageCode.save('code.png')
    image = imageCode
    image = image.point(lambda x: 0 if x < 143 else 255)  # 处理图片上的每个像素点，使图片上每个点“非黑即白”
    borderImage = ImageOps.expand(image, border=20, fill='white')
    borderImage.save(imagePath)

    text1 =pytesseract.image_to_string(Image.open("code.png")).strip()

    text2 = pytesseract.image_to_string(Image.open("captcha.png")).strip()

    print("原图:"+ text1)
    print("白底图:" + text2)

def open():
    driver = webdriver.Chrome('C:/Users/admin/Downloads/chromedriver_win32/chromedriver.exe')
    driver.get('https://www.jiguang.cn/accounts/login/form') #登录页面
    time.sleep(1)
    driver.maximize_window()
    driver.save_screenshot(imageName)  # 截屏，并保存图片
    time.sleep(1)
    return imageName

if __name__ == '__main__':
    img =open()
    cleanImage(img)