import tkiteasy as tke
ymax = 600
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

g = tke.ouvrirFenetre(xmax, ymax)
# setup des classe système
class abeille:
    def __init__(self, x:int, y:int, equipe:int, nectar:int, classe:str, etat:bool):
        self.x = x
        self.y = y
        self.equipe = equipe
        self.nectar = nectar
        self.classe = classe
        self.etat = etat
def dessiner_background():
    """
    Dessine l'arrière plan du jeu en fonction des constant de base
    """
    compteur = 0
    for x in range(0,xmax,taille_carre_x):
        
        for y in range(0,ymax,taille_carre_y):
            g.pause(0.0001)
            g.update()
            if compteur == 1:
                color = 'black'
                compteur =0
            else:
                color = 'white'
                compteur += 1
            g.dessinerRectangle(x,y,taille_carre_x,taille_carre_y,color)
        if x/taille_carre_x % 2 == 0:
            compteur = 1
        else: 
            compteur = 0
dessiner_background()
# Boucle à vide qui attend un clic
g.attendreClic()

# Fermeture fenêtre
g.fermerFenetre()


