from math import sqrt
ymax :int = 800
xmax :int = 800
nb_carre :int = 16
if nb_carre == 16: # type: ignore
    nb_carre_y :int = 16
    nb_carre_x :int = 16
else:
    nb_carre_x = nb_carre
    nb_carre_y = nb_carre
taille_carre :int = xmax
taille_carre_x = int(xmax//nb_carre_x)
taille_carre_y = int(ymax//nb_carre_y)
play :bool = True  # A mettre sur faux pour couper le jeu | interrupteur général
condi :bool = False
taille_spawn_x :int = round(sqrt(nb_carre_x))
taille_spawn_y :int = round(sqrt(nb_carre_y))
# --------------------------------------
# Configuration des limite de fin de jeu
time_out = 300 # nb de tour max 
# ----------------------------------
# Configuration de l'interface de graphique
map_default_color_black = 'black'
map_default_color_white = 'white'
spawn_equipe_1bk :str = 'green'
spawn_equipe_1wh :str = "light green"
spawn_equipe_2bk :str = 'blue'
spawn_equipe_2wh :str = 'DeepSkyBlue'
spawn_equipe_3bk :str = 'dark violet'
spawn_equipe_3wh :str = 'purple'
spawn_equipe_4bk :str = 'red'
spawn_equipe_4wh :str = 'indian red'
map_error_color :str = 'orange'
map_flower_color :str = "DeepPink2"
map_player_color :str = "navy"
map_color_flower :str = "cyan"
# ---------------------------
# Gestion des Abeilles
id_actuelle :int = 0
list_abeille_J1 :list[int] = []
list_abeille_J2 :list[int] = []
list_abeille_J3 :list[int] = []
list_abeille_J3 :list[int] = []
# ----------------------------
# Gestion des fleurs
nectar_initial = 10
max_nectar = 45


# -----------------------
# Verification des règles de configuration
if max_nectar % 3 != 0:
    assert(f"Problème de configuration : Le nectar max n'est pas Disivible par 3 | Valeur Acteuelle : {max_nectar}")
if nb_carre % 2 != 0:
    assert(f"Problème de configuration : Le Nombre de Cases n'est pas Disivible par 2 | Valeur Acteuelle : {nb_carre}")
if time_out % 4 != 0:
    assert(f"Problème de configuration : Le nombre de tour max ( Time out ) n'est pas Disivible par 4 | Valeur Acteuelle : {time_out}")