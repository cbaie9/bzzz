import tkiteasy as tke
import start as frontend



# setup des classe système 
class abeille:
    def __init__(self, x:int, y:int, equipe:int, nectar:int, classe:str, etat:bool):
        self.x = x
        self.y = y
        self.equipe = equipe
        self.nectar = nectar
        self.classe = classe
        self.etat = etat


def Cas_matrice(nb_carre:int):
        
    matrice_placement_perso = [[0 for i in range(nb_carre)] for j in range(nb_carre)]


    matrice_placement_perso[1][14] = 1


    for i in range(len(matrice_placement_perso)) : 
        print(matrice_placement_perso[i])