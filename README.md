# Bathycel
Code to correct probes biased by a wrong sound velocity profile

The algorithm is presented in an article T. H. Mohammadloo, M. Snellen, W. Renoud, J. Beaudoin and D. G. Simons, "Correcting Multibeam Echosounder Bathymetric Measurements for Errors Induced by Inaccurate Water Column Sound Speeds," in IEEE Access, vol. 7, pp. 122052-122068, 2019, doi: 10.1109/ACCESS.2019.2936170.

A typical exemple of use of this code is :

swath1 = pd.read_csv("swath1.txt",header=0) #with mandatory columns in swath 1: the X,Y,Z coordinates of proes (assigned as Footprint X, Footprint Y, Footprint Z), the ping number and the beam number (referenced as Ping and #Beam), the transudcer X,Y,Z (referenced as Transucer X, Transducer Y and Transducer Z)

swath2 = pd.read_csv("swath2.txt",header=0)

leve = {0:swath1, 1:swath2} 
leve = rotation_sondes(leve) # from Rotasonde import rotation_sondes
leve = transfo_donnees(leve) # from transformation_des_donnees import transfo_donnees
leve = apply_cor(leve) # from apply_cor import apply_cor

Results are presented in the pdf file and you can ask me any question @ jeremie.lambert@ensta-bretagne.org
