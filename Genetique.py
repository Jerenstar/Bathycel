import numpy as np
from tqdm import tqdm
def genetique(data, pt_depart, bounds, f, q=16, F=0.6, pc=0.55, Ng=20, D=2):
	dc  = bounds[1]-bounds[0]
	vect_0 = np.random.random((q,D))*dc+bounds[0]
	#first vector	
	for i in tqdm(range(Ng)):
		#We take the n best values of vect_0 to generate a new vector 
		n = 5
		result_vect_0 = f(data,vect_0,pt_depart)
		vect_generateur = np.zeros((n,D))
		for k in range(int(F*q)):
			vect_generateur[k] = vect_0[np.argmin(result_vect_0)]
			result_vect_0[np.argmin(result_vect_0)] = np.max(result_vect_0)
		V_ip1 = np.zeros((q,D))
		###Croisement
		for k in range(q-int(F*q)):
			a,b,c = ind[0],ind[1],ind[2]
			V_ip1[int(F*q)+k] = np.array([vect_generateur[a][0],vect_generateur[b][0]])
			
		### Croisement
		vect_croisement = np.random.random((q,D))
		U_ip1 = V_ip1
		U_ip1 = np.where(vect_croisement<pc,U_ip1,vect_0)

		###selection
		res_int = f(data,U_ip1,pt_depart)
		

		if np.min(res_int)<np.min(result_vect_0):
			vect_0 = U_ip1
	
	# print(vect_0[np.argmin(f(data,vect_0,pt_depart))],f(data,vect_0,pt_depart)[np.argmin(f(data,vect_0,pt_depart))])
	return vect_0[np.argmin(f(data,vect_0,pt_depart))]
	

	
def aleat(list_exc,extent,n):
	list_return = []
	delta = extent[1]-extent[0]
	while len(list_return) < n:
		r = int(np.random.random()*(delta))
		if r not in list_exc :
			list_exc.append(r)
			list_return.append(r)
	return  list_return

