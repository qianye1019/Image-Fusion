from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from skimage import io, util, filters
import colorsys
from collections import defaultdict
from collections import defaultdict

def colours_by_freq(img):
  image = img.convert('HSV')
  by_color = defaultdict(int)
  for pixel in image.getdata():
    if(pixel[2] < 255 and pixel[2] > 25):
      by_color[pixel] += 1
  y = list(reversed(sorted(by_color,key=by_color.get)))
  return y;
def check_surround(key_list,H,limit):
  for i in key_list:
    if( (H > i-limit) and (H < i + limit) ):
      return i;
  return -1;
def map_list_to_list(cl1,cl2):
  dic = {}
  l = len(cl2)
  j = 0;
  for i in cl1:
    dic[i] = cl2[j]
    j +=1
    if(j == l):
      break;
  return dic;

'''
Transplant_Face = Image.open('char2.png') #face that will be transplanted
Transplant_Face = Transplant_Face.convert('HSV')
image2 = Image.open('plume.png').convert('HSV')
x = Transplant_Face.load()
y = image2.load()
w,h = Transplant_Face.size
f1 = colours_by_freq(Transplant_Face)
f2 = colours_by_freq(image2)
a,g = classify_color(f1,15)
c,h = classify_color(f2,15)
print(a)
print(c)
d = color_maps(a,c)
e = color_maps(c,a)
print(g)
print(h)'''