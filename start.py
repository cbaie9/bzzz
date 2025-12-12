import tkiteasy as tke
import backend # type: ignore
import lib_graphisme
import config
play = True
x_old = None
y_old = None
condi = False
g = tke.ouvrirFenetre(config.xmax, config.ymax)
lib_graphisme.dessiner_background()
carre = g.dessinerRectangle(0,0,0,0,'red')
while play:
    while True:
        clic = g.recupererClic()
        if clic is not None:
            x = (clic.x - clic.x % config.taille_carre_x)/config.taille_carre_x
            y = (clic.y - clic.y % config.taille_carre_y)/config.taille_carre_y
            if y_old == None or x_old == None:
                y_old = y
                x_old = x
            if x != x_old or y != y_old:
                print(f"y :{y}   | y_old :  {y_old}")
                print(f"x :{x}   | x_old :  {x_old}")
                if (x+1 == x_old or x-1 == x_old or x == x_old) and (y+1 == y_old or y-1 == y_old or y==y_old):
                    condi = True
            else:
                condi = True 
        if condi:
            condi = False
            break
    g.supprimer(carre)
    carre = g.dessinerRectangle(x*config.taille_carre_x,y*config.taille_carre_x,config.taille_carre_x,config.taille_carre_y,'red') # type: ignore
    
    y_old = y  # type: ignore  Le y et le x sont forcement defini car on est sortie de la boucle 
    x_old = x  # type: ignore



# Boucle à vide qui attend un clic
g.attendreClic()

# Fermeture fenêtre
g.fermerFenetre()


