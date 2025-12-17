#import tkiteasy as tke
#import start as frontend
import config 
from random import choice


# setup des classe système 
class abeille:
    def __init__(self, x:int, y:int, equipe:int, nectar:int, classe:str, etat:bool, id:int):
        self.x :int = x # Postion x du l'abeille
        self.y :int = y # Postion y de d'abeille
        self.equipe :int = equipe # Numero de l'équipe de l'abeille (Entre 1 et 4 compris)
        self.nectar :int = nectar # Nombre de nectar que porte l'abeille actuelle 
        self.classe :str = classe # Classe de l'abeille (Esclaireuse etc)
        self.etat :bool = etat # True = Vivant | False = KO
        self.id :int = id # id de l'abeille UNIQUE 


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
            range_x2 = int(config.taille_spawn_x) # configuration pour l'équipe 1
            range_y1 = 0
            range_y2 = int(config.taille_spawn_y)
        elif x == 2: #création de la zone de l'équipe 2 qui correspond au chiffre 2
            range_y1 = config.nb_carre-int(config.taille_spawn_y)
            range_y2 = config.nb_carre_y
        elif x == 3: #création de la zone de l'équipe 3 qui correspond au chiffre 3
            range_x1 = config.nb_carre_x-int(config.taille_spawn_x)
            range_x2 = config.nb_carre_x
            range_y1 = 0
            range_y2 = int(config.taille_spawn_y)
        elif x == 4: #création de la zone de l'équipe 4 qui correspond au chiffre 4
            range_x1 = config.nb_carre-int(config.taille_spawn_x)
            range_x2 = config.nb_carre_y
            range_y1 = config.nb_carre_y-int(config.taille_spawn_y)
            range_y2 = config.nb_carre_y
        else: # break au cas la cycle suivante si problème
            break
        for i in range(range_x1,range_x2) :  # pyright: ignore[reportPossiblyUnboundVariable]  |  range_x1 et range_x2 sont forcement defini sinon break
            for j in range(range_y1,range_y2) : # pyright: ignore[reportPossiblyUnboundVariable] | range_y1 et range_y2 sont forcement defini sinon break
                matrice_placement_map[i][j] = x
        #placement des fleurs à l'aide de la fonction "emplacement_fleurs(L_coord_case)"
    L_emplacement_fleur = emplacement_fleurs(liste_coord_possible())

    for i in range(len(L_emplacement_fleur)) : 
        x,y = L_emplacement_fleur[i]
        matrice_placement_map[x][y] = 10+config.nectar_initial
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

def case_valide(x:int,y:int,equipe:int)-> bool:
    
    if map[x][y] == 0 or map[x][y] == equipe:
        output = True
    else :
        output = False
    return output
def emplacement_fleurs(L_coord_case : list[tuple[int,int]]) : 
    """
    Retourne les coordonnées aléatoires pour le placement des fleurs

    """
    L_coord_fleur :list[tuple[int,int]]= []
    L_coord_fleur_temp :list[tuple[int,int]]= []
    for i in range(int(config.nb_carre//4)) :  #on choisit au hasard 4 coordonnées pour les fleurs
        L_coord_fleur.append(choice(L_coord_case))
    

    for i in range(4) : #on construit la symétrie 
        x,y = L_coord_fleur[i]
        L_coord_fleur_temp.append((config.nb_carre_x-1-x,y))
        L_coord_fleur_temp.append((x,config.nb_carre_x-1-y))
        L_coord_fleur_temp.append((config.nb_carre_x-1-x,config.nb_carre_x-1-y))

    for i in range(len(L_coord_fleur_temp)) : #on importe les coordonnées stockées dans la liste tampon dans la liste finale
        L_coord_fleur.append(L_coord_fleur_temp[i])
    
    return L_coord_fleur

def liste_coord_possible()-> list[tuple[int,int]]: 
    """
    Renvoie la liste des coordonnées qui ne correspondent pas à une base
    entrée : list
    sortie : list
    """
    L_coord_sans_base :list[tuple[int,int]]= []

    for i in range(int(config.taille_spawn_x), int(config.nb_carre_x//2)) : 
        for j in range(int(config.taille_spawn_y)) :
            L_coord_sans_base.append((i,j))

    for i in range(config.nb_carre_x//2) : 
        for j in range(int(config.taille_spawn_y),config.nb_carre_y//2) : 
            L_coord_sans_base.append((i,j))

    return L_coord_sans_base
#-----------------------------------------------------------------------------------MAIN-----------------------------------------------------------------------------------#

map = creation_matrice_map()
affichage_matrice(map)