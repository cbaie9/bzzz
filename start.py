import tkiteasy as tke
ymax = 600
xmax = 800
largeurcarre = 100 
# Ouverture de fenêtre
g = tke.ouvrirFenetre(xmax, ymax)

# Votre programme ICI

g.dessinerLigne(0,0,xmax,ymax,'VioletRed')
g.dessinerLigne(0,ymax/2,xmax,ymax/2,'VioletRed')
g.dessinerLigne(0,ymax,xmax,0,'red')
g.dessinerLigne(xmax/2-largeurcarre*0.5,ymax/2-largeurcarre*0.5,xmax/2+largeurcarre*0.5,ymax/2-largeurcarre*0.5,"blue")
g.dessinerLigne(xmax/2-largeurcarre*0.5,ymax/2+largeurcarre*0.5,xmax/2+largeurcarre*0.5,ymax/2+largeurcarre*0.5,"blue")
g.dessinerLigne(xmax/2-largeurcarre*0.5,ymax/2-largeurcarre*0.5,xmax/2-largeurcarre*0.5,ymax/2+largeurcarre*0.5,"blue")
g.dessinerLigne(xmax/2+largeurcarre*0.5,ymax/2-largeurcarre*0.5,xmax/2+largeurcarre*0.5,ymax/2-largeurcarre*0.5,"blue")
# Boucle à vide qui attend un clic
g.attendreClic()

# Fermeture fenêtre
g.fermerFenetre()
