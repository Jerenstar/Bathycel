import pandas as pd
import numpy as np
def transfo_donnees(leve,rx=1,ry=1):
	xmin = 1e18
	ymin = 1e18
	xmax = -1e18
	ymax = -1e18
	for i in leve:
		xmin = np.minimum(leve[i]["Footprint X"].min(),xmin)
		ymin = np.minimum(leve[i]["Footprint Y"].min(),ymin)
		xmax = np.maximum(leve[i]["Footprint X"].max(),xmax)
		ymax = np.maximum(leve[i]["Footprint Y"].max(),ymax)

	# Repère local
	for i in leve:
		leve[i]["Footprint X New"] = leve[i]["Footprint X"] - xmin 
		leve[i]["Footprint Y New"] = leve[i]["Footprint Y"] - ymin 
		leve[i]["X_div_rx"]=leve[i]["Footprint X New"]//rx
		leve[i]["Y_div_ry"]=leve[i]["Footprint Y New"]//ry
		leve[i]["z"] = leve[i]["Transducer Z"] - leve[i]["Footprint Z"]
		
	return leve