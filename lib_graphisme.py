import tkiteasy as tke # type: ignore
import config
import backend
import random


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
    abeille1 = backend.abeille(0,0,1,0,'smashbro',True,config.id_actuelle)
    global g  
    g = tke.ouvrirFenetre(config.xmax, config.ymax)
    dessiner_background()
    dessiner_spawn()
    carre = g.dessinerRectangle(0,0,0,0, config.map_player_color)
    while config.play:
        while True:
            clic = g.recupererClic()
            if clic is not None:
                abeille1.x = (clic.x - clic.x % config.taille_carre_x)//config.taille_carre_x
                abeille1.y = (clic.y - clic.y % config.taille_carre_y)//config.taille_carre_y
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
    g.afficherImage(config.xmax-config.taille_image_spawn,config.ymax-config.taille_image_spawn,"./image/spawn/red.png")
    g.afficherImage(0,config.ymax-config.taille_image_spawn,"./image/spawn/blue.png")
    g.afficherImage(0,0,"./image/spawn/green.png")
    g.afficherImage(config.xmax-config.taille_image_spawn,0,"./image/spawn/violet.png")
# <---------------------------------- >
def menu(): # Menu du jeu
    global g 
    g = tke.ouvrirFenetre(config.taille_mini, config.taille_mini)
    g.afficherImage(0,0,'./image/background_menu.png')
    # titre
    g.dessinerRectangle((config.taille_mini/2)-(config.taille_mini/4),(config.taille_mini/8)-(config.taille_mini/16),config.taille_mini/2,config.taille_mini/8,'yellow')
    g.afficherTexte("BZZZ",config.taille_mini/2,config.taille_mini/8,'red')
    # btn jouer
    g.dessinerRectangle((config.taille_mini/2)-(config.taille_mini/4),(config.taille_mini)-((config.taille_mini/8))-(config.taille_mini/16),config.taille_mini/2,config.taille_mini/8,'black')
    g.afficherTexte("Jouer",config.taille_mini/2,config.taille_mini-config.taille_mini/8,'white')
    
    carre = g.dessinerRectangle(10,10,50,50,'red')  # initialisation de l'abeille du menu "carre"
    g.supprimer(carre)
    vx = 10 # definition de la veloctée de l'abeille
    vy = 10
    while True: # boucle infini pour l'interface menu
        
        while True: # boucle 'infini' pour récupere le click
            clic = g.recupererClic()
            if clic is not None:
                break
            if carre.x <= 0 or carre.x+50 > config.taille_mini : # colision avec les mur de l'interface ( gauche + droite)
                vx *= -1
                if vx > 50:  # Sécurité pour que la vitesse n'aille pas trop haute
                    vx = 50
            if carre.y <= 0 or carre.y+50 >= config.taille_mini : # colision avec les mur de l'interface ( haut + bas)
                vy *= -1
                if vy > 50 :
                    vy = 50
            g.deplacer(carre,vx,vy)
            g.pause(0.05)

        ### action réaliser quand on fait un lcik
        if random.randint(1,2) == 1: # randomisation de la direction de lancement (axe x)
            vx = 10
        else :
            vx = -10
        if random.randint(1,2) == 1: # randomisation de la direction de lancement (axe y)
            vy = 10
        else :
            vy = -10
        g.supprimer(carre)
        x = (clic.x)-50
        y = (clic.y)-50
        carre = g.afficherImage(x,y,'./image/abeille_menu.png')
        #### fin
        ### colision du bouton jouer
        if ((config.taille_mini/2)-(config.taille_mini/4)) <= clic.x <= ((config.taille_mini/2)-(config.taille_mini/4))+config.taille_mini/2 : # collsion x bouton jouer
            if ((config.taille_mini)-((config.taille_mini/8))-(config.taille_mini/16)) <= clic.y <= ((config.taille_mini)-((config.taille_mini/8))-(config.taille_mini/16))+config.taille_mini/8:
                break
    # Fermeture fenêtre et lancement du jeu
    g.fermerFenetre()
    start()

if __name__ == "__main__": # Lance le jeu quand lancé seul 
    menu()