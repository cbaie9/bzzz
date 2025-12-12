import tkiteasy as tke
import start as frontend
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


def creation_matrice_perso() -> list:
    """
    Créer la base de la matrice qui permet de suivre le déplacement des personnages
    entrée : None
    sortie : list 

    """
    matrice_placement_perso = [[0 for i in range(config.nb_carre_x)] for j in range(config.nb_carre_y)]
    return matrice_placement_perso


def creation_matrice_map() -> list : 
    """
    Créer la base de la matrice dans laquelle se trouve les emplacements des fleurs et des bases
    entrée : None 
    sortie : list
    """
    #------------------------------Création zones----------------------------------#
    #création de la zone de l'équipe 1 qui correspond au chiffre 1
    matrice_placement_map = [[0 for i in range(nb_carre)] for j in range(nb_carre)]
    for i in range(int(sqrt(nb_carre_x))) : 
        for j in range(int(sqrt(nb_carre_y))) : 
            matrice_placement_map[i][j] = 1

    #création de la zone de l'équipe 2 qui correspond au chiffre 2
    for i in range(int(sqrt(nb_carre_x))) : 
        for j in range(nb_carre-int(sqrt(nb_carre_y)),nb_carre_y) :
            matrice_placement_map[i][j] = 2

    #création de la zone de l'équipe 3 qui correspond au chiffre 3
    for i in range(nb_carre-int(sqrt(nb_carre_x)),nb_carre_y) : 
        for j in range(int(sqrt(nb_carre))) :
            matrice_placement_map[i][j] = 3

    #création de la zone de l'équipe 4 qui correspond au chiffre 4
    for i in range(nb_carre-int(sqrt(nb_carre_x)),nb_carre_y) : 
        for j in range(nb_carre-int(sqrt(nb_carre_x)),nb_carre_y) :
            matrice_placement_map[i][j] = 4


    return matrice_placement_map


def recup_coord_base(L:list)->list :
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

def affichage_matrice(L) :
    """
    Affiche la matrice passée en paramètre
    entrée : list
    sortie : None
    """
    for i in range(len(L)) :
        print(L[i])

#def emplacement_fleurs() : 
    """
    Retourne les coordonnées aléatoires pour le placement des fleurs

    """
    L_coordonnées = []

    for i in range(nb_carre) :
        for j in range(nb_carre) : 
            L_coordonnées.append((i,j))

#-----------------------------------------------------------------------------------MAIN-----------------------------------------------------------------------------------#
