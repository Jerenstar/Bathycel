import pandas as pd
import numpy as np 
from Rotasonde import *
import time as t
def segment(fauchees,rx,ry,largeur_tranche):
	"""
	Realise la segmentation sur la liste de fauchees données en argument,
	renvoie une liste de dataframe correspondant à chaque segment
	
	Pour l'instant, la fonction ne marche que sur deux fauchées, l'implémenter 
	sur 3,4,... fauchees reste à faire


	entrée : 
	fauchee : un dictionnaire contenant les deux fauchees, que l'on aura pivoté verticalement 
	(format des fauchees contenu dans la doc)
	rx : resolution selon l'axe x
	ry : resolution selon l'axe y


	sortie : une liste contenant des data frame, chaque dataframe correspond a un segment
	les colonnes sont les memes que pour les fauchees + qq infos pr la fonction cout
	
	"""
	
	sondes = [] #Variable qui sera transformé en une concaténation des deux fauchees
	listes_seg = [] #variable qui contiendra les segments

	for i in fauchees: #concaténation + ajout d'une collone indiquant le numéro de fauchee
		fauchees[i]["nF"] = i
		sondes.append(fauchees[i])
	sondes = pd.concat(sondes,ignore_index=True)
	
	#Calcul du nombre de cases 
	dx = sondes["Footprint X"].max()-sondes["Footprint X"].min() 
	dy = sondes["Footprint Y"].max()-sondes["Footprint Y"].min()
	nb_cases_largeur = int(dx//rx)+2
	nb_cases_hauteur = int(dy//ry)+2
	
	#Attribution d'une case (x,y) à chaque sondes
	sondes["cases_x"] = (sondes["Footprint X"]//rx).astype(int)
	sondes["cases_y"] = (sondes["Footprint Y"]//ry).astype(int)
	sondes["cases_x"] -= sondes["cases_x"].min()
	sondes["cases_y"] -= sondes["cases_y"].min()

	#Attribution d'une case (reperée par un num unique au lieu de x,y) a chaque sondes
	#cette opération sera utile pour le calcul de la fct cout
	sondes["case"] = (sondes["cases_x"] + sondes["cases_y"]*nb_cases_largeur).astype(int)

	#On rajoute une collone indiquant pour chaque sondes la moyenne des sondes dans la case ou elle se trouve
	#C'est finalement la profondeur de la case qui sera utile pour le calcul de la fonction coût
	#La profondeur est calculée dans le référentiel du sondeur 
	
	sondes["z"] = sondes["Transducer Z"] - sondes["Footprint Z"]
	moy_cases = sondes[["case","z"]].groupby("case",as_index = False).mean().rename({"z":"Moy"},axis = 1)
	sondes = sondes.merge(moy_cases,left_on = "case",right_on = "case")
	sondes["seg"] = sondes["cases_y"]//largeur_tranche
	sondes_1 = sondes
	#On cherche a present les cases contenant des sondes provenant des deux fauchees 
	#Pour ca on commence par separer les fauchees
	fauchee1 = sondes[sondes["nF"]==0]
	fauchee2 = sondes[sondes["nF"]==1]

	#On crée des masques indiquant les sondes de la fauchee 1 qui partagent une case avec 
	#des sondes de la fauchee deux et vice-versa
	m1 = fauchee1["case"].isin(fauchee2["case"])
	m2 = fauchee2["case"].isin(fauchee1["case"])

	#On applique les masques
	fauchee1 = fauchee1[m1==True]
	fauchee2 = fauchee2[m2==True]
	sondes = pd.concat([fauchee1,fauchee2],ignore_index=True)
	#Dans sondes, il ne reste plus que des sondes situées dans des cases 
	#où les sondes proviennent des deux fauchees

	#Puisque on a pivoter les fauchees de manière verticale, on peut donc trouver dans quel segment
	#ranger chaque sondes en utilisant sa coordonée verticale
	sondes["seg"] = sondes["cases_y"]//largeur_tranche
	
	#On crée les segments
	for i in sondes["seg"].unique():
		seg = sondes[sondes["seg"]==i]
		listes_seg.append(seg)

	return listes_seg,sondes_1,sondes["seg"].unique()

if __name__ == "__main__":
	data_1 = pd.read_csv("20211004_155627 - L1 - 0001.filt_40.txt",header=0)
	data_2 = pd.read_csv("20211004_155449 - L1 - 0001.filt_38.txt",header=0)
	fauchees = {0:data_1,1:data_2}
	fauchees = rotation_sondes(fauchees)
	segment(fauchees,0.5,0.5)