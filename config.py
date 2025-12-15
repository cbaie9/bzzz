ymax = 800
xmax = 800
nb_carre = 16
if nb_carre == 16:
    nb_carre_y = 16
    nb_carre_x = 16
else:
    nb_carre_x = nb_carre
    nb_carre_y = nb_carre
taille_carre = xmax
taille_carre_x = int(xmax//nb_carre_x)
taille_carre_y = int(ymax//nb_carre_y)
play = True
condi = False
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