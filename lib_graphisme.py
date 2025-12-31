import tkiteasy as tke # type: ignore
import config
import backend


def dessiner_background(): #quadriage selon la couleur des spawn via la matrice map
    """
    Dessine l'arrière plan du jeu en fonction des constant de base
    """
    compteur = 0
    for x in range(0,config.xmax_game,config.taille_carre_x):
        
        for y in range(0,config.ymax_game,config.taille_carre_y):
            g.update()
            if compteur == 1:
                color = get_couleur_map(x//config.taille_carre_x,y//config.taille_carre_y,True)
                compteur =0
            else:
                color = get_couleur_map(x//config.taille_carre_x,y//config.taille_carre_y,False)
                compteur += 1
            g.dessinerRectangle(x,y,config.taille_carre_x,config.taille_carre_y,color)
        if x/config.taille_carre_x % 2 == 0:
            compteur = 1
        else: 
            compteur = 0
        
def start():
    x_old = 0
    y_old = 0
    abeille1 = backend.abeille(0,0,1,0,'eclaireuse',True,config.id_actuelle)
    global g  
    g = tke.ouvrirFenetre(config.xmax, config.ymax_game)
    actualisation_background()
    carre = g.afficherImage(abeille1.x*config.taille_carre_x,abeille1.y*config.taille_carre_x,'./image/abeille_menu.png')
    while config.play:
        while True:
            clic = g.recupererClic()
            if clic is not None:
                actualisation_background()
                if (clic.x - clic.x % config.taille_carre_x)//config.taille_carre_x <= 15:
                    abeille1.x = (clic.x - clic.x % config.taille_carre_x)//config.taille_carre_x
                else:
                    abeille1.x = 15
                abeille1.y = (clic.y - clic.y % config.taille_carre_y)//config.taille_carre_y
                if abeille1.y == y_old and abeille1.x == x_old:
                    dessiner_case_deplacement(abeille1.x,abeille1.y,abeille1.equipe,abeille1.classe,y_old,x_old) # developper le système de case rouge
                config.condi = backend.case_valide(abeille1.x,abeille1.y,abeille1.equipe,abeille1.classe,y_old,x_old)

            if config.condi:
                config.condi = False
                break
        g.supprimer(carre)
        
        if config.nb_carre >= 16:
            carre = g.afficherImage(abeille1.x*config.taille_carre_x,abeille1.y*config.taille_carre_x,'./image/abeille_menu.png') # image de joueur normal
        else :
            carre = g.afficherImage(abeille1.x*config.taille_carre_x,abeille1.y*config.taille_carre_x,'./image/abeille_menu_mini.png') # image de joueur en mode mini ( prevu pour nb_carre = 8)
        dessiner_spawn()
        y_old = abeille1.y  # type: ignore  Le y et le x sont forcement defini car on est sortie de la boucle 
        x_old = abeille1.x  # type: ignore



    # Boucle à vide qui attend un clic
    g.attendreClic()

    # Fermeture fenêtre
    g.fermerFenetre()
def get_couleur_map(x:int,y:int,black:bool = False)->str:
    """
    Docstring for get_couleur_map
    
    :param x: Coordonnée x de la position sur la map
    :type x: int
    :param y: Coordonnée y de la position sur la map
    :type y: int
    :param black: Est-ce que la case actuelle est une case est noir sinon elle sera blanche par défault
    :type black: bool
    :return: Retourne un couleur en str
    :rtype: str
    """
    if not 0 <= x <= config.nb_carre_x and 0 <= y <= config.nb_carre_y:
        print(f"erreur de oob x ={x}, y : {y}")
        print(f"{config.taille_carre_x},   {config.taille_carre_y}")
        return config.map_error_color
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

def stat_part():
    global g
    g.dessinerRectangle(config.xmax_game,0,config.xmax_stat,config.ymax_game,'gray')
    g.afficherTexte('J1',config.xmax_game+20,20,'red',20)

def dessiner_case_deplacement(x:int , y:int,equipe:int,class_ab:str,y_old:int,x_old:int):
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
    """
    liste = backend.get_list_deplacement(x,y)
    for x_list,y_list in liste:
        if backend.case_valide(x_list,y_list,equipe,class_ab,y_old,x_old):
            g.dessinerRectangle(x_list*config.taille_carre_x,y_list*config.taille_carre_y,config.taille_carre_x,config.taille_carre_y,config.map_player_color)
            #debug print(f"feur xl :{x_list} ||| yl : {y_list}")
def actualisation_background():
    """
    Docstring for actualisation_background

    Ressiner tout l'arrère plan en appellant les fonction prevue à cet effet
    """
    dessiner_background()
    dessiner_spawn()
    stat_part()


### lanecement du jeu ( info -> mettre les fonction avant pls)
if __name__ == "__main__": # Lance le jeu quand lancé seul 
    menu()