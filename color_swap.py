from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from skimage import io, util, filters
import colorsys
import colour_map
from collections import defaultdict

def colours_by_freq(img):
	image = img.convert('HSV')
	by_color = defaultdict(int)
	for pixel in image.getdata():
		if( (pixel[2] < 255) and (pixel[2] > 0) and (pixel[1] > 0) and (pixel[1] < 255)):
			by_color[pixel] += 1
	y = list(reversed(sorted(by_color,key=by_color.get)))
	return y,by_color;
def sort_by_tone_frequency(keylist,dic,bycolor):
	new_key_list = []
	new_dic = {}
	for key in keylist:
		if(not key in new_dic):
			new_dic[key] = 0;
		for color in dic[key]:
			new_dic[key] += bycolor[color];
	return list(reversed(sorted(new_dic,key=new_dic.get)))
def HSV_list_to_rgb(list):
	new_list = []
	for i in list:
		i = colorsys.hsv_to_rgb(i[0]/255,i[1]/255,i[2]/255)
		new_list.append(i);
	return new_list;
def colour_encode(tuple):
	a,b,c = tuple[0:3];
	return 3*a+4*5*c;

def color_decoding(image,key_list1,key_list2,dic2,limit):
	map = map_list_to_list(key_list1,key_list2)
	w,h = image.size
	img = image.load()
	for i in range(h):
		for j in range(w):
			pixel = img[j,i];
			H = pixel[0]
			key = check_surround(key_list1,H,limit);
			if( (key >= 0) and (key in map)):
				mapped_H = map[key]
				S = img[j,i][1];
				V = img[j,i][2];
				new_color = closest_colour_by_s(dic2[mapped_H],S);
				if(S > 0):
					img[j,i] = (new_color[0],new_color[1],int((1*new_color[2]+3*img[j,i][2])/4));
				else:
					img[j,i] = (new_color[0],S,int((1*new_color[2]+3*img[j,i][2])/4));
	return image.convert('RGBA')

def closest_colour_by_s(color_list,s):
	max_diff = 500;
	diff = 500;
	picked_color = (0,0,0)
	for color in color_list:
		diff = abs(color[1] - s);
		if(diff < max_diff):
			max_diff = diff;
			picked_color = color;
	return picked_color



def colour_map(color_list,color_list_2):
	dic = {}
	j = 0;
	k = len(color_list_2)
	for i in color_list:
			dic[colour_encode(i)] = color_list_2[j];
			j = j + 1;
			if(j == k):
				break;
	return dic
def map_list_to_list(cl1,cl2):
  dic = {}
  l = len(cl2)
  j = 0;
  for i in cl1:
  	if(j < l):
  		dic[i] = cl2[j]
  		j +=1
  	else:
  		break;

  return dic;
def check_surround(color_list,H,limit):
	for i in color_list:
		if( (H > (i-limit) ) and (H < (i + limit) ) ):
			return i;
	return -1;

def classify_color(color_list,limit):
  dic = {}
  key_list = []
  for i in color_list:
    H = i[0];
    key = check_surround(key_list,H,limit) 
    if( key < 0 ):
      key_list.append(H);
      group = [];
      group.append(i)
      dic[H] = group;
    else:
      dic[key].append(i)
  return key_list,dic;





def change_colour(pokemon1,pokemon2,poke_fusion,limit):
	Transplant_Face = Image.open(pokemon1) #face that will be transplanted
	Face_Body = Image.open(pokemon2) #original face of the body where the face above will be transplanted
	Transplant_Image = Image.open(poke_fusion)
	Transplant_Image = Transplant_Image.convert('HSV')
	Face_Body = Face_Body.convert('HSV')
	Transplant_Face = Transplant_Face.convert('HSV')
	x = Transplant_Face.load()
	y = Face_Body.load()
	w,h = Transplant_Face.size
	pixels = Transplant_Face.getcolors(w*h)
	f1,bycolor1 = colours_by_freq(Face_Body)
	f2,bycolor2 = colours_by_freq(Transplant_Face)
	keylist1,dic1 = classify_color(f1,limit)
	keylist2,dic2 = classify_color(f2,limit)
	keylist1 = sort_by_tone_frequency(keylist1,dic1,bycolor1)
	keylist2 = sort_by_tone_frequency(keylist2,dic2,bycolor2)
	c = color_decoding(Transplant_Image,keylist1,keylist2,dic2,limit)
	plt.imshow(c)
	plt.show()
	new_fusion = pokemon1[5:8] + pokemon2[5:7] + '.png';
	io.imsave(new_fusion,c)
	return new_fusion


#print(k)