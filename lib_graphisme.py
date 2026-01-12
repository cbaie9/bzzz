import tkiteasy as tke # type: ignore
import config
import backend

    # pour les warning, la fonction appelle ne renvoie en que des int dans les mode 1 et 2 -> voir definition fonction 
J1 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(1,1)),int(backend.get_spawn_coor(1,2)),1,'eclaireuse')]) # pyright: ignore[reportArgumentType]
J2 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(2,1)),int(backend.get_spawn_coor(2,2)),2,'eclaireuse')]) # pyright: ignore[reportArgumentType]
J3 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(3,1)),int(backend.get_spawn_coor(3,2)),3,'eclaireuse')]) # pyright: ignore[reportArgumentType]
J4 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(4,1)),int(backend.get_spawn_coor(4,2)),4,'eclaireuse')]) # pyright: ignore[reportArgumentType]
global Players
Players = [J1,J2]


def dessiner_background(): #quadriage selon la couleur des spawn via la matrice map
    """
    Dessine l'arrière plan du jeu en fonction des constant de base
    """
    compteur = 0
    for x in range(0,config.xmax_game,config.taille_carre_x):
        
        for y in range(0,config.ymax_game,config.taille_carre_y):
            if compteur == 1:
                color = get_couleur_map(x//config.taille_carre_x,y//config.taille_carre_y)
                compteur =0
            else:
                color = get_couleur_map(x//config.taille_carre_x,y//config.taille_carre_y)
                compteur += 1
            g.dessinerRectangle(x,y,config.taille_carre_x,config.taille_carre_y,color)
        if x/config.taille_carre_x % 2 == 0:
            compteur = 1
        else: 
            compteur = 0

def start():
    """
    Docstring for start

    Code 'boucle' principal du jeu
    """
    # ----- Initailisation de la fenêtre + abeille
    global g
    g = tke.ouvrirFenetre(config.xmax, config.ymax_game)
    actualisation_background_map()
    if len(Players) == 1:
        liste_img_p1 = [g.afficherImage(Players[0].list_abeille[0].x*config.taille_carre_x,Players[0].list_abeille[0].y*config.taille_carre_x,get_image_sprite(1,"ouvrière"))]
        List_img :list[list[tke.ObjetGraphique]] = [liste_img_p1] 
    elif len(Players) == 2 : 
        liste_img_p1 = [g.afficherImage(Players[0].list_abeille[0].x*config.taille_carre_x,Players[0].list_abeille[0].y*config.taille_carre_x,get_image_sprite(1,"ouvrière"))]
        liste_img_p2 = [g.afficherImage(Players[1].list_abeille[0].x*config.taille_carre_x,Players[1].list_abeille[0].y*config.taille_carre_x,get_image_sprite(2,"ouvrière"))]
        List_img :list[list[tke.ObjetGraphique]] = [liste_img_p1,liste_img_p2] 
    else : 
        liste_img_p1 = [g.afficherImage(Players[0].list_abeille[0].x*config.taille_carre_x,Players[0].list_abeille[0].y*config.taille_carre_x,get_image_sprite(1,"ouvrière"))]
        liste_img_p2 = [g.afficherImage(Players[1].list_abeille[0].x*config.taille_carre_x,Players[1].list_abeille[0].y*config.taille_carre_x,get_image_sprite(2,"ouvrière"))]
        liste_img_p3 = [g.afficherImage(Players[2].list_abeille[0].x*config.taille_carre_x,Players[2].list_abeille[0].y*config.taille_carre_x,get_image_sprite(3,"ouvrière"))]
        liste_img_p4 = [g.afficherImage(Players[3].list_abeille[0].x*config.taille_carre_x,Players[3].list_abeille[0].y*config.taille_carre_x,get_image_sprite(4,"ouvrière"))]
        List_img :list[list[tke.ObjetGraphique]] = [liste_img_p1,liste_img_p2,liste_img_p3,liste_img_p4] 
     
    #-------------------Boucle principale
    while config.play:
        for joueur in Players:
            # Gestion du tour multi-abeilles
            abeilles_restantes = [i for i in range(len(joueur.list_abeille))] #création de la liste qui contient toutes les abeilles du joueur actuel sous forme [0,1,2] qui correspondent aux indices des abeilles
            for xlr in range(len(joueur.list_abeille)):
                auto_dep = joueur.list_abeille[xlr].autodep
                revert = False
                if joueur.list_abeille[xlr].etat == False:
                    abeilles_restantes.remove(xlr) # enlevement des abeille ko de la liste d'abeille restant
                elif auto_dep[0] == True and config.extra_auto_dep:
                    x_dep = 0
                    y_dep = 0
                    depla = False #deplacement est-il déjà effectué
                    extrac = auto_dep[1]
                    print(extrac)
                    if extrac[0] >= 0: # obtention du signe chemin calculé
                        signex = 1
                    else:
                        signex = -1
                    if extrac[1] >= 0:
                        signey = 1
                    else:
                        signey = -1
                    # autodeplacement du tour | on touche a une donnée abeille donc non optimisable dans un fonction
                    if not extrac[0] == 0:
                            x_dep = 1*signex
                            depla = True
                    if (not extrac[1] == 0) and ((not depla) or joueur.list_abeille[xlr].classe == "eclaireuse"):
                        # deplacement en diagonal 
                        y_dep = 1*signey
                    joueur.list_abeille[xlr].x = joueur.list_abeille[xlr].x_old +x_dep
                    joueur.list_abeille[xlr].y = joueur.list_abeille[xlr].y_old +y_dep
                    print(f"autodep3 | {x_dep} | {y_dep} | {joueur.list_abeille[xlr].x_old}+{x_dep} = {joueur.list_abeille[xlr].x}")
                    if not backend.case_valide(joueur.list_abeille[xlr]):
                        revert = True
                        print(f"autodep4.1 | {joueur.list_abeille[xlr].autodep} | {(True,(extrac[0],extrac[1]))}")
                        joueur.list_abeille[xlr].y = joueur.list_abeille[xlr].y_old
                        joueur.list_abeille[xlr].x = joueur.list_abeille[xlr].x_old
                    else:
                        joueur.list_abeille[xlr].autodep = (True,(extrac[0]+x_dep,extrac[1]+y_dep))
                        joueur.list_abeille[xlr].x_old = joueur.list_abeille[xlr].x
                        joueur.list_abeille[xlr].y_old = joueur.list_abeille[xlr].y
                        print(f"autodep4.2 | {joueur.list_abeille[xlr].autodep} | {(True,(extrac[0],extrac[1]))}")
                        abeilles_restantes.remove(xlr) # envlement due au fait que l'abeille a bougé en automatique
                    if extrac[1] == 0 and  extrac[0] == 0:
                        joueur.list_abeille[xlr].autodep = (False,(0,0))
                print("###### \n Fin dump auto dep \n #####")
            while len(abeilles_restantes) > 0 and config.play: #tant qu'il y a des abeilles dans la liste / tant que le bouton stop croix rouge n'est pas cliqué
                afficher_toutes_les_abeilles(List_img)
                stat_part(joueur) # actulisation des statistique pour le joueur actuelle
                # ---------------------- #
                # Selection de l'abeille
                print("#########\n Selection de l'abeille a jouer \n ########## ")
                selection = True
                abeille_selectionnee = 0 # Initialisation de l'abeille selectionne si pbm
                while selection:
                    clic = g.attendreClic()
                    clic_custom = backend.clic_custom(clic.x,clic.y) # classe clic custom pour éviter les problème de typpage, aucun changement fonctionnelle
                    retour_btn = bouton_stat(clic_custom,joueur)
                    if config.play == False: # pyright: ignore[reportUnnecessaryComparison] -> faux car bouton_stat()
                        break
                    elif 1 <= retour_btn  <= 3:
                        classe_str = ['ouvrière','bourdon','eclaireuse']
                        joueur.list_abeille.append(backend.creation_abeille(joueur,classe_str[retour_btn-1])) # type: ignore 
                        joueur.nectar -= config.cout_ponte
                        texture_ab = get_image_sprite(joueur.id+1,classe_str[retour_btn-1])
                        List_img[joueur.id].append(g.afficherImage(Players[joueur.id].list_abeille[len(joueur.list_abeille)-1].x*config.taille_carre_x,Players[joueur.id].list_abeille[len(joueur.list_abeille)-1].y*config.taille_carre_x,texture_ab))
                        afficher_toutes_les_abeilles(List_img)
                        print(len(List_img[joueur.id]))
                        abeilles_restantes.append(len(joueur.list_abeille)-1) #on rajoute l'indice de l'abeille à la liste par ex [0,1,2,3] + [4] car la nouvelle abeille est la cinquième
                    elif retour_btn == 4:
                        abeilles_restantes = []
                        print("skip le tour")
                        break
                    # si le temps ajouter ici le système de déplacement automatique / IA
                    x_clic_formate,y_clic_formate = clic_formate(clic_custom) # formatage du clic /case
                    for i in abeilles_restantes: #on parcourt tout les "id" des abeilles
                        if joueur.list_abeille[i].x == x_clic_formate and joueur.list_abeille[i].y == y_clic_formate and joueur.list_abeille[i].etat: #si l'abeille se trouve sur la case sur laquelle on vient de cliquer
                            abeille_selectionnee = i #l'abeille sélectionnée est l'indice par ex si on sélectionne l'abeille 0 alors cette variable = 0                             selection = False
                            selection = False #on a finit la sélection on peut passer au reste
                            break
                if config.play == False or len(abeilles_restantes)==0: # pyright: ignore[reportUnnecessaryComparison] -> faux car bouton_stat()
                        print("break len2")
                        break # sortie de la boucle prématurée car le bouton de fermeture à été appuiyée
                print(f"########### \n fin selection : \n abeille selectionne :{abeille_selectionnee} | x: {joueur.list_abeille[abeille_selectionnee].x} | y: {joueur.list_abeille[abeille_selectionnee].y} \n ########")
                #          ICI
                # ---------------------- # 
                stat_part(joueur,abeille_selectionnee)
                dessiner_case_deplacement(joueur.list_abeille[abeille_selectionnee])  # affichage des déplacement possible par le joueur
                afficher_toutes_les_abeilles(List_img)
                clic = g.attendreClic()
                clic_custom = backend.clic_custom(clic.x,clic.y) # classe clic custom pour éviter les problème de typpage, aucun changement fonctionnelle
                dessiner_case_deplacement(joueur.list_abeille[abeille_selectionnee],False) # faux -> efface les cases de prévisualisation 
                actualisation_background_map() 
                # --------------- Determination du clic du joueur ( par cases )
                # calcul des collision
                joueur.list_abeille[abeille_selectionnee].x_old = joueur.list_abeille[abeille_selectionnee].x #on actualise les coordonnées de l'abeille
                joueur.list_abeille[abeille_selectionnee].y_old = joueur.list_abeille[abeille_selectionnee].y # idem
                joueur.list_abeille[abeille_selectionnee].x, joueur.list_abeille[abeille_selectionnee].y = clic_formate(clic_custom) # changement -> mtn dans fonction dédié pour éviter la répétition
                print(f"########### \n fin déplacement : \n abeille selectionne :{abeille_selectionnee} | x: {joueur.list_abeille[abeille_selectionnee].x} | y: {joueur.list_abeille[abeille_selectionnee].y} \n ########")
                #---------
                # est-ce que la case choisi est la valide
                #debug position# print(joueur.list_abeille[abeille_selectionnee].x,joueur.list_abeille[abeille_selectionnee].y)
                if backend.case_valide(joueur.list_abeille[abeille_selectionnee]):
                    if backend.est_Butinable(joueur.list_abeille[abeille_selectionnee].x,joueur.list_abeille[abeille_selectionnee].y): # [MODIF]
                        nectar_add = backend.Butinage(joueur.list_abeille[abeille_selectionnee],joueur.list_abeille[abeille_selectionnee].x,joueur.list_abeille[abeille_selectionnee].y) # [MODIF]
                        if nectar_add > 0:
                            joueur.list_abeille[abeille_selectionnee].nectar += nectar_add #l'abeille sélectionnée reçoit le nectar
                            stat_part(joueur)
                    else :
                        deplacement_joueur(joueur,abeille_selectionnee,List_img)
                    
                    abeilles_restantes.remove(abeille_selectionnee) #on retire l'abeille qui vient d'être faite 
                else :
                    # colision btn stat
                    retour_btn = bouton_stat(clic_custom,joueur) # deplacer dans fonction dédié | clic custom = classe pour éviter les pbm de typpage
                    
                    if config.extra_auto_dep:
                        # deplacement automatique si on ne clique sur une case qui n'est pas automatiquement valide
                        print("######### \n Debut dump auto deplacement \n #####")
                        tuple_auto_dep = backend.auto_deplacement_list(joueur.list_abeille[abeille_selectionnee],clic_custom) # Préparation  et calcul du trajet autodeplacement
                        revert = False
                        if tuple_auto_dep[0]:
                            x_dep = 0
                            y_dep = 0
                            depla = False #deplacement est-il déjà effectué
                            joueur.list_abeille[abeille_selectionnee].autodep = tuple_auto_dep
                            extrac = tuple_auto_dep[1]
                            print(extrac)
                            if extrac[0] >= 0: # obtention du signe chemin calculé
                                signex = 1
                            else:
                                signex = -1
                            if extrac[1] >= 0:
                                signey = 1
                            else:
                                signey = -1
                            # autodeplacement du tour | on touche a une donnée abeille donc non optimisable dans un fonction
                            if not extrac[0] == 0:
                                x_dep = 1*signex
                                depla = True
                            if (not joueur.list_abeille[abeille_selectionnee].autodep[1][1] == 0) and ((not depla) or joueur.list_abeille[abeille_selectionnee].classe == "eclaireuse"):
                                # deplacement en diagonal 
                                y_dep = 1*signey
                            joueur.list_abeille[abeille_selectionnee].x = joueur.list_abeille[abeille_selectionnee].x_old +x_dep
                            joueur.list_abeille[abeille_selectionnee].y = joueur.list_abeille[abeille_selectionnee].y_old +y_dep
                            print(f"autodep3 | {x_dep} | {y_dep} | {joueur.list_abeille[abeille_selectionnee].x_old}+{x_dep} = {joueur.list_abeille[abeille_selectionnee].x}")
                            if not backend.case_valide(joueur.list_abeille[abeille_selectionnee]):
                                revert = True
                                print(f"autodep4.1 | {joueur.list_abeille[abeille_selectionnee].autodep} | {(True,(extrac[0],extrac[1]))}")
                            else:
                                joueur.list_abeille[abeille_selectionnee].autodep = (True,(extrac[0]+x_dep,extrac[1]+y_dep))
                                joueur.list_abeille[abeille_selectionnee].x_old = joueur.list_abeille[abeille_selectionnee].x
                                joueur.list_abeille[abeille_selectionnee].y_old = joueur.list_abeille[abeille_selectionnee].y
                                print(f"autodep4.2 | {joueur.list_abeille[abeille_selectionnee].autodep} | {(True,(extrac[0],extrac[1]))}")
                                abeilles_restantes.remove(abeille_selectionnee) # envlement due au fait que l'abeille a bougé en automatique
                            if extrac[1] == 0 and  extrac[0] == 0:
                                joueur.list_abeille[abeille_selectionnee].autodep = (False,(0,0))
                        if not tuple_auto_dep[0] or revert:
                            print(f"autodep4.1.1")
                            joueur.list_abeille[abeille_selectionnee].y = joueur.list_abeille[abeille_selectionnee].y_old
                            joueur.list_abeille[abeille_selectionnee].x = joueur.list_abeille[abeille_selectionnee].x_old
                        
                        print("###### \n Fin dump auto dep \n #####")
                    else:
                        joueur.list_abeille[abeille_selectionnee].y = joueur.list_abeille[abeille_selectionnee].y_old
                        joueur.list_abeille[abeille_selectionnee].x = joueur.list_abeille[abeille_selectionnee].x_old
                    actualisation_background_map() 
                    afficher_abeille(joueur.list_abeille[abeille_selectionnee],List_img[joueur.id][abeille_selectionnee])
                    if config.play == False or len(abeilles_restantes)==0:  # pyright: ignore[reportUnnecessaryComparison] -> Warning faux due à la foncion bouton_stat
                        break

                    # INFO DEV : les retour de backend.creation_abeille ne sont pas None car verification de bouton_stat
                    #
                    #
                    elif 1 <= retour_btn  <= 3:
                        # creation des abeille quand selection déjà effectué | Je sais que le code est déjà au dessus mais non optimisable ( dans un fonction) sinon les donnée ne sont pas sauvegardées dans la fonction
                        classe_str = ['ouvrière','bourdon','eclaireuse']
                        joueur.list_abeille.append(backend.creation_abeille(joueur,classe_str[retour_btn-1])) # type: ignore 
                        joueur.nectar -= config.cout_ponte
                        texture_ab = get_image_sprite(joueur.id+1,classe_str[retour_btn-1])
                        List_img[joueur.id].append(g.afficherImage(Players[joueur.id].list_abeille[len(joueur.list_abeille)-1].x*config.taille_carre_x,Players[joueur.id].list_abeille[len(joueur.list_abeille)-1].y*config.taille_carre_x,texture_ab))
                        afficher_toutes_les_abeilles(List_img)
                        print(len(List_img[joueur.id]))
                        abeilles_restantes.append(len(joueur.list_abeille)-1)#on rajoute l'indice de l'abeille à la liste par ex [0,1,2,3] + [4] car la nouvelle abeille est la cinquième
                    elif retour_btn == 4:
                        abeilles_restantes.clear()
                    # si le temps ajouter ici le système de déplacement automatique / IA
            # verif de fin de tour
            backend.update_abeille()
            list_ko = backend.escarmouche()
            for xlist_escar in range(len(list_ko)): # extraction des données de la fonction
                tuple_ko :tuple[int,int] = list_ko[xlist_escar] # puis mise ko des abeille concernée
                Players[tuple_ko[0]].list_abeille[tuple_ko[1]].compteur_KO = config.Time_KO
                Players[tuple_ko[0]].list_abeille[tuple_ko[1]].etat = False
                if tuple_ko[1] in abeilles_restantes:
                    abeilles_restantes.remove(tuple_ko[1]) # fix qu'un abeille KO ne peut pas jouer
            fin_de_tour(joueur)
            # info non je peut pas bouger ça dans une fonction ça marche pas dans l'architecture du code
            for x in range(len(Players)): # for pour le nombre de joueur
                liste_joueur_actuelle :list[backend.abeille] = Players[x].list_abeille # liste d'abeille pour le joueur actuelle
                for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
                    if not liste_joueur_actuelle[y].etat:
                        print(f"{x},{y} false")
                        texture = get_image_sprite(liste_joueur_actuelle[y].equipe,liste_joueur_actuelle[y].classe,liste_joueur_actuelle[y].etat)
                        objgrap = g.afficherImage(liste_joueur_actuelle[y].x*config.taille_carre_x,liste_joueur_actuelle[y].y*config.taille_carre_x,texture)
                        if not objgrap == List_img[x][y]:
                            List_img[x][y] = objgrap # met à jour l'image de toute les abeille 

    # Fermeture fenêtre
    g.fermerFenetre()


def get_couleur_map(x:int,y:int)->str:
    """
    Docstring for get_couleur_map
    
    :param x: Coordonnée x de la position sur la map
    :type x: int
    :param y: Coordonnée y de la position sur la map
    :type y: int
    :return: Retourne un couleur en str
    :rtype: str
    """
    # determine si la case demandé est dans la map
    if not (0 <= x < config.nb_carre_x and 0 <= y < config.nb_carre_y):
        print(f"erreur de oob x ={x}, y : {y}")
        print(f"{config.taille_carre_x},   {config.taille_carre_y}")
        return config.map_error_color
    # determine la couleur du damier
    if (x % 2 == 0 and y % 2 == 0) or (x%2 == 1 and y % 2 == 1) :
        black = False
    else :
        black = True
    if backend.map[x][y] == 0:
        if black:
            output = config.map_default_color_black
        else :
            output = config.map_default_color_white
    elif backend.map[x][y] == 1:
        if black:
            output = config.spawn_equipe_1bk
        else :
            output = config.spawn_equipe_1wh
    elif backend.map[x][y] == 2:
        if black:
            output = config.spawn_equipe_2bk
        else :
            output = config.spawn_equipe_2wh
    elif backend.map[x][y] == 3:
        if black:
            output = config.spawn_equipe_3bk
        else:
            output = config.spawn_equipe_3wh
    elif backend.map[x][y] == 4:
        if black:
            output = config.spawn_equipe_4bk
        else:
            output = config.spawn_equipe_4wh
    elif 10 <= backend.map[x][y] <= 100:
        output = config.map_flower_color
    else:
        output = config.map_error_color
    return output
def dessiner_spawn():
    """
    Docstring for dessiner_spawn

    Affiche les maison 'spawn' à l'écran
    """
    g.afficherImage(config.xmax_game-config.taille_image_spawn,config.ymax_game-config.taille_image_spawn,"./image/spawn/red.png")
    g.afficherImage(0,config.ymax_game-config.taille_image_spawn,"./image/spawn/blue.png")
    g.afficherImage(0,0,"./image/spawn/green.png")
    g.afficherImage(config.xmax_game-config.taille_image_spawn,0,"./image/spawn/violet.png")
# <---------------------------------- >
def menu(): # Menu du jeu
    """
    Docstring for menu

    Code 'principal' pour le menu du jeu, calcul les colision de l'abeille avec les mur et son apparition au niveau du clic et le bouton pour lancer le jeu
    """
    global g 
    menu_background()
    carre = g.afficherImage(config.taille_mini/2,config.taille_mini/2,'./image/abeille_menu.png')  # initialisation de l'abeille du menu "carre"
    vx,vy = backend.velo_menu() # direction aléatoire
    while True: # boucle infini pour l'interface menu
            g.deplacer(carre,vx,vy)
            g.pause(0.05)

            clic = g.recupererClic()
            if clic is not None: 
                # boutons
                    ### colision du bouton jouer
                if ((config.taille_mini/2)-(config.taille_mini/4)) <= clic.x <= ((config.taille_mini/2)-(config.taille_mini/4))+config.taille_mini/2 : # collsion x bouton jouer
                    if ((config.taille_mini)-((config.taille_mini/8))-(config.taille_mini/16)) <= clic.y <= ((config.taille_mini)-((config.taille_mini/8))-(config.taille_mini/16))+config.taille_mini/8:
                        break
                ### action réaliser quand on fait un clic
                vx,vy = backend.velo_menu() # direction aléatoire
                g.supprimer(carre) # suppresion de l'ancien carre
                # calcul d'une marge de sécurité pour éviter un rebond infini 
                if clic.x > config.taille_mini/2:
                    marge_mini_x = config.taille_texture_abeille
                else:
                    marge_mini_x = 0
                if clic.y > config.taille_mini/2:
                    marge_mini_y = config.taille_texture_abeille
                else:
                    marge_mini_y = 0
                # calcul des coordonnées où sera posé l'image
                x = (clic.x)-marge_mini_x
                y = (clic.y)-marge_mini_y
                carre = g.afficherImage(x,y,'./image/abeille_menu.png')
                #### fin
            if carre.x <= 0 or carre.x+50 > config.taille_mini : # colision avec les mur de l'interface ( gauche + droite)
                vx *= -1
                if vx > 50:  # Sécurité pour que la vitesse n'aille pas trop haute
                    vx = 50
            elif carre.y <= 0 or carre.y+50 >= config.taille_mini : # colision avec les mur de l'interface ( haut + bas)
                vy *= -1
                if vy > 50 :
                    vy = 50
            elif carre.x <= -5 or carre.x+50 > config.taille_mini+5 or carre.y <= -5 or carre.y+50 >= config.taille_mini+5 :
                g.supprimer(carre)
                carre = g.afficherImage(config.taille_mini/2,config.taille_mini/2,'./image/abeille_menu.png')

    # Fermeture fenêtre et lancement du jeu
    g.fermerFenetre()
    start()
def menu_background():
    """
    Docstring for menu_background

    Affiche le menu quand on lance le jeu ( arrière plan )
    """
    global g
    g = tke.ouvrirFenetre(config.taille_mini, config.taille_mini)
    g.afficherImage(0,0,'./image/background_menu.png')
    # titre
    g.dessinerRectangle((config.taille_mini/2)-(config.taille_mini/4),(config.taille_mini/8)-(config.taille_mini/16),config.taille_mini/2,config.taille_mini/8,'yellow')
    g.afficherTexte("BZZZ",config.taille_mini/2,config.taille_mini/8,'red')
    # btn jouer
    g.dessinerRectangle((config.taille_mini/2)-(config.taille_mini/4),(config.taille_mini)-((config.taille_mini/8))-(config.taille_mini/16),config.taille_mini/2,config.taille_mini/8,'black')
    g.afficherTexte("Jouer",config.taille_mini/2,config.taille_mini-config.taille_mini/8,'white')

def stat_part(joueur:backend.joueur,select:int=-1):
    """
    Docstring for stat_part

    Actualise la partie "statistique" de l'écran en fonction du tour du joueur qui est en cours
    
    :param joueur: Description
    :type joueur: backend.joueur
    """
    global g
    slnum = 0
    if not select == -1:
         slnum :int = select
    print(slnum)
    g.dessinerRectangle(config.xmax_game,0,config.xmax_stat,config.ymax_game,'gray')
    for x in range(0,4):
        color = ['green','purple','blue','red']
        y = x+1
        #j3
        if joueur.id == x:
            #print(x,y)
            g.afficherTexte(f'J{y}',config.xmax_game+20,((config.ymax_game//8)*y)-30,color[x],20)
            g.afficherTexte(f'Nectar abeille {slnum} {Players[x].list_abeille[slnum].nectar}',config.xmax_game+config.xmax_stat//4+25,(config.ymax_game//8)*y,color[x],20)
            g.afficherTexte(f'Nectar {Players[x].nectar}',(config.xmax_game+config.xmax_stat)-config.xmax_stat//4,(config.ymax_game//8)*y,color[x],20)
    #btn exit
    g.dessinerRectangle((config.xmax_game+config.xmax_stat)-config.size_btn_quit,0,config.size_btn_quit,config.size_btn_quit,'red')
    g.dessinerLigne(((config.xmax)-config.size_btn_quit)+config.margin_cross,config.margin_cross,config.xmax-config.margin_cross,config.size_btn_quit-config.margin_cross,'white smoke')
    g.dessinerLigne(((config.xmax)-config.size_btn_quit)+config.margin_cross,config.size_btn_quit-config.margin_cross,config.xmax-config.margin_cross,config.margin_cross,'white smoke')
    # btn créer abeille :
    g.dessinerLigne(config.xmax_game,(config.ymax_game//8)*5-config.sub_margin_btn-20,config.xmax,(config.ymax_game//8)*5-config.sub_margin_btn-20,'black')
    g.afficherTexte(f'Créer des abeilles | coût : {config.cout_ponte}',config.xmax_game+config.xmax_stat//2,(config.ymax_game//8)*5-config.sub_margin_btn,'black',20)
    for x in range(0,3):
        Nom = ['Ouvrière','Bourdon','Eclaireuse']
        if joueur.nectar >= 3 and not backend.ya_quelqun(backend.get_spawn_coor(joueur.id+1,1),backend.get_spawn_coor(joueur.id+1,2)): # pyright: ignore[reportArgumentType] -> voir definition fonction mode 1 et 2 ne renvoie que des int et non des tuple
            color_creer :str = 'dark green'
        else:
            color_creer :str = 'red'
        g.afficherTexte(f'{Nom[x]}',config.xmax_game+config.xmax_stat//4,(config.ymax_game//8)*(5+x*0.5)+config.sub_margin_btn,'orange',20)
        g.dessinerRectangle(config.xmax_game+config.xmax_stat//2,(config.ymax_game//8)*(5+x*0.5),config.size_btn_quit*2,config.size_btn_quit,color_creer)
    g.afficherTexte(f'Fin de tour',config.xmax_game+config.xmax_stat//4,(config.ymax_game//8)*(7)+config.sub_margin_btn,'orange',20)
    g.dessinerRectangle(config.xmax_game+config.xmax_stat//2,(config.ymax_game//8)*(7),config.size_btn_quit*4,config.size_btn_quit,'green')




def dessiner_case_deplacement(abeille:backend.abeille, ecrire:bool = True):
    """
    Docstring for dessiner_case_deplacement

    Quand cette fonction est appellée dessine les case où l'abeille defini peut se deplacer,
    
    :param x: Position x ou le joueur a cliquer / veut se déplacer  |
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
    :ecrire: Est-ce que les programme affiche ou supprime les cases | Booléen
    """
    print(abeille.classe)
    if abeille.classe == "eclaireuse":
        mode = 1
    else:
        mode = 2
    liste = backend.get_list_deplacement(abeille.x,abeille.y,mode)
    for x_list,y_list in liste:
            if backend.case_valide(abeille):
                if ecrire:
                    if backend.est_Butinable(x_list,y_list):
                        g.dessinerRectangle(x_list*config.taille_carre_x,y_list*config.taille_carre_y,config.taille_carre_x,config.taille_carre_y,config.map_flower_color)
                    else:
                        g.dessinerRectangle(x_list*config.taille_carre_x,y_list*config.taille_carre_y,config.taille_carre_x,config.taille_carre_y,config.map_player_color)
                else :
                    g.dessinerRectangle(x_list*config.taille_carre_x,y_list*config.taille_carre_y,config.taille_carre_x,config.taille_carre_y,get_couleur_map(x_list,y_list))
                #debug print(f"feur xl :{x_list} ||| yl : {y_list}"))
def actualisation_background_map():
    """
    Docstring for actualisation_background

    Ressiner tout l'arrère plan en appellant les fonction prevue à cet effet
    """
    dessiner_background()
    dessiner_spawn()
def afficher_abeille(abeille:backend.abeille,carre:tke.ObjetGraphique):
    """
    Docstring for afficher_abeille

    Affiche l'abeille demandée à l'écran
    
    :param abeille: Description
    :type abeille: backend.abeille
    :param carre: Description
    :type carre: tke.ObjetGraphique
    """

    g.supprimer(carre)
    if config.nb_carre >= 16:
        carre = g.afficherImage(abeille.x*config.taille_carre_x,abeille.y*config.taille_carre_x,get_image_sprite(abeille.equipe,abeille.classe)) # image de joueur normal
    else :
        carre = g.afficherImage(abeille.x*config.taille_carre_x,abeille.y*config.taille_carre_x,'./image/abeille_menu_mini.png') # image de joueur en mode mini ( prevu pour nb_carre = 8)
    return carre
def fin_de_tour(joueur:backend.joueur):
    """
    Docstring for fin_de_tour

    Verification de fin tour pour toutes les abeille et le retour nectar

    
    """
    
    
    #print("------------------------")
    #backend.affichage_matrice(backend.map)
    # detection de fin de jeu
    # Condition de fin de partie
    #
    # Condition 1 Limite de tous
    config.tour_actuel += 1  # on vient de finir un tour
    if config.tour_actuel >= config.time_out:  # TIME_OUT = 300 dans config.py [file:8]
        print("Fin de partie : TIMEOUT atteint")
        config.play = False  # va faire sortir du while config.play dans lib_graphisme
    # Condition 2 : + de 50% du nectar en sa possesion
    condi_fin2 = nectar_epuise()
    if condi_fin2[0]:
        config.play = False
        print(f"################## \n La partie à un gagnant \n Bravo au joueur {condi_fin2[1]} qui a reussi à récolter plus la moitié du nectar possible \n ###############")
    # ajout du nectar au joueur si l'abeille en porte et se trouve au spawn de son équipe   
    for x in range(len(Players)): # for pour le nombre de joueur
        #print(x)
        liste_joueur_actuelle :list[backend.abeille] = Players[x].list_abeille # liste d'abeille pour le joueur actuelle
        for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            #print(y,backend.map[liste_joueur_actuelle[y].x][liste_joueur_actuelle[y].y])
            if backend.map[liste_joueur_actuelle[y].x][liste_joueur_actuelle[y].y] == x+1: # regarde si la position est égale à l'équipe du joueur si elle appartient (via la matrice et les spawns)
                if liste_joueur_actuelle[y].nectar > 0 : # si l'abeille à du nectar sur elle
                    Players[x].nectar += liste_joueur_actuelle[y].nectar
                    liste_joueur_actuelle[y].nectar = 0
                    print(f"Fin de tour | joueur n°{x+1} | abeille n°{y} | nectar ab = {liste_joueur_actuelle[y].nectar}| nectar joueur {Players[x].nectar}")
    stat_part(joueur)
def afficher_toutes_les_abeilles(liste_img:list[list[tke.ObjetGraphique]]):
    """
    Docstring for afficher_toutes_les_abeilles

    Comme le nom est explicit, affiche tous les abeilles de tous les joueur à l'écran 
    
    :param liste_img: Description
    :type liste_img: list[list[tke.ObjetGraphique]]
    """
    for x in range(len(Players)): # for pour le nombre de joueur
        liste_joueur_actuelle :list[backend.abeille] = Players[x].list_abeille # liste d'abeille pour le joueur actuelle
        for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            g.afficherImage(liste_joueur_actuelle[y].x*config.taille_carre_x,liste_joueur_actuelle[y].y*config.taille_carre_y,get_image_sprite(liste_joueur_actuelle[y].equipe,liste_joueur_actuelle[y].classe))

def get_image_sprite(equipe:int,class_ab:str, etat:bool=True)->str:
    """
    Docstring for get_image_sprite
    Retourne le chemin direct des texture des abeilles de tous type sous forme de 'path'
    
    :param equipe: Description
    :type equipe: int
    :param class_ab: Description
    :type class_ab: str
    :return: Description
    :rtype: str
    """
    output = './image/abeille_menu.png' # par défault si si pbm
    if etat:
        if equipe == 1:
            if class_ab == "ouvrière":
                output = "./image/abeilles/ouvrière/vert.png"
            elif class_ab == "eclaireuse":
                output = "./image/abeilles/eclaireuse/ec_vert.png"
            elif class_ab == "bourdon":
                output = "./image/abeilles/bourdon/bd_vert.png"
        elif equipe == 2:
            if class_ab == "ouvrière":
                output = "./image/abeilles/ouvrière/violet.png"
            elif class_ab == "eclaireuse":
                output = "./image/abeilles/eclaireuse/ec_violet.png"
            elif class_ab == "bourdon":
                output = "./image/abeilles/bourdon/bd_violet.png"
        elif equipe == 3:
            if class_ab == "ouvrière":
                output = "./image/abeilles/ouvrière/bleu.png"
            elif class_ab == "eclaireuse":
                output = "./image/abeilles/eclaireuse/ec_bleu.png"
            elif class_ab == "bourdon":
                output = "./image/abeilles/bourdon/bd_bleu.png"
        elif equipe == 4:
            if class_ab == "ouvrière":
                output = "./image/abeilles/ouvrière/rouge.png"
            elif class_ab == "eclaireuse":
                output = "./image/abeilles/eclaireuse/ec_rouge.png"
            elif class_ab == "bourdon":
                output = "./image/abeilles/bourdon/bd_rouge.png"
    else: # abeille KO
        if class_ab == "ouvrière":
            output = "./image/abeilles/ouvrière/down.png"
        elif class_ab == "eclaireuse":
            output = "./image/abeilles/eclaireuse/ec_down.png"
        elif class_ab == "bourdon":
            output = "./image/abeilles/bourdon/bd_down.png"
        else:
            output = "./image/abeilles/bourdon/bd_down.png"
    return output
def clic_formate(clic:backend.clic_custom):
    """
    Docstring for clic_formate
    Retourne le clic formaté selon le système de case de la matrice
    Par défaut demande le clic si non fournis précédement
    
    :param clic: Description
    :type clic: tk.Event[tk.Canvas]
    """
    if (clic.x - clic.x % config.taille_carre_x)//config.taille_carre_x <= 15: # collision unique pour éviter que le joueur ne puisse pas aller sur la part stat
        x:int = (clic.x - clic.x % config.taille_carre_x)//config.taille_carre_x
    else:
                x = 15 # si le joueur essaie, le colle à la bordure
    y:int = (clic.y - clic.y % config.taille_carre_y)//config.taille_carre_y
    return x,y
def bouton_stat(clic: backend.clic_custom,joueur:backend.joueur)->int:
    """
    Docstring for bouton_stat

    Calcul des colision de bouton de la partie statistique en fonction du clic du joueur  
    
    :param clic: Description
    :type clic: tk.Event[tk.Canvas]
    """
    # partie boutons stat :
    # bouton quitter  
    # INFO DEV :
    #
    #  on calcule les collision à la main sinon on aurait un pbm du clic qui serait forcement dans la zone de jeu 
    #
    if config.xmax-config.size_btn_quit <= clic.x <= config.xmax and 0 <= clic.y <= config.size_btn_quit:
            print("Bye-Bye")
            config.play = False
        # boutons abeille : ouvrière
    elif config.xmax_game+config.xmax_stat//2 <= clic.x <= ((config.xmax_game+config.xmax_stat//2)+2*config.size_btn_quit) and (config.ymax_game//8)*(5) <= clic.y <= ((config.ymax_game//8)*5)+config.size_btn_quit:
        # ajouter créer abeille ici (ouvrière)
        print("abeille : ouvrière")
        if (backend.creation_abeille(joueur,'ouvrière')) is not None:
            return 1
    elif config.xmax_game+config.xmax_stat//2 <= clic.x <= ((config.xmax_game+config.xmax_stat//2)+2*config.size_btn_quit) and (config.ymax_game//8)*5.5 <= clic.y <= ((config.ymax_game//8)*5.5)+config.size_btn_quit:
        # ajouter créer abeille ici ( bourdon )
        print("abeille : bourdon")
        if (backend.creation_abeille(joueur,'bourdon')) is not None:
            return 2
    elif config.xmax_game+config.xmax_stat//2 <= clic.x <= ((config.xmax_game+config.xmax_stat//2)+2*config.size_btn_quit) and (config.ymax_game//8)*6 <= clic.y <= ((config.ymax_game//8)*6)+config.size_btn_quit:
        # ajout créer abeille ici ( eclaireuse )
        print("abeille : eclaireuse")
        if (backend.creation_abeille(joueur,'ouvrière')) is not None:
            return 3
    elif (config.xmax_game+config.xmax_stat//4 <= clic.x <= (config.xmax_game+config.xmax_stat//4)+(config.size_btn_quit*8)) and ((config.ymax_game//8)*(7) <= clic.y <= ((config.ymax_game//8)*(7))+config.size_btn_quit):
        print("Fin de tour")
        return 4
        
    
    return -1
def nectar_epuise()->tuple[bool,int]:
    """
    Docstring for nectar_epuise
    Verfie les condition de fin de jeu

    Si un joueur possède plus de la moitié du nectar en circulation en sa possètion alors il est déclaré vaincure de la partie et la fonction renvoie un tuple vrai avec le numéro du joueur sinon le tuple sera (False,0)


    :return: Description
    :rtype: tuple[bool, int]
    """
    nectar_abeilles = 0
    joueur = 0
    fin = False
    for i in range(len(Players)):    # récuprère tous le nectar contenue sur l'abeille
        for abeille in Players[i].list_abeille:
            nectar_abeilles += abeille.nectar
    nectar_map = 0
    for i in range(config.nb_carre_x): # récuprer tous le nectar contenue dans les fleur 
        for j in range(config.nb_carre_y):
                if (10 <= backend.map[i][j] <= (10 + config.max_nectar) ): 
                    nectar_map += (backend.map[i][j]-10)
    for x in range(len(Players)): # récupere et compare tous le nectar des joueur avec les autres
        if Players[x].nectar > nectar_map+nectar_abeilles:
            joueur = x
            fin = True
            break
    return (fin,joueur)
def deplacement_joueur(joueur:backend.joueur,id_selec:int,list_img:list[list[tke.ObjetGraphique]]):
    """
    Docstring for deplacement_joueur

    Fonction qui lance d'autre fonction qui s'execute lors du deplacement du joueur | optimisation de la fonction principal
    
    :param joueur: Description
    :type joueur: backend.joueur
    :param id_selec: Description
    :type id_selec: int
    :param list_img: Description
    :type list_img: list[list[tke.ObjetGraphique]]
    """
    # deplacement du joueur
    afficher_abeille(joueur.list_abeille[id_selec],list_img[joueur.id][id_selec]) # [MODIF]
    dessiner_spawn()
    afficher_toutes_les_abeilles(list_img)
    
    
### lanecement du jeu ( info -> mettre les fonction avant pls)
if __name__ == "__main__": # Lance le jeu quand lancé seul 
    menu()