import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import *
from tqdm import tqdm
def MNT(leve,rx = 1,ry = 1):
	# Taille matrice :
	#m, résolution en x
	#m, résolution en y
	m = 0
	n = 0
	for i in leve:
		n = int(max(n,(leve[i]["Footprint X New"].max())//rx+1))
		m = int(max(m,(leve[i]["Footprint Y New"].max())//ry+1))

	# Création de la grille contenant les sondes
	MNT_somme = np.zeros((n,m))
	MNT_compte = np.zeros((n,m))

	# test des valeurs max et min des 2 pour vérifier qu'elles soient dans la grille MNT
	#On range les sondes dans la grille

	for j in leve:
		for i in (leve[j].index):
			try:
				MNT_somme[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])] += leve[j]["z"][i]
				MNT_compte[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])] += 1
			except :
				pass

	MNT = MNT_somme/(MNT_compte)
	return MNT


def MNT_diff(leves,rx = 1,ry = 1):
	m = 0
	n = 0
	for leve in leves:
		for i in leve:
			n = int(max(n,(leve[i]["Footprint X New"].max())//rx+1))
			m = int(max(m,(leve[i]["Footprint Y New"].max())//ry+1))

	liste_MNT_compte = []
	list_MNT = []
	liste_MNT_somme = []

	
	
	for i in range(2):
		liste_MNT_somme.append(np.zeros((n,m)))
		liste_MNT_compte.append(np.zeros((n,m)))


		# test des valeurs max et min des 2 pour vérifier qu'elles soient dans la grille MNT

	for i in range(len(leves)):
		for count,fauchee in enumerate(leves[i]):
			print("Création d'un MNT de différences étape {}/4".format((i)*2+(count+1)))
			for k in tqdm(leves[i][fauchee].index):
				liste_MNT_somme[i][int(leves[i][fauchee]["X_div_rx"][k]),int(leves[i][fauchee]["Y_div_ry"][k])] += leves[i][fauchee]["z"][k]
				liste_MNT_compte[i][int(leves[i][fauchee]["X_div_rx"][k]),int(leves[i][fauchee]["Y_div_ry"][k])] += 1
		list_MNT.append(liste_MNT_somme[i]/liste_MNT_compte[i])
	# print(np.nanstd(list_MNT[0] - list_MNT[1]))
	return list_MNT[0] - list_MNT[1]

def MNT_std(leve,rx = 1,ry = 1 ):

	# Taille matrice :
	#m, résolution en x
	#m, résolution en y
	m = 0
	n = 0

	for i in leve:
		n = int(max(n,(leve[i]["Footprint X New"].max())//rx+1))
		m = int(max(m,(leve[i]["Footprint Y New"].max())//ry+1))


	
	# Création de la grille contenant les sondes
	MNT_somme = np.zeros((n,m))
	MNT_compte = np.zeros((n,m))
	MNT_std = np.zeros((n,m))

	# test des valeurs max et min des 2 pour vérifier qu'elles soient dans la grille MNT
	##On range les sondes dans la grille

	for count1,j in enumerate(leve):
		print("Création d'un MNT d'écarts-types étape {}/4".format(count1+1))
		for i in tqdm(leve[j].index):
			MNT_somme[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])] += leve[j]["z"][i]
			MNT_compte[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])] += 1
	MNT = MNT_somme/(MNT_compte)
	for count1,j in enumerate(leve):
		print("Création d'un MNT d'écarts-types étape {}/4".format(count1+3))
		for i in tqdm(leve[j].index):
			MNT_std[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])] += (MNT[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])]-leve[j]["z"][i])**2
	MNT_std = np.sqrt(MNT_std/(MNT_compte))
	return MNT_std

def MNT_c(leve,rx = 1,ry = 1):
	# Taille matrice :
	#m, résolution en x
	#m, résolution en y
	m = 0
	n = 0
	for i in leve:
		n = int(max(n,(leve[i]["Footprint X New"].max())//rx+1))
		m = int(max(m,(leve[i]["Footprint Y New"].max())//ry+1))

	# Création de la grille contenant les sondes
	MNT_somme = np.zeros((n,m))
	MNT_compte = np.zeros((n,m))

	# test des valeurs max et min des 2 pour vérifier qu'elles soient dans la grille MNT
	#On range les sondes dans la grille

	for j in leve:
		for i in (leve[j].index):
			try:
				MNT_somme[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])] += leve[j]["c_"][i]
				MNT_compte[int(leve[j]["X_div_rx"][i])][int(leve[j]["Y_div_ry"][i])] += 1
			except :
				pass

	MNT = MNT_somme/(MNT_compte)
	return MNT