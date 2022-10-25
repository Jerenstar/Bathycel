import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
import time as t

def rotation_sondes(leve,n=400):
	fauche_min = 0
	first_sonde = leve[fauche_min][(leve[fauche_min]["Ping"] == leve[fauche_min]["Ping"].min())].mean()
	X_min = leve[fauche_min].groupby("Ping").median()["Footprint X"].min()
	Y_min = leve[fauche_min].groupby("Ping").median()["Footprint Y"].min()
	X_max = leve[fauche_min].groupby("Ping").median()["Footprint X"].max()
	Y_max = leve[fauche_min].groupby("Ping").median()["Footprint Y"].max()
	for i in leve:
		leve[i]["Footprint X"] = leve[i]["Footprint X"] - X_min
		leve[i]["Footprint Y"] = leve[i]["Footprint Y"] - Y_min
		leve[i]["z"] = leve[i]["Transducer Z"] - leve[i]["Footprint Z"]
		
	##On calcule l'angle de rotation en utilisant le faisceau au nadir, l'hypoth

	last_sonde = leve[fauche_min][(leve[fauche_min]["Ping"] == leve[fauche_min]["Ping"].max())].mean()
	
	theta =  float(np.arctan(Y_max/X_max))
	R_theta = np.array([[-np.sin(theta),np.cos(theta)],[-np.cos(theta),-np.sin(theta)]])
	
	for i in leve:
		X_Y = leve[i][["Footprint X" , "Footprint Y"]]
		X_Y = np.array(X_Y)
		X_Y_p = R_theta@X_Y.T
		leve[i][["Footprint X", "Footprint Y"]] = X_Y_p.T
	return leve


