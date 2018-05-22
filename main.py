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
import colour_map as cm
import face_transplant as ft

def get_hsv_from_pixel(pixel):
	pixel = pixel/255;
	h,s,v = colorsys.rgb_to_hsv(pixel[0],pixel[1],pixel[2])
	return h,s,v;

#---------------------COLOR TRANSFER:---------------------------------------------
'''pk1 = 'poke/pikachu.png'
pk2 = 'poke/blastoise.png'
pk3 = 'poke/blastoise.png'
cs.change_colour(pk1,pk2,pk3,10)

face1 = 'poke/pikachu_face.png'
cs.change_colour(pk2,face1,face1,10)'''

#-------------------Input------------------------------------------------------------
pokemon_body = input('Insira o nome do pokemon que será usado como corpo:\n')
pokemon_face = input('Insira o nome do pokemon que será usado como rosto:\n')

body_string = 'poke/' + pokemon_body + '_body.png'
plastic_face_string = 'poke/' + pokemon_body + '_face.png'
face_string = 'poke/' + pokemon_face + '_face.png'

src_string  = 'poke/' + pokemon_body + '.png'
original_string =  'poke/' + pokemon_face + '.png'




#-------------------Loading----------------------------------------------------------
#body = 'poke/blastoise_body.png' #insert the body with no face where the face will be transplated
B = io.imread(body_string)
plastic_face = io.imread(plastic_face_string); #insert the face of the body chosen
overlay =  io.imread(face_string) #insert the face that will be transplanted
src     =  io.imread(src_string) #insert the whole picture of the body that will be transplanted

#-------------------Change face colours----------------------------------------------
overlay_string = cs.change_colour(plastic_face_string,face_string,face_string,10)
overlay = io.imread(overlay_string)

#-------------------Transplanting the new coloured face into the body-------------------------------------------------
H,W,D= plastic_face.shape
cX,cY = ft.get_face_center(body_string)
#-------------------------------------------------------------------------------------
overlay = cv2.resize(overlay, (W,H))
#-------------------------------------------------------------------------------------
h = int(H/2)
w = int(W/2)
plt.show()
for y in range (W):
	for x in range (H):
		Hue,Sat,V = get_hsv_from_pixel(overlay[x][y])
		if(  (Sat> 0.5)  or (V < 0.90) ):
			#print(overlay[x][y])
			src[cY-h+x+1][cX-w+y] = overlay[x][y]
io.imsave(pokemon_body + pokemon_face + '.png',src)
plt.imshow(src)
plt.show()
#------------------Final colour change----------------------------------------------

cs.change_colour(original_string,src_string,pokemon_body + pokemon_face + '.png',10)
print ('Done')