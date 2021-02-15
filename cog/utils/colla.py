from PIL import Image
import cv2


def mirikora2():
   im1 = Image.open('picture/colla/image.png')
   im2 = Image.open('picture/colla/コラ.png')
   img_resize = im2.resize(im1.size)
   print(im2.size)
   im1.paste(img_resize, (0, 0), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def ppp():
   im1 = Image.open('picture/colla/image.png')
   im2 = Image.open('picture/colla/PPP.png')
   img_resize = im2.resize(im1.size)
   print(im2.size)
   im1.paste(img_resize, (0, 0), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def deresute_kora():
   im1 = Image.open('picture/colla/image.png')
   im2 = Image.open('picture/colla/デレステコラ.png')
   img_resize = im2.resize(im1.size)
   print(im2.size)
   im1.paste(img_resize, (0, 0), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def nhk():
   im1 = Image.open('picture/colla/image.png')
   im2 = Image.open('picture/colla//nhk.png')
   img_resize = im2.resize((int(im1.size[0] / 3.7), int(im1.size[1] / 3)))
   print(im1.size)
   print(img_resize.size)
   im1.paste(img_resize, (int(img_resize.size[0] * 2.8), int(img_resize.size[1] * 2)), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def bazirisuku():
   im1 = Image.open('picture/colla/image.png').convert("RGBA")
   im2 = Image.open('picture/colla//baji.png').convert("RGBA")
   img_resize = im2.resize((int(im1.size[0] / 1.5), int(im1.size[1] / 1.4)))
   print(im1.size)
   print(img_resize.size)
   im1.paste(img_resize, (int(img_resize.size[0] / 3.4), int(img_resize.size[1] / 3)), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def out():
   im1 = Image.open('picture/colla/image.png')
   im2 = Image.open('picture/colla/all_out.png')
   img_resize = im2.resize((int(im1.size[0] / 2), int(im1.size[1] / 2)))
   print(im1.size)
   print(img_resize.size)
   im1.paste(img_resize, (int(img_resize.size[0] / 2), int(img_resize.size[1])), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def gaming():
   img1 = cv2.imread('picture/colla/image.png')
   img2 = cv2.imread('picture/colla/rainbow.jpg')
   img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
   img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

   img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

   blended = cv2.addWeighted(src1=img1, alpha=0.6, src2=img2, beta=0.4, gamma=0)

   cv2.imwrite('picture/colla/new.png', cv2.cvtColor(blended, cv2.COLOR_RGB2BGR))


def elon():
   im1 = Image.open('picture/colla/image.png')
   im2 = Image.open('picture/colla/elon.png')
   img_resize = im2.resize(im1.size)
   print(im2.size)
   im1.paste(img_resize, (0, 0), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def onesin():
   im1 = Image.open('picture/colla/image.png').convert("RGBA")
   im2 = Image.open('picture/colla/onesin.png').convert("RGBA")
   img_resize = im2.resize(im1.size)
   print(im2.size)
   im1.paste(img_resize, (0, 0), img_resize)
   im1.save('picture/colla/new.png', quality=95)


def colla_maker(num):
   if num == 1:
      mirikora2()
   elif num == 2:
      bazirisuku()
   elif num == 3:
      deresute_kora()
   elif num == 4:
      ppp()
   elif num == 5:
      out()
   elif num == 6:
      nhk()
   elif num == 7:
      gaming()
   elif num == 8:
      elon()
   else:
      onesin()
