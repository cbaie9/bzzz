# Bzzz

Cette repo [[github](https://github.com/cbaie9/bzzz)] est consacré au jeu BZZZ pour la saé 1.01 et 1.02

# Installation et lancement
Prérequis
#Python 3.8+
#tkinter(inclus dans Python standard)
#tkiteasy (fourni dans  'tkiteasy.py')
## Pour démarrer le jeu

Lancer le fichier start.py ou backend.py
```./start.py```

## But du jeu
Le jeu est simple, récolter le plus de la moitié du nectar ou en avoir le plus à la fin des 300 tour de jeu
Le jeu se joue a 4 joueurs qui tourne sur le jeu, chaque joueur commence avec une abeille éclaireuse sur son spawn et 10 nectar de base, ou il peut se deplacer en cliquant sur un abeille de son équipe sur une case bleu affiché ou en rose pour une fleur pour s'y deplace et y butiner automatiquement. Il faut faire attention aux abeille ennemis qui peuevent vous attaquer si se trouvent à coté et cela déclanchera une escarmouche où chaque abeille devra esquiver un attaque avec un probabilité en fonction de la force et du nombre d'opposant 



# Documentation

Le code possède 2 fonction qui peuvent demarré le jeu ; menu qui demarrera le menu du jeu avec le nom et une abeille qui se déplacera aléatoirement et start() qui est la fonction boucle principal du jeu où se lanceront toutes les autres fonctions du jeu

Ici je vais faire le tour de la plupart des fonction critique du programme et ne faire un petit description

## Fichier lib_graphisme.py

### start() (lib_graphisme.py)

Fonction principal du programme, gèrent du système de tour et de selection des abeille, tout ce qui touchent aux abeille doit rester dans cette fonction principal sous peine de ne pas être sauvegarder et ne pas utilisable dans la suite de la partie

### actualisation_background

Gèrent et lance tous les fonction lié à l'actualisation de l'arrière plan comme le dessin de la map en foncion de la matrice map, des spawn

### afficher_abeille/affiche_tous_les_abeilles 

Fonction qui affiche une abeille en particuiler où tous les abeille contenue dans la liste des abeille de joueur de 1 à 4 

### Dessiner case deplacement 

Fonction qui afficher les case 'bleu' où le joueur peut se déplacer via des appel avec la map et la position des joueur acteuelle 

### fin de tour

Fonction qui effectué les verification de fin de tour pour terminer la partie, actualiser la partie stat de écran aussi

### stat_part

Fonction qui dessine toute la partie statistique de l'écran en fonction du joueur actuel avec précalcul si les bouton peuvent être appuyé ou chager la coueleur affiché

### get image sprite 

Fonction qui renvoie l'image associé à l'abeille demandé en fonction et la classe équipe et de son état


### clic formate

Fonction qui formate le clic afin d'obtenir un format de clic par case qui peut être utilisable pour des calcul de coordonnées de map

### bouton stat 

Fonction qui calcul si le clic effectué se trouve sur les botuon de la partie statistique

## Fichier backend.py

### creation matrice map

Fonction qui créer la map sous la forme de liste de liste de int et implémente les spawns etc les fleur en changeant les donnée à certain coordonnées

### case valide 

Fonction qui dit un deplacement est valide selon l'équipe, la classe du joueur, de la position précedente et si une abeille est déjà présente sur la case 


### get list deplacement

Fonction qui renvoie les position autour de celle demande en fonction du mode demande qui fait varié les case renvoyer comme le mode 1 qui renvoie les toute les case autour de celle demandé y compris la case unitial, pour le mode renvoie les position acessible par les bourdon et les ouvrière ( deplacement) et pour le mode 3 ; Ne renvoie pas la position du joueur mais uniquement les case autour ( liste pour les escarmouches)

### est butinable 

Fonction qui renvoie si l'emplacement est butinable à cette endroit ( coté map/server uniquement)


### Butinage 

Fonction qui butine la fleur à la postion et ajoute le nectar a l'abeille


MAJ : Retourne le nectar que l'on doit donnée a abeille avec un appel de type
    abeille.nectar += butinage(abeille,abeille.x,abeille.y)
    Note pour raison pratique pensez a actualiser les stat après l'appel ( non obligatoire mais instinctif pour debug et le joueur)

### Fonction get spawn coor

Fonction qui renvoie les coordonnée du spawn choisi

Mode 1: Renvoie la coordonnées x du spawn du joueur choisi
Mode 2: Renvoie la coordonnées y du spawn du joueur choisi
Mode 3: Renvoie les coordonnées sous la forme d'un tuple (x,y)

### ya_quelqun

Fonction  qui renvoie si une abeille se trouve sur les coordonnées démande et renvoie un booléen en fonction de ça

### Création abeille 

Fonction qui créer un abeille et renvoie l'abeille créer à la fin de la fonction

### escarmouche

Fonction gèrant le fonctionnement général des escarmouche avec la detection, le calcul des probabilité d'esquive et le renvoie d'une liste des abeille qui sont tombée au combat ( KO )

### get oppo 

Fonction renvoyant le nombre d'opposant dans une liste donnée

### get abeilles pos

Fonction qui renvoie l'abeille à une position données si elle existe



# Credit :

Developpement : @cbaie9, @casstssn, @usualsuspect940

Texturing image : @fufuBS1 ( sur Discord / github)
