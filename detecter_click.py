import tkiteasy as tke
ymax = 600
xmax = 800
click = None

# Ouverture de fenêtre
g = tke.ouvrirFenetre(xmax, ymax)
for bcx in range(0,5):
    while True:
        clic = g.recupererClic()
        if clic is not None:
            break
    g.dessinerRectangle(0,0,xmax,ymax,'black')    
    g.dessinerRectangle(clic.x -20,clic.y -20,40,40,'red')

g.attendreClic()           
# Fermeture fenêtre
g.fermerFenetre()