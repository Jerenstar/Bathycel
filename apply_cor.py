from segmentation import *
import numpy as np
from Genetique	import *
from Fonction_cout import *
import os
from scipy.optimize import minimize

def apply_cor(data,largeur_tranche=20, rx=0.5, ry=0.5):
	segs,data1,liste_seg = segment(data,rx,ry,largeur_tranche)
	data1["seg"] = closest_inlist(data1["seg"],liste_seg)	
	counter = 1
	data1["c_"] = 0
	data1["prof_moy_seg"] = 0
	for i in segs : 
		print("segment {}/{}".format(counter,len(segs)))
		c0 = 1480
		c = minimize(cout,(1480,1480),bounds=((1400,1600),(1400,1600)),args = (i,c0),options={'xtol': 1e-5},tol=0.00001)
		c1 = c.x[0]
		c2 = c.x[1]
		print(c1,c2)
		# print(c1,c2)
		# if int(cout((c0,c0),i,c0))<int(cout((c1,c2),i,c0)):
		# 	c1 = c0
		# 	c2 = c0
		print("cout initial : ",cout((c0,c0),i,c0))
		print("meilleur cout obtenu : ",cout((c1,c2),i,c0),"\n\n")
		num_seg = i["seg"].unique()[0]  
		data1["c"] = c0
		data1["teta"] = np.arccos(np.minimum(data1["z"]/(data1["c"]*data1["Two Way Travel Time"]),1))
		data1.loc[(data1.seg == num_seg) & (data1.nF == 0),"z"] = calcul_pro(data1[data1["nF"]==0]["Two Way Travel Time"],data1["teta"],c0,c1)
		data1.loc[(data1.seg == num_seg) & (data1.nF == 1),"z"] = calcul_pro(data1[data1["nF"]==1]["Two Way Travel Time"],data1["teta"],c0,c2)
		data1.loc[(data1.seg == num_seg) & (data1.nF == 0),"c_"] = c1/2+c2/2
		data1.loc[(data1.seg == num_seg) & (data1.nF == 1),"c_"] = c1/2+c2/2
		data1.loc[(data1.seg == num_seg) & (data1.nF == 1),"prof_moy_seg"] = (data1.loc[(data1.seg == num_seg) & (data1.nF == 0),"z"].mean()+data1.loc[(data1.seg == num_seg) & (data1.nF == 1),"z"].mean())/2
		data1.loc[(data1.seg == num_seg) & (data1.nF == 0),"prof_moy_seg"] = (data1.loc[(data1.seg == num_seg) & (data1.nF == 0),"z"].mean()+data1.loc[(data1.seg == num_seg) & (data1.nF == 1),"z"].mean())/2
		counter += 1 
		progrès = int(counter/len(liste_seg)*20)
	return	data1



def closest_inlist(list1,list2):
	list_return = []
	for i in list1:
		list3 = abs(list2-i)	
		list_return.append(list2[np.argmin(list3)])
	return list_return	
