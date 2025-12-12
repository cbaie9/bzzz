ymax = 800
xmax = 800
nb_carre = 16
if nb_carre == 16:
    nb_carre_y = 16
    nb_carre_x = 16
else:
    nb_carre_x = nb_carre
    nb_carre_y = nb_carre
taille_carre = xmax
taille_carre_x = int(xmax//nb_carre_x)
taille_carre_y = int(ymax//nb_carre_y)