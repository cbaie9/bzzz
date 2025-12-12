import tkiteasy as tke
# import start as frontend
import config 
from random import * 
from math import * 


# setup des classe système 
class abeille:
    def __init__(self, x:int, y:int, equipe:int, nectar:int, classe:str, etat:bool):
        self.x = x
        self.y = y
        self.equipe = equipe

        self.nectar = nectar
        self.classe = classe
        self.etat = etat


def creation_matrice_perso() -> list[list[int]]:
    """
    Créer la base de la matrice qui permet de suivre le déplacement des personnages
    entrée : None
    sortie : list 

    """
    matrice_placement_perso = [[0 for i in range(config.nb_carre_x)] for j in range(config.nb_carre_y)] # pyright: ignore[reportUnusedVariable]
    return matrice_placement_perso


def creation_matrice_map() -> list[list[int]] : 
    """
    Créer la base de la matrice dans laquelle se trouve les emplacements des fleurs et des bases
    entrée : None 
    sortie : list
    """
    #------------------------------Création zones----------------------------------#
    #création d'une matrice assiocié à la carte vide
    matrice_placement_map = [[0 for i in range(config.nb_carre_x)] for j in range(config.nb_carre_y)] # pyright: ignore[reportUnusedVariable]
    #création des spawn d'équipe    
    for x in range(1,5):
        if x == 1:
            range_x1 = 0
            range_x2 = int(sqrt(config.nb_carre_x)) # configuration pour l'équipe 1
            range_y1 = 0
            range_y2 = int(sqrt(config.nb_carre_y))
        elif x == 2: #création de la zone de l'équipe 2 qui correspond au chiffre 2
            range_y1 = config.nb_carre-int(sqrt(config.nb_carre_y))
            range_y2 = config.nb_carre_y
        elif x == 3: #création de la zone de l'équipe 3 qui correspond au chiffre 3
            range_x1 = config.nb_carre_x-int(sqrt(config.nb_carre_x))
            range_x2 = config.nb_carre_x
            range_y1 = 0
            range_y2 = int(sqrt(config.nb_carre_y))
        elif x == 4: #création de la zone de l'équipe 4 qui correspond au chiffre 4
            range_x1 = config.nb_carre-int(sqrt(config.nb_carre_x))
            range_x2 = config.nb_carre_y
            range_y1 = config.nb_carre_y-int(sqrt(config.nb_carre_y))
            range_y2 = config.nb_carre_y
        else: # break au cas la cycle suivante si problème
            break
        for i in range(range_x1,range_x2) :  # pyright: ignore[reportPossiblyUnboundVariable]
            for j in range(range_y1,range_y2) : # pyright: ignore[reportPossiblyUnboundVariable]
                matrice_placement_map[i][j] = x
    return matrice_placement_map


#def recup_coord_base(L:list[list[int]])->list :
    """
    Créer une liste de liste contenant les coordonnées des emplacement des différentes zones d'équipes
    entrée : list
    sortie : list
    """
    L_coord_case = [[],[],[],[]]
    for i in range(len(L)) : 
        for j in range(len(L[i])) : 
            if L[i][j] == 1 : 
                L_coord_case[0].append((i,j))
            elif L[i][j] == 2 : 
                L_coord_case[1].append((i,j))
            elif L[i][j] == 3 : 
                L_coord_case[2].append((i,j))
            elif L[i][j] == 4 : 
                L_coord_case[3].append((i,j))
    return L_coord_case

def affichage_matrice(L : list[list[int]]) :
    """
    Affiche la matrice passée en paramètre
    entrée : list
    sortie : None
    """
    for i in range(len(L)) :
        print(L[i])

# def emplacement_fleurs() : 
    """
    Retourne les coordonnées aléatoires pour le placement des fleurs

    """
    # L_coordonnées : list[list[int]]= []

   # for i in range(config.nb_carre_x) :
       # for j in range(config.nb_carre_y) :
         #   pass
            # print(i,j)
           # L_coordonnées.append((i,j)) 

#-----------------------------------------------------------------------------------MAIN-----------------------------------------------------------------------------------#
affichage_matrice(creation_matrice_map())
