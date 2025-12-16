import tkiteasy as tke # type: ignore
import config
import backend


def dessiner_background(): #quadriage selon la couleur des spawn via la matrice map
    """
    Dessine l'arrière plan du jeu en fonction des constant de base
    """
    compteur = 0
    for x in range(0,config.xmax,config.taille_carre_x):
        
        for y in range(0,config.ymax,config.taille_carre_y):
            g.pause(0.0001)
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
    x_old = None
    y_old = None
    abeille1 = backend.abeille(0,0,1,0,'smashbro',True)
    global g  
    g = tke.ouvrirFenetre(config.xmax, config.ymax)
    dessiner_background()
    dessiner_spawn()
    carre = g.dessinerRectangle(0,0,0,0, config.map_player_color)
    while config.play:
        while True:
            clic = g.recupererClic()
            if clic is not None:
                abeille1.x = (clic.x - clic.x % config.taille_carre_x)/config.taille_carre_x
                abeille1.y = (clic.y - clic.y % config.taille_carre_y)/config.taille_carre_y
                if y_old == None or x_old == None:
                    y_old = abeille1.y
                    x_old = abeille1.x
                if abeille1.x != x_old or abeille1.y != y_old:
                    print(f"y :{abeille1.y}   | y_old :  {y_old}")
                    print(f"x :{abeille1.x}   | x_old :  {x_old}")
                    if (abeille1.x+1 == x_old or abeille1.x-1 == x_old or abeille1.x == x_old) and (abeille1.y+1 == y_old or abeille1.y-1 == y_old or abeille1.y==y_old):
                        config.condi = True
                else:
                    config.condi = True 
            if config.condi:
                config.condi = False
                break
        g.supprimer(carre)
        carre = g.dessinerRectangle(abeille1.x*config.taille_carre_x,abeille1.y*config.taille_carre_x,config.taille_carre_x,config.taille_carre_y,config.map_player_color) # type: ignore
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
    else:
        output = config.map_error_color
    return output
def dessiner_spawn():
    g.afficherImage(config.xmax-config.taille_carre_x,config.ymax-config.taille_carre_y,"./image/spawn/red.png",'center')
    g.afficherImage(config.taille_carre_x,config.ymax-config.taille_carre_y,"./image/spawn/blue.png",'center')
    g.afficherImage(config.taille_carre_x,config.taille_carre_y,"./image/spawn/green.png",'center')
    g.afficherImage(config.xmax-config.taille_carre_x,config.taille_carre_y,"./image/spawn/violet.png",'center')