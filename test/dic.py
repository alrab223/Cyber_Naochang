import os
from PIL import Image

imagefilename = "rainbow.jpg"

curdir = os.path.dirname(os.path.abspath(__file__))

def get_image_size(src):
    w = src.width
    h = src.height
    return w,h

def main():
    try:
        im = Image.open(imagefilename)
        w, h = get_image_size(im)
        print('width: ',w)
        print('height:',h)
        
        im1,im2,im3,im4=split_quarter_image(im)
        im1.save('1.jpg')
        im2.save('2.jpg')
        im3.save('3.jpg')
        im4.save('4.jpg')
        
    except Exception as x:
        print(x)
        

def split_quarter_image(src):
    w,h = get_image_size(src)
    
    i1 = src.crop((0 ,0 , w/2 , h/2))
    i2 = src.crop((w/2 ,0 , w , h/2))
    i3 = src.crop((0 ,h/2 , w/2 , h))
    i4 = src.crop((w/2 ,h/2 , w , h))

    return i1,i2,i3,i4
        
if __name__ == "__main__":
    main()