#import tkiteasy as tke
#import lib_graphisme
import config 
from random import choice
import random
import lib_graphisme

# setup des classe système 
class abeille:
    def __init__(self, x:int, y:int, equipe:int, classe:str):
        self.x :int = x # Postion x du l'abeille
        self.y :int = y # Postion y de d'abeille
        self.equipe :int = equipe # Numero de l'équipe de l'abeille (Entre 1 et 4 compris)
        self.nectar :int = 0 # Nombre de nectar que porte l'abeille actuelle 
        self.classe :str = classe # Classe de l'abeille (Esclaireuse etc)
        self.compteur_KO = 0
        self.etat :bool = True # True = Vivant | False = KO
        if equipe == 1:
            self.id :int = config.id_actuelle_J1 # id de l'abeille UNIQUE 
            config.id_actuelle_J1 += 1
        elif equipe == 2:
            self.id :int = config.id_actuelle_J2
            config.id_actuelle_J2 += 1
        elif equipe == 3:
            self.id :int =config.id_actuelle_J3
            config.id_actuelle_J3 += 1
        else:
            self.id :int = config.id_actuelle_J4
            config.id_actuelle_J4 += 1
        self.x_old :int = x
        self.y_old :int = y
        #self.img :tke.ObjetGraphique= lib_graphisme.g.afficherImage(self.x,self.y,'./image/abeille_menu.png')
        # calcul de la force/nectar_max en fonction de la classe
        force :int 
        nectar_max :int
        if classe == "bourdon":
            force = 5
            nectar_max = 1
        elif classe == "eclaireuse":
            force = 1
            nectar_max = 3
        elif classe == "ouvrière":
            force = 1
            nectar_max = 12
        else :
            force = 1
            nectar_max = 1
        self.force = force
        self.nectar_max = nectar_max
        self.FE :int = 0
        self.autodep :tuple[bool,tuple[int,int]] = (False,(0,0))
class joueur:
    def __init__(self, list_abeille:list[abeille]) -> None:
        self.list_abeille = list_abeille # liste d'abeille des joueurs
        self.id = config.id_actuelle_joueur
        config.id_actuelle_joueur += 1
        self.nectar = config.nectar_initial
class clic_custom:
    def __init__(self, x:int,y:int) -> None:
        self.x = x # Position x du clic
        self.y = y # Position y du clic
        

def creation_matrice_perso() -> list[list[int]]:
    """
    Créer la base de la matrice qui permet de suivre le déplacement des personnages
    entrée : None
    sortie : list 

    """
    matrice_placement_perso = [[0 for _ in range(config.nb_carre_x)] for _ in range(config.nb_carre_y)] 
    return matrice_placement_perso


def creation_matrice_map(testing :bool = False) -> list[list[int]] : 
    """
    Créer la base de la matrice dans laquelle se trouve les emplacements des fleurs et des bases
    entrée : None 
    sortie : list
    """
    #------------------------------Création zones----------------------------------#
    #création d'une matrice assiocié à la carte vide
    matrice_placement_map = [[0 for _ in range(config.nb_carre_x)] for _ in range(config.nb_carre_y)]
    #création des spawn d'équipe    
    for x in range(1,5):
        if x == 1:
            range_x1 = 0
            range_x2 = int(config.taille_spawn_x) # configuration pour l'équipe 1
            range_y1 = 0
            range_y2 = int(config.taille_spawn_y)
        elif x == 2: #création de la zone de l'équipe 3 qui correspond au chiffre 3
            range_x1 = config.nb_carre_x-int(config.taille_spawn_x)
            range_x2 = config.nb_carre_x
            range_y1 = 0
            range_y2 = int(config.taille_spawn_y)
        elif x ==3 :
            range_x1 = 0
            range_x2 = int(config.taille_spawn_x)
            range_y1 = config.nb_carre-int(config.taille_spawn_y)
            range_y2 = config.nb_carre_y
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
    if testing:
        return matrice_placement_map
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

def case_valide(abeille:abeille)-> bool:
    """
    Docstring for case_valide

    Renvoie si on peut se déplacer sur la case en fonction de la position actuel, de l'équipe, de la classe de l'abeille et la position où le joueur veut se déplacer
    
    :param x: Position x ou le joueur a cliquer / veut se déplacer
    :type x: int
    :param y: Position y ou le joueur a cliquer / veut se déplacer
    :type y: int
    :param equipe: équipe du joueur
    :type equipe: int
    :param class_ab: Classe de l'abeille que le joueur veut déplacer
    :type class_ab: str
    :param y_old: Position y où l'abeille est actuellement
    :type y_old: int
    :param x_old: Position x où l'abeille est actuellement
    :type x_old: int
    :return: Renvoie si la case est valide
    :rtype: bool
    """
    output2 = False
    compteur = 0
    print(f"verif {abeille.equipe}, {abeille.x} | {abeille.y}")
    if  ((not 0<=abeille.y<config.nb_carre)or (not 0<=abeille.y<config.nb_carre))  and (not abeille.etat) : # empêche les déplacement dans la partie stat de l'écran ou que l'abeille soit KO
        return False
    if map[abeille.x][abeille.y] == 0 or (map[abeille.x][abeille.y] == abeille.equipe or (10 <= map[abeille.x][abeille.y] <= (10 + config.max_nectar) )):
        output = False
        if abeille.classe == 'ouvrière' or abeille.classe == 'bourdon':
            if ((abeille.x_old+1 == abeille.x or abeille.x_old == abeille.x or abeille.x_old-1 == abeille.x) and abeille.y == abeille.y_old) or (abeille.x_old == abeille.x and (abeille.y == abeille.y_old or abeille.y == abeille.y_old+1 or abeille.y == abeille.y_old-1)):
                output = True
        elif abeille.classe == 'eclaireuse':
            if ((abeille.x_old+1 == abeille.x) or (abeille.x_old == abeille.x) or (abeille.x_old-1 == abeille.x)) and ((abeille.y == abeille.y_old) or (abeille.y == abeille.y_old+1) or (abeille.y == abeille.y_old-1)):
                output = True
        elif abeille.classe == 'debug':
            output = True
    else :
        output = False
    if output:
        import lib_graphisme # import limité sinon crash
        for x in range(len(lib_graphisme.Players)): # for pour le nombre de joueur
            #print(x)
            liste_joueur_actuelle = lib_graphisme.Players[x].list_abeille # liste d'abeille pour le joueur actuelle
            for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
                if liste_joueur_actuelle[y].x == abeille.x and liste_joueur_actuelle[y].y == abeille.y :
                    compteur += 1
        if compteur == 1 or compteur == 0:
            output2 = True
    return output and output2 and abeille.etat
def emplacement_fleurs(L_coord_case : list[tuple[int,int]]) : 
    """
    Retourne les coordonnées aléatoires pour le placement des fleurs

    """
    L_coord_fleur :list[tuple[int,int]]= []
    L_coord_fleur_temp :list[tuple[int,int]]= []
    for i in range(int(config.nb_fleur)) :  #on choisit au hasard 4 coordonnées pour les fleurs
        L_coord_fleur.append(choice(L_coord_case))
    

    for i in range(config.nb_fleur) : #on construit la symétrie 
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
def velo_menu() -> tuple[int,int]:
    """
    Docstring for velo_menu
    
    :return: Renvoie un tuple donnant un velocité aléatoire à l'abeille du menu
    :rtype: tuple[int, int]
    """
    if random.randint(1,2) == 1: # randomisation de la direction de lancement (axe x)
        vx = 10
    else :
        vx = -10
    if random.randint(1,2) == 1: # randomisation de la direction de lancement (axe y)
        vy = 10
    else :
        vy = -10
    return vx,vy
def get_list_deplacement(x :int, y:int,mode:int =1 ) -> list[tuple[int,int]]:
    """
    Docstring for get_list_deplacement
    - Renvoie une liste preliminaire pour l'affichage des case déplacable

    Mode = 1 Renvoie les position autour du joueur dans la liste ( Par défault ) -> deplacement pour les abeille de type eclaireuse
    Mode = 2 Renvoie les position acessible par les bourdon et les ouvrière ( deplacement)
    Mode = 3 : Ne renvoie pas la position du joueur mais uniquement les case autour ( liste escarmouche)

    :param x: Position actuelle du joueur ( axe x )
    :type x: int
    :param y: Position actuelle du joueur ( axe y )
    :type y: int
    :return: Liste des position potencielle où le joueur peut se déplacer
    :rtype: list[tuple[int, int]]
    """
    list_deplace :list[tuple[(int,int)]] = []
    # première colonne
    if x > 0 :
        if (y > 0 and (not mode == 2)) and (not ya_quelqun(x-1,y-1) or mode == 3):
            list_deplace.append(((x-1,y-1)))
        if (not ya_quelqun(x-1,y) or mode == 3):
            list_deplace.append((x-1,y))
        if y < config.nb_carre and (not mode ==2) and (not ya_quelqun(x-1,y+1) or mode == 3):
            list_deplace.append((x-1,y+1))
    # deuxième colonne
    if y > 0 and (not ya_quelqun(x,y-1) or mode == 3) :
        list_deplace.append((x,y-1))
    if mode == 1 or mode == 2:
        list_deplace.append((x,y)) # deplacement sur place ( ne bouge pas)
    if y+1 < config.nb_carre_y and (not ya_quelqun(x,y-1) or mode == 3):
            #print(f"[debug]:[fonc:get_list_deplacement]:{y}, {config.nb_carre_y}")
            list_deplace.append((x,y+1))
    # trosième colonne
    if x+1 < config.nb_carre_x : 
        if y > 0 and (not mode == 2) and (not ya_quelqun(x+1,y-1) or mode == 3):
            list_deplace.append((x+1,y-1))
        if (not ya_quelqun(x+1,y) or mode ==3):
            list_deplace.append((x+1,y))
        if (y+1 < config.nb_carre and (not mode == 2)) and (not ya_quelqun(x+1,y+1) or mode == 3):
            list_deplace.append((x+1,y+1))
    #print(f"[debug]:[fonc]:[get_list_deplacement]: {list_deplace}")
    return list_deplace
def est_Butinable(x:int,y:int)-> bool:
    """
    Docstring for est_Butinable

    Renvoie un booléan si la position est une fleur qui est butinable
    
    :param x: Position x que l'on veut verifié
    :type x: int
    :param y: Position y que l'on veut verifié
    :type y: int
    :return: True or False
    :rtype: bool
    """
    output = False
    if x < 0 or y < 0 or y >= config.nb_carre or x >= config.nb_carre: # sécurité anti oob
        return False
    elif 10 < map[x][y] <= config.max_nectar: 
        output = True   
    return output
def Butinage(abeille:abeille,x:int,y:int)-> int:
    """
    Docstring for Butinage
    Butine la fleur à la postion et ajoute le nectar a l'abeille
    
    :param abeille: abeille qui butine 
    :type abeille: abeille
    :param x: Position x de l'abeille 
    :type x: int
    :param y: Position y de l'abeille
    :type y: int

    MAJ : Retourne le nectar que l'on doit donnée a abeille avec un appel de type
    abeille.nectar += butinage(abeille,abeille.x,abeille.y)
    Note pour raison pratique pensez a actualiser les stat après l'appel ( non obligatoire mais instinctif pour debug et le joueur)
    """
    if est_Butinable(x,y) and (0<=abeille.nectar<abeille.nectar_max): # verification coté server + coté abeille
            # determine si la case demandé est dans la map
        print(f"erreur de oob x ={x}, y : {y}")
        if not (0 <= x < config.nb_carre_x and 0 <= y < config.nb_carre_y-1):
            
            print(f"{config.taille_carre_x},   {config.taille_carre_y}")
            return False
        if abeille.nectar+config.nectar_par_butinage <= abeille.nectar_max and (map[x][y]-config.nectar_par_butinage >= 10):
            abeille.nectar =+ config.nectar_par_butinage # transfère "normal"
            map[x][y] -= config.nectar_par_butinage
            print('btnage-normal')
            return config.nectar_par_butinage
        else: # si l'un des coté ne peut plus faire de transfère par config.nectar_par_butinage alors on le fait manuellement pas 1
            map[x][y] -= 1
            return 1
    else :
        return 0
def get_list_abeille(joueur :joueur)-> list[abeille] | list[int]:
    """
    Docstring for get_list_abeille
    Renvoie la liste des abeille du joueur ( non utilisé dans le code mais la )
    
    :param joueur: Description
    :type joueur: joueur
    :return: Description
    :rtype: list[abeille] | list[int]
    """
    if 1<=joueur.id<=4:
        output = joueur.list_abeille
    else:
        assert(f"Erreur : Le nombre de joueur doit être entre 1 et 4 compris - actuellemement {joueur.id}")
        output = [-1]
    return output

def get_spawn_coor(j:int,mode:int = 3)-> type[tuple[int,int]] | int:
    """
    Docstring for get_spawn_coor
    
    :param j: Numéro du joueur compris entre 1 et 4
    :type j: int
    :param mode: Mode de la fonction :

    Mode 1: Renvoie la coordonnées x du spawn du joueur choisi
    Mode 2: Renvoie la coordonnées y du spawn du joueur choisi
    :type mode: int
    :return: Coordonnées 
    :rtype: type[tuple[int, int]] | int
    """
    if 1<=j<=4:
        if j == 1:
            if mode == 3:
                output = tuple[int(0),int(0)]
            else: 
                output = 0
        elif j == 2:
            if mode == 1:
                output = int(config.nb_carre_x-1)
            elif mode == 2:
                output = 0
            else:
                output = tuple[int(config.nb_carre_x-1),int(0)]
        elif j == 3:
            if mode == 1:
                output = 0
            elif mode == 2:
                output = int(config.nb_carre_y-1)
            else:
                output = tuple[int(0),int(config.nb_carre_y-1)]
        else:
            if mode == 1:
                output = config.nb_carre_x-1
            elif mode == 2:
                output = config.nb_carre_y-1
            else:
                output = tuple[int(config.nb_carre_x-1),int(config.nb_carre_y-1)]
    else:
        assert(f"Erreur : Le nombre de joueur doit être entre 1 et 4 compris - actuellemement {j}")
        if mode == 3:
            output = tuple[config.nb_carre_x//2,config.nb_carre_y//2]
        else:
            output = config.nb_carre//2
    return output
def ya_quelqun(x:int,y:int)->bool:
    """
    Docstring for ya_quelqun
    -> Renvoie un booléen en fonction si une abeille se trouve sur la position demandé

    :param x: Position en l'axe x
    :type x: int
    :param y: Position en l'axe y
    :type y: int
    :return: Oui s'il y a une entité sur la case, l'inverse sinon
    :rtype: bool
    """
    import lib_graphisme
    for forx in range(len(lib_graphisme.Players)): # for pour le nombre de joueur
        liste_joueur_actuelle :list[abeille] = lib_graphisme.Players[forx].list_abeille # liste d'abeille pour le joueur actuelle
        for fory in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            if liste_joueur_actuelle[fory].x == x and liste_joueur_actuelle[fory].y == y:
                return True
    return False
def creation_abeille(joueur:joueur,classe:str) :
    """
    Docstring for creation_abeille
    -> ajoute une nouvelle abeille à la liste du joueur passé en paramètre si la case du spawn n'est pas déjà occupée et qu'il possède suffisemment de nectar

    :param joueur: joueur
    :type joueur: joueur
    :param classe: bourdon éclaireuse ou l'autre
    :type classe: str
    """
    print("#çamarchepas mais azy")
    x_spawn = int(get_spawn_coor(joueur.id+1,1))  # type: ignore # voir defininition fonction pour les erreur 
    y_spawn = int(get_spawn_coor(joueur.id+1,2))    # type: ignore
    #             return None #on retourne None afin de pouvoir vérifier certaines conditions dans le lib_graphisme lors de la création d'une nouvelle abeille 
    if not ya_quelqun(x_spawn,y_spawn) : #si l'espace n'est pas occupé 
        if joueur.nectar >= config.cout_ponte : #si le joueur possède suffisemment de nectar
            print(f"[fonction creation abeille]: retour abeille valide-> sortie de la fonction")
            return  abeille(x_spawn, y_spawn, joueur.id+1,classe) #on créer une nouvelle entrée de la classe abeille, on fait joueur.id +1 car c'est {0,1,2,3} != {1,2,3,4}
        
    else :
        return None # s'il n'a pas suffisemment de nectar 
def map_info(x:int,y:int)->list[int|str]:
    """
    Docstring for ya_quelqun
    -> Renvoie les information ( équipe + classe )de l'abeille en fonction si une abeille se trouve sur la position demandé

    
    le renvoie sous la forme [equipe,classe]
    :param x: Position en l'axe x
    :type x: int
    :param y: Position en l'axe y
    :type y: int
    :return: Oui s'il y a une entité sur la case, l'inverse sinon
    :rtype: bool
    """
    import lib_graphisme
    for forx in range(len(lib_graphisme.Players)): # for pour le nombre de joueur
        liste_joueur_actuelle :list[abeille] = lib_graphisme.Players[forx].list_abeille # liste d'abeille pour le joueur actuelle
        for fory in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            if liste_joueur_actuelle[fory].x == x and liste_joueur_actuelle[fory].y == y:
                return [liste_joueur_actuelle[fory].equipe,liste_joueur_actuelle[fory].classe]
    return [0,'rien']
def escarmouche()->list[tuple[int,int]]:
    """
    Docstring for escarmouche
    

    Fonction gèrant le fonctionnement général des escarmouche avec la detection, le calcul des probabilité d'esquive et le renvoie d'une liste des abeille qui sont tombée au combat ( KO )
    :return: Liste des abeille KO
    :rtype: list[tuple[int, int]]
    """
    escar = False
    liste_FE = []
    Fe_oppo = 0
    print(f"[fonction escarmouche]:Verfication")
    list_ko : list[tuple[int,int]] = []
    for x in range(len(lib_graphisme.Players)): # for pour le nombre de joueur
        liste_joueur_actuelle :list[abeille] = lib_graphisme.Players[x].list_abeille # liste d'abeille pour le joueur actuelle
        for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            liste_position_autour = get_list_deplacement(liste_joueur_actuelle[y].x,liste_joueur_actuelle[y].y,3)
            for xl in range(len(liste_position_autour)-1):
                # verification des position autour des abeille
                tuple_xy = liste_position_autour[xl]
                if ya_quelqun(tuple_xy[0],tuple_xy[1]):
                    abeille_ennemis = get_abeille_pos(tuple_xy[0],tuple_xy[1]) # On obtient l'abeille au point où on a detecté via ya_qqun() qui l'y avais un avais une abeille
                    # verification si l'abeille n'est pas allié et qu'elle n'est pas déjà KO
                    if isinstance(abeille_ennemis,abeille):
                        if (not abeille_ennemis.equipe-1 == lib_graphisme.Players[x].id) and liste_joueur_actuelle[y].etat == True: # Verication si l'abeille est ennemis et notre abeille en état de combat
                            # escarmouche confirmée : acquisition des information préliminaire (FE)
                            print("[fonction escarmouche]: préparation de l'escarmouche")
                            escar = True
                            liste_FE :list[int]
                            liste_FE.append(abeille_ennemis.FE) # pyright: ignore[reportUnknownMemberType] Liser la ligne du dessus enft
                    else :
                            print("escarmouche annulé : abeille non trouvé par get_abeille_pos() ")
                if escar:
                    random_number = random.random()
                    for sumx in range(len(liste_FE)):
                        Fe_oppo += liste_FE[sumx] # calcul FE opposant
                    chance_equive = liste_joueur_actuelle[y].force / (liste_joueur_actuelle[y].force + Fe_oppo)
                    if random_number<chance_equive:
                        print(f"Le joueur {x} a reussi l'esquive")
                        escar = False
                    else : 
                        print(f"Le joueur {x} à rate son esquive il sera ko pour {config.Time_KO} tours")
                        list_ko.append((x,y))
                        escar = False
    return list_ko
def get_oppo(liste:list[tuple[int,int]])->int:
    """

    Docstring for get_oppo
    Renvoie le nombre d'opposant dans la liste de position donnée
    
    :param liste: Liste de position où il faut verifier s'il y a un opposant
    :type liste: list[tuple[int, int]]
    :return: Le nombre d'opposant dans la liste donnée
    :rtype: int
    """
    oppo = 0
    for liste_autour in range(len(liste)-1):
        tuple_xy = liste[liste_autour]
        if ya_quelqun(tuple_xy[0],tuple_xy[1]):
            oppo += 1
    return oppo
def get_abeille_pos(xv:int,yv:int)->abeille|None:
    """
    Docstring for get_abeille_pos

    Fonction renvoie renvoyant l'abeille se trouvant sur la position donnés s'il y en une
    Appel conseille avec ya_quelqun() pour le résultat ne renvoie pas de None
    
    :param xv: Position x de l'abeille a trouvé
    :type xv: int
    :param yv: Position y de l'abeille a trouvé
    :type yv: int
    :return: L'abeille trouvé" s'il y en a à cette position
    :rtype: abeille | None
    """
    for x in range(len(lib_graphisme.Players)): # for pour le nombre de joueur
        liste_joueur_actuelle :list[abeille] = lib_graphisme.Players[x].list_abeille # liste d'abeille pour le joueur actuelle
        for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            if liste_joueur_actuelle[y].x == xv and liste_joueur_actuelle[y].y == yv:
                return liste_joueur_actuelle[y]

def update_abeille():
    """
    Docstring for update_abeille

    Fonction qui met a jour les carasteritique de l'abeille comme son état de retablisement ou le calcul de force effective avec son nombre d'opposant
    """
    for x in range(len(lib_graphisme.Players)): # for pour le nombre de joueur
        liste_joueur_actuelle :list[abeille] = lib_graphisme.Players[x].list_abeille # liste d'abeille pour le joueur actuelle
        for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            div = get_oppo(get_list_deplacement(liste_joueur_actuelle[y].x,liste_joueur_actuelle[y].y,3))
            if not div == 0:
                liste_joueur_actuelle[y].FE = liste_joueur_actuelle[y].force // div
            else:
                liste_joueur_actuelle[y].FE = liste_joueur_actuelle[y].force
            retabli = False
            if not liste_joueur_actuelle[y].etat:
                liste_joueur_actuelle[y].compteur_KO -= 1
                retabli = True
            if liste_joueur_actuelle[y].compteur_KO == 0:
                liste_joueur_actuelle[y].etat = True
                if retabli:
                    print(f"Fin de Tour : L'abeille {y} du joueur {x+1} (classe : {liste_joueur_actuelle[y].classe}) peut maintenant de nouveau jouer")
            else:
                print(f"Il reste plus que {liste_joueur_actuelle[y].compteur_KO} tour avant que l'abeille {y} du joueur {x+1} puissent rejouer")
def auto_deplacement_list(abeille_j:abeille,clic:clic_custom)->tuple[bool,tuple[int,int]]:
    """
    Docstring for auto_deplacement_list

    
    :param abeille_j: A1beille a déplacer au point x,y
    :type abeille_j: abeille
    :param x: Position sur l'axe x où on veut déplacer l'abeille
    :type x: int
    :param y: Position sur l'axe y où on veut déplacer l'abeille
    :type y: int
    :return: Tuple contenant les info permettant de créer un chemin a suivre pour l'abeille
            Pour ce tuple (True,(9,15))
            Le true est que le deplacement automatique est activé, 9 pour le déplacement x en soit l'objectif est en abeille.x + 9
            et la même chose pour le 15 
    :rtype: tuple[bool, tuple[int, int]]
    """
    tuple_clic = lib_graphisme.clic_formate(clic)
    x = tuple_clic[0]
    y = tuple_clic[1]
    output = (False,(0,0))
    print(f"auto1 | {x} | {y} | {abeille_j.x_old} | {abeille_j.y_old}")
    if 0 <= x < config.nb_carre_x and 0 <= y < config.nb_carre_y and (map[x][y] == 0 or 10 < map[x][y] <= 10+config.max_nectar or map[x][y]==abeille_j.equipe): # 
        if x > abeille_j.x_old:
            xauto = abs(abeille_j.x_old-x)
        else:
            xauto = (abeille_j.x_old-x)*-1
        if y > abeille_j.y_old:
            yauto = abs(abeille_j.y_old-y)
        else:
            yauto = (abeille_j.y_old-y)*-1
        output = (True,(xauto,yauto))
        if 0<=abeille_j.x_old+xauto<config.nb_carre_x and 0<=abeille_j.y_old+yauto<config.nb_carre_y:
            print("conforme")
        else:
            print(f"FATAL : y_old:{abeille_j.y_old} |x_old: {abeille_j.x_old} | yauto:{yauto} | xauto : {xauto}")
            print(f"FATAL info : destination : x:{x}, y:{y}")
        print(f"log : y_old:{abeille_j.y_old} |x_old: {abeille_j.x_old} | yauto:{yauto} | xauto : {xauto}")
        print(f"log info : destination : x:{x}, y:{y}")
        print(output)
    return output
#-----------------------------------------------------------------------------------MAIN-----------------------------------------------------------------------------------#

map = creation_matrice_map()
affichage_matrice(map)
if __name__ == "__main__": # Lance le jeu quand lancé seul 
    import lib_graphisme
    lib_graphisme.menu()

