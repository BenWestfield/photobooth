from PIL import Image
from time import sleep
from picamera import PiCamera
import cups

dir = "/home/pi/Photos/"

camera = PiCamera()
camera.resolution = (1024,768)
camera.rotation = 180
conn = cups.Connection()
printer = conn.getPrinters()
name = list(printer.keys()) [0]
print("printing to " + name)

def take_photo(file):
    print("taking picture")
    sleep(2)
    camera.capture(dir + file+".jpeg")

def resize(photo):
    photo.resize((502,370))

sleep(1)
take_photo("img1")
img1 = Image.open(dir + "img1.jpeg")
take_photo("img2")
img2 = Image.open(dir + "img2.jpeg")
take_photo("img3")
img3 = Image.open(dir + "img3.jpeg")
take_photo("img4")
big_img = Image.open(dir + "img4.jpeg")

img_bg = Image.open("/home/pi/Downloads/horses.jpeg")
img_bg.paste(img1.resize((502,370)), (30,800))
img_bg.paste(img2.resize((502,370)), (30 + (502 *1) + (15 * 1),800))
img_bg.paste(img3.resize((502,370)), (30 + (502 *2) + (15 * 2),800))
img_bg.paste(big_img.resize((966,725)), ((1600 - 996), 40))
img_bg.save(dir + "photobooth.jpeg")

conn.printFile(name,dir + "photobooth.jpeg","Photobooth",{})

