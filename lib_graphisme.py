import tkiteasy as tke # type: ignore
import start
import config


def dessiner_background():
    """
    Dessine l'arrière plan du jeu en fonction des constant de base
    """
    compteur = 0
    for x in range(0,config.xmax,config.taille_carre_x):
        
        for y in range(0,config.ymax,config.taille_carre_y):
            start.g.pause(0.0001)
            start.g.update()
            if compteur == 1:
                color = 'black'
                compteur =0
            else:
                color = 'white'
                compteur += 1
            start.g.dessinerRectangle(x,y,config.taille_carre_x,config.taille_carre_y,color)
        if x/config.taille_carre_x % 2 == 0:
            compteur = 1
        else: 
            compteur = 0