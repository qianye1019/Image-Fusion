import skimage
from skimage import io, util, filters
from PIL import Image

import cv2
from skimage.measure import label
from skimage import morphology as mo
from skimage.color import label2rgb

from matplotlib import pyplot as plt
import numpy as np
import colorsys
import skimage
from skimage import io, util, filters
from skimage.measure import label
from skimage import morphology as mo
from skimage.color import label2rgb
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import numpy as np
import color_swap as cs

def save_image(name,extension,image):
	new_image = name[:-3] + '_' + extension + '.png';
	io.imsave(new_image,image)
def alpha_to_white(img,w,h):
	for i in range(h):
		for j in range(w):
			if(img[i][j][3] == 0):
				img[i][j] = [255,255,255,255];
			else:
				img[i][j] = [0,0,0,255];
def get_face_center(image):
	faceless_body = io.imread(image)
	h,w,d = faceless_body.shape
	alpha_to_white(faceless_body,w,h)
	new_image = image[:-4] + '_bw.png'
	io.imsave(new_image,faceless_body)
	im = cv2.imread(new_image)
	imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im_gauss = cv2.GaussianBlur(imgray, (5, 5), 0)
	ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
	im2,contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(im, contours, -1, (1,56,187), 1)
	plt.imshow(im)
	plt.show()
	contours_area = sorted(contours, key=cv2.contourArea)
	c = contours_area[0]
	M = cv2.moments(c)
	if(M["m00"] > 0):
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		print(cX,cY)
	return cX,cY

'''
#-------------------Input------------------------------------------------------------
pokemon_body = input('Insira o nome do pokemon que será usado como corpo:\n')
pokemon_face = input('Insira o nome do pokemon que será usado como rosto:\n')
body_string = 'poke/' + pokemon_body + '_body.png'
plastic_face_string = 'poke/' + pokemon_body + '_face.png'
face_string = 'poke/' + pokemon_face + '_face.png'
src_string  = 'poke/' + pokemon_body + '.png'
overlay_string =  'poke/' + pokemon_face + '.png'
#-------------------Loading----------------------------------------------------------
#body = 'poke/blastoise_body.png' #insert the body with no face where the face will be transplated
B = io.imread(body_string)
plastic_face = io.imread(plastic_face_string); #insert the face of the body chosen
overlay =  io.imread(face_string) #insert the face that will be transplanted
src     =  io.imread(src_string) #insert the whole picture of the body that will be transplanted
#-------------------Change body colours----------------------------------------------

h,w,d= src.shape
#-------------------Finding the face-------------------------------------------------
cX,cY = get_face_center(body_string)
#-------------------------------------------------------------------------------------
W = plastic_face.shape[0]
H = plastic_face.shape[1]
overlay = cv2.resize(overlay, (W,H))
#-------------------------------------------------------------------------------------
h = int(H/2)
w = int(W/2)
plt.show()
for y in range (W):
	for x in range (H):
		if(overlay[x][y][3] > 0   ):
			pass
			src[cY+1-h+x][cX-w+y] = overlay[x][y]
io.imsave(pokemon_body + pokemon_face + '.png',src)
plt.imshow(src)
plt.show()
cs.change_colour(overlay_string,src_string,pokemon_body + pokemon_face + '.png')
print ('Done')'''