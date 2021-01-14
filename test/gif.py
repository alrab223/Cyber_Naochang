from PIL import Image
import glob
files = sorted(glob.glob('../picture/fortune/*.gif'))  
images = list(map(lambda file : Image.open(file) , files))
images[0].save('image.gif' , save_all = True , append_images = images[1:] , duration = 20 , loop = 0)