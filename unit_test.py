import config
import backend
import lib_graphisme

def test_map()->bool:
    """
    Doctring for test_map

    Test unitaire pour la fonction creation matrice map de backend.py
    """
    test1 = False
    test2 = False
    test3 = False
    map_base = backend.creation_matrice_map(True) # Retourne la matrice Vide sans les fleur
    
    map_voulu = [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
                [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
                [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4],
                [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4]]
    if not map_base == map_voulu: # test 1 : Est-ce que la map se génère correctement sans les fleurs
        assert("La map n'est pas celle voulu défini dans le test unitaire de map, le test unitaire a échoué")
    else:
        print(f"Le test Unitaire 1 de la map à été reussi")
        test1 = True
    # test 2 
    map_fleur = backend.creation_matrice_map()
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count_fleur = 0
    for x in range(len(map_fleur)):
        for y in range(len(map_fleur[x])):
            if map_fleur[x][y] == 1: 
                count1 += 1
            elif map_fleur[x][y] == 2:
                count2 += 1
            elif map_fleur[x][y] == 3:
                count3 += 1
            elif map_fleur[x][y] == 4:
                count4 += 1
            elif 10 <= map_fleur[x][y] <= config.max_nectar:
                count_fleur += 1
    if not ((count1 == config.nb_carre) and (count2 == config.nb_carre) and (count3 == config.nb_carre) and (count4 == config.nb_carre)):
        assert("Les élément de map ne sont pas conforme | Les spawn d'équipe ne sont pas de la bonne taille")
    else:
        print("Le test Unitaire de la map 2  à été reussi")
        test2 = True
    if not (count_fleur == config.nb_fleur*4):
        assert(" Le nombre de fleur généré par la map est incorrecte")
    else:
        print("Le test unitaire de la map 3 à été reussi")
        test3 = True
    return test1 and test2 and test3


def test_yaquelqun()->bool:
    """
    Docstring for test_yaquelqun

    Test la fonction Ya quelqu'un
    -> Creation d'un joueur test et verication si la fonction peut le detecté
    
    :return: Description
    :rtype: bool
    """
    test1 = False
    Joueur_test = backend.joueur([backend.abeille(config.nb_carre//2,config.nb_carre//2,1,'eclaireuse')])
    lib_graphisme.Players.append(Joueur_test)
    if backend.ya_quelqun(config.nb_carre//2,config.nb_carre//2):
        test1 = True
        print(f"Le test unitaire de la fonction ya quelqu'un à été reussi")
    else:
        assert("La Test Unitaire de la fonction ya quelqu'un à échoué a reconnaitre le joueur test")
    
    return test1


def test_case_valide()->bool:
    """
    Docstring for test_case_valide

    Test Unitaire de la fonction case_valide()

    -> Test si la fonction peut se déplace sur un case neutre ou fleur
    -> Test si la fonction peut se deplacer sur un case de son spawn 
    -> Test si la fonction bloque les déplacement sur un spawn énnemis
    -> Test si la fonction bloque les déplacement quand l'abeille est ko
    
    :return: Description
    :rtype: bool
    """
    test1 = False
    test2 = False
    test3 = False
    test4 = False
    test5 = False
    # test 1 : deplacement sur un case neutre
    # utilsation de l'abeille 0 du joueur 1 | on configure la position de l'abeille au préalabre
    lib_graphisme.Players[1].list_abeille[0].x = config.nb_carre//2
    lib_graphisme.Players[1].list_abeille[0].y = config.nb_carre//2
    lib_graphisme.Players[1].list_abeille[0].x_old = (config.nb_carre//2)-1
    lib_graphisme.Players[1].list_abeille[0].y_old = config.nb_carre//2
    if backend.case_valide(lib_graphisme.Players[1].list_abeille[0]):
        test1 = True
        print("Le test unitaire 1 de case valide à été reussi")
    else:
        print("Le test unitaire 1 de case valide à échoué")
    # test 2 : Déplacement sur un case du spawn du joueur
    # utilsation de l'abeille 0 du joueur 1 | on configure la position de l'abeille au préalabre
    lib_graphisme.Players[1].list_abeille[0].x = 1
    lib_graphisme.Players[1].list_abeille[0].y = 1
    lib_graphisme.Players[1].list_abeille[0].x_old = 0
    lib_graphisme.Players[1].list_abeille[0].y_old = 1
    lib_graphisme.Players[1].list_abeille[0].equipe = 1
    if backend.case_valide(lib_graphisme.Players[1].list_abeille[0]):
        test2 = True
        print("Le test unitaire 2 de case valide à été reussi")
    else:
        print("Le test unitaire 2 de case valide à échoué")
    # test 3 : Déplacement sur un case du spawn ennemie | Même test que précedent en changeant l'équipe du joueur
    # Le déplacement doit étre impossible 
    # utilsation de l'abeille 0 du joueur 1 | on configure la position de l'abeille au préalabre
    lib_graphisme.Players[1].list_abeille[0].x = 1
    lib_graphisme.Players[1].list_abeille[0].y = 1
    lib_graphisme.Players[1].list_abeille[0].x_old = 0
    lib_graphisme.Players[1].list_abeille[0].y_old = 1
    lib_graphisme.Players[1].list_abeille[0].equipe = 4
    if not backend.case_valide(lib_graphisme.Players[1].list_abeille[0]):
        test3 = True
        print("Le test unitaire 3 de case valide à été reussi")
    else:
        print("Le test unitaire 3 de case valide à échoué")
    # test 4 : Déplacement sur un case pendant que l'abeille soit KO
    # Le déplacement doit étre impossible | Test 1 en étant ko
    # utilsation de l'abeille 0 du joueur 1 | on configure la position de l'abeille au préalabre
    lib_graphisme.Players[1].list_abeille[0].etat = False
    lib_graphisme.Players[1].list_abeille[0].x = config.nb_carre//2
    lib_graphisme.Players[1].list_abeille[0].y = config.nb_carre//2
    lib_graphisme.Players[1].list_abeille[0].x_old = (config.nb_carre//2)-1
    lib_graphisme.Players[1].list_abeille[0].y_old = config.nb_carre//2
    if not backend.case_valide(lib_graphisme.Players[1].list_abeille[0]):
        test4 = True
        print("Le test unitaire 4 de case valide à été reussi")
    else:
        print("Le test unitaire 4 de case valide à échoué")
    return test1 and test2 and test3 and test4
#test_map()
#test_yaquelqun()
test_case_valide()


    

