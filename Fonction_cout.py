# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 11:24:28 2021

@author: Stan
"""
import pandas as pd
import numpy as np

def cout(vec_c,data,current_c):
	"""
	Calcule le cout d'un jeu de célérité donné
	data = segment 
	new_c = liste contenant les nouvelles celeritées pour les fauchées présentes dans le segment
	current_c = celeritee estimmée ou calculée précédemment pour chaque fauchee

	"""
	new_c = np.array([[vec_c[0],vec_c[1]]])
	vec_result = np.zeros((new_c.shape[0],1))

	

	for j in range(vec_result.shape[0]):
		data["c"] = 0
		data["nc"] = 0
		for i in data["nF"].unique():
			data.loc[data["nF"]==i,"c"] = current_c
			data.loc[data["nF"]==i,"nc"] = new_c[j,i]
		data["teta"] = np.arccos(data["z"]/(data["c"]*data["Two Way Travel Time"]))
		data["nvz"] = calcul_pro(data["Two Way Travel Time"], data["teta"], data["c"], data["nc"])
		moy_cases = data[["case","nvz"]].groupby("case",as_index = False).mean().rename({"nvz":"Moy"},axis = 1)
		data = data.merge(moy_cases,left_on = "case",right_on = "case",suffixes = ("_x",None))
		data["tot"] = (data["nvz"]-data["Moy"])**2       
		diff_case = data.groupby(["case"],as_index = False)["tot"].sum()
		count_cell = data["case"].value_counts(sort=False).to_frame(name = "count").reset_index()
		count_cell.columns = ["case","count"]
		diff_case = diff_case.merge(count_cell,left_on = "case", right_on = "case")
		diff_case["tot"] = np.sqrt(diff_case["tot"]/diff_case["count"])
		vec_result[j,0] += diff_case["tot"].sum()

	return vec_result[0,0]
    



def calcul_pro(travel_time, angle, ancienne_c, nouvelle_c):

    nouvel_angle = np.arcsin(np.minimum((nouvelle_c/ancienne_c)*np.sin(angle),1))
    distance = nouvelle_c*travel_time
    nouvelle_profondeur = distance*np.cos(nouvel_angle)

    return nouvelle_profondeur