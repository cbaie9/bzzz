import tkiteasy as tke # type: ignore
import config
import backend

    # pour les warning, la fonction appelle ne renvoie en que des int dans les mode 1 et 2 -> voir definition fonction 
J1 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(1,1)),int(backend.get_spawn_coor(1,2)),1,'eclaireuse')]) # pyright: ignore[reportArgumentType]
J2 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(2,1)),int(backend.get_spawn_coor(2,2)),2,'eclaireuse')]) # pyright: ignore[reportArgumentType]
J3 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(3,1)),int(backend.get_spawn_coor(3,2)),3,'eclaireuse')]) # pyright: ignore[reportArgumentType]
J4 = backend.joueur([backend.abeille(int(backend.get_spawn_coor(4,1)),int(backend.get_spawn_coor(4,2)),4,'eclaireuse')]) # pyright: ignore[reportArgumentType]
global Players
Players = [J1,J2,J3,J4]


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
    # ----- Initailisation de la fenêtre + abeille
    global g
    g = tke.ouvrirFenetre(config.xmax, config.ymax_game)
    actualisation_background_map()
    liste_img_p1 = [g.afficherImage(Players[0].list_abeille[0].x*config.taille_carre_x,Players[0].list_abeille[0].y*config.taille_carre_x,'./image/abeille_menu.png')]
    liste_img_p2 = [g.afficherImage(Players[1].list_abeille[0].x*config.taille_carre_x,Players[1].list_abeille[0].y*config.taille_carre_x,'./image/abeille_menu.png')]
    liste_img_p3 = [g.afficherImage(Players[2].list_abeille[0].x*config.taille_carre_x,Players[2].list_abeille[0].y*config.taille_carre_x,'./image/abeille_menu.png')]
    liste_img_p4 = [g.afficherImage(Players[3].list_abeille[0].x*config.taille_carre_x,Players[3].list_abeille[0].y*config.taille_carre_x,'./image/abeille_menu.png')]
    List_img :list[list[tke.ObjetGraphique]] = [liste_img_p1,liste_img_p2,liste_img_p3,liste_img_p4] 
    #-------------------Boucle principale
    while config.play:
        for joueur in Players:
            afficher_toutes_les_abeilles(List_img)
            stat_part(joueur)
            dessiner_case_deplacement(joueur.list_abeille[0]) 
            afficher_abeille(joueur.list_abeille[0],List_img[joueur.id][joueur.list_abeille[0].id])
            clic = g.attendreClic()
            dessiner_case_deplacement(joueur.list_abeille[0],False)
            actualisation_background_map()
            
            # previsualisation des déplacement
            #re affichage des abeille du au calque de déplacement
            if clic is not None:
                
                # calcul des collision
                # faux -> efface les cases de prévisualisation 
                # --------------- Determination du clic du joueur ( par cases )
                if (clic.x - clic.x % config.taille_carre_x)//config.taille_carre_x <= 15: # collision unique pour éviter que le joueur ne puisse pas aller sur la part stat
                    joueur.list_abeille[0].x = (clic.x - clic.x % config.taille_carre_x)//config.taille_carre_x
                else:
                    joueur.list_abeille[0].x = 15 # si le joueur essaie, le colle à la bordure
                joueur.list_abeille[0].y = (clic.y - clic.y % config.taille_carre_y)//config.taille_carre_y
                #---------
                # est-ce que la case choisi est la valide
                print(joueur.list_abeille[0].x,joueur.list_abeille[0].y)
                if backend.case_valide(joueur.list_abeille[0]):
                    if backend.est_Butinable(joueur.list_abeille[0].x,joueur.list_abeille[0].y):
                        nectar_add = backend.Butinage(joueur.list_abeille[0],joueur.list_abeille[0].x,joueur.list_abeille[0].y)
                        if nectar_add > 0:
                            joueur.list_abeille[0].nectar += nectar_add
                            stat_part(joueur)
                    else :
                        # deplacement du joueur
                        afficher_abeille(J1.list_abeille[0],List_img[joueur.id][joueur.list_abeille[0].id])
                        dessiner_spawn()
                        joueur.list_abeille[0].y_old = joueur.list_abeille[0].y
                        joueur.list_abeille[0].x_old = joueur.list_abeille[0].x
                        afficher_toutes_les_abeilles(List_img)
                else :
                    # partie boutons stat :
                    # bouton quitter
                    if config.xmax-config.size_btn_quit <= clic.x <= config.xmax and 0 <= clic.y <= config.size_btn_quit:
                        print("Bye-Bye")
                        config.play = False
                    # boutons abeille : ouvrière
                    elif config.xmax_game+config.xmax_stat//2 <= clic.x <= ((config.xmax_game+config.xmax_stat//2)+2*config.size_btn_quit) and (config.ymax_game//8)*5 <= clic.y <= ((config.ymax_game//8)*5)+config.size_btn_quit:
                        # ajouter créer abeille ici (ouvrière)
                        pass
                    elif config.xmax_game+config.xmax_stat//2 <= clic.x <= ((config.xmax_game+config.xmax_stat//2)+2*config.size_btn_quit) and (config.ymax_game//8)*6 <= clic.y <= ((config.ymax_game//8)*6)+config.size_btn_quit:
                        # ajouter créer abeille ici ( bourdon )
                        pass
                    elif config.xmax_game+config.xmax_stat//2 <= clic.x <= ((config.xmax_game+config.xmax_stat//2)+2*config.size_btn_quit) and (config.ymax_game//8)*7 <= clic.y <= ((config.ymax_game//8)*7)+config.size_btn_quit:
                        # ajout créer abeille ici ( eclaireuse )
                        pass
                    # si le temps ajouter ici le système de déplacement automatique / IA
                    # --- ICI --- #
                    # ----------- #
                    joueur.list_abeille[0].y = joueur.list_abeille[0].y_old
                    joueur.list_abeille[0].x = joueur.list_abeille[0].x_old
                    afficher_abeille(joueur.list_abeille[0],List_img[joueur.id][joueur.list_abeille[0].id])
                    if config.play == False:
                        break
                    # si le temps ajouter ici le système de déplacement automatique / IA
                # verif de fin de tour
                fin_de_tour(joueur)
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
        output = config.map_color_flower
    else:
        output = config.map_error_color
    return output
def dessiner_spawn():
    g.afficherImage(config.xmax_game-config.taille_image_spawn,config.ymax_game-config.taille_image_spawn,"./image/spawn/red.png")
    g.afficherImage(0,config.ymax_game-config.taille_image_spawn,"./image/spawn/blue.png")
    g.afficherImage(0,0,"./image/spawn/green.png")
    g.afficherImage(config.xmax_game-config.taille_image_spawn,0,"./image/spawn/violet.png")
# <---------------------------------- >
def menu(): # Menu du jeu
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
    global g
    g = tke.ouvrirFenetre(config.taille_mini, config.taille_mini)
    g.afficherImage(0,0,'./image/background_menu.png')
    # titre
    g.dessinerRectangle((config.taille_mini/2)-(config.taille_mini/4),(config.taille_mini/8)-(config.taille_mini/16),config.taille_mini/2,config.taille_mini/8,'yellow')
    g.afficherTexte("BZZZ",config.taille_mini/2,config.taille_mini/8,'red')
    # btn jouer
    g.dessinerRectangle((config.taille_mini/2)-(config.taille_mini/4),(config.taille_mini)-((config.taille_mini/8))-(config.taille_mini/16),config.taille_mini/2,config.taille_mini/8,'black')
    g.afficherTexte("Jouer",config.taille_mini/2,config.taille_mini-config.taille_mini/8,'white')

def stat_part(joueur:backend.joueur):
    global g
    
    g.dessinerRectangle(config.xmax_game,0,config.xmax_stat,config.ymax_game,'gray')
    for x in range(0,4):
        color = ['green','purple','blue','red']
        y = x+1
        #j3
        if joueur.id == x:
            #print(x,y)
            g.afficherTexte(f'J{y}',config.xmax_game+20,((config.ymax_game//8)*y)-30,color[x],20)
            g.afficherTexte(f'Nectar ab0 {Players[x].list_abeille[0].nectar}',config.xmax_game+config.xmax_stat//4,(config.ymax_game//8)*y,color[x],20)
            g.afficherTexte(f'Nectar {Players[x].nectar}',(config.xmax_game+config.xmax_stat)-config.xmax_stat//4,(config.ymax_game//8)*y,color[x],20)
    #btn exit
    g.dessinerRectangle((config.xmax_game+config.xmax_stat)-config.size_btn_quit,0,config.size_btn_quit,config.size_btn_quit,'red')
    g.dessinerLigne(((config.xmax)-config.size_btn_quit)+config.margin_cross,config.margin_cross,config.xmax-config.margin_cross,config.size_btn_quit-config.margin_cross,'white smoke')
    g.dessinerLigne(((config.xmax)-config.size_btn_quit)+config.margin_cross,config.size_btn_quit-config.margin_cross,config.xmax-config.margin_cross,config.margin_cross,'white smoke')
    # btn créer abeille :
    g.dessinerLigne(config.xmax_game,(config.ymax_game//8)*5-config.sub_margin_btn-20,config.xmax,(config.ymax_game//8)*5-config.sub_margin_btn-20,'black')
    g.afficherTexte(f'Créer des abeilles | coût : {config.prix_abeille}',config.xmax_game+config.xmax_stat//2,(config.ymax_game//8)*5-config.sub_margin_btn,'black',20)
    for x in range(5,8):
        Nom = ['Ouvrière','Bourdon','Eclaireuse']
        if joueur.nectar >= 3 and backend.ya_quelqun(backend.get_spawn_coor(joueur.id+1,1),backend.get_spawn_coor(joueur.id+1,2)): # pyright: ignore[reportArgumentType] -> voir definition fonction mode 1 et 2 ne renvoie que des int et non des tuple
            color_creer :str = 'dark green'
        else:
            color_creer :str = 'red'
        g.afficherTexte(f'{Nom[x-5]}',config.xmax_game+config.xmax_stat//4,(config.ymax_game//8)*x+config.sub_margin_btn,'orange',20)
        g.dessinerRectangle(config.xmax_game+config.xmax_stat//2,(config.ymax_game//8)*x,config.size_btn_quit*2,config.size_btn_quit,color_creer)




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
    liste = backend.get_list_deplacement(abeille.x,abeille.y)
    for x_list,y_list in liste:
            if backend.case_valide(abeille):
                if ecrire:
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
    for x in range(len(Players)): # for pour le nombre de joueur
        liste_joueur_actuelle :list[backend.abeille] = Players[x].list_abeille # liste d'abeille pour le joueur actuelle
        for y in range(len(liste_joueur_actuelle)): # for pour la liste d'abeille / joueur
            g.afficherImage(liste_joueur_actuelle[y].x*config.taille_carre_x,liste_joueur_actuelle[y].y*config.taille_carre_y,get_image_sprite(liste_joueur_actuelle[y].equipe,liste_joueur_actuelle[y].classe))

def get_image_sprite(equipe:int,class_ab:str)->str:
    output = './image/abeille_menu.png'
    if equipe == 1:
        if class_ab == "ouvrière":
            output = "./image/abeilles/ouvrière/vert.png"
        elif class_ab == "eclaireuse":
            output = "./image/abeilles/eclaireuse/ec_vert.png"
        elif class_ab == "bourdon":
            output = "./image/abeilles/bourdon/bd_vert.png"
    elif equipe == 2:
        if class_ab == "ouvrière":
            output = "./image/abeilles/ouvrière/bleu.png"
        elif class_ab == "eclaireuse":
            output = "./image/abeilles/eclaireuse/ec_bleu.png"
        elif class_ab == "bourdon":
            output = "./image/abeilles/bourdon/bd_bleu.png"
    elif equipe == 3:
        if class_ab == "ouvrière":
            output = "./image/abeilles/ouvrière/violet.png"
        elif class_ab == "eclaireuse":
            output = "./image/abeilles/eclaireuse/ec_violet.png"
        elif class_ab == "bourdon":
            output = "./image/abeilles/bourdon/bd_violet.png"
    elif equipe == 4:
        if class_ab == "ouvrière":
            output = "./image/abeilles/ouvrière/rouge.png"
        elif class_ab == "eclaireuse":
            output = "./image/abeilles/eclaireuse/ec_rouge.png"
        elif class_ab == "bourdon":
            output = "./image/abeilles/bourdon/bd_rouge.png"
    return output


### lanecement du jeu ( info -> mettre les fonction avant pls)
if __name__ == "__main__": # Lance le jeu quand lancé seul 
    menu()