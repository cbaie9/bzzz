import tkiteasy as tke
import backend # type: ignore
import lib_graphisme
import config


g = tke.ouvrirFenetre(config.xmax, config.ymax)


lib_graphisme.dessiner_background()
# Boucle à vide qui attend un clic
g.attendreClic()

# Fermeture fenêtre
g.fermerFenetre()


