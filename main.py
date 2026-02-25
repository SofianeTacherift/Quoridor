from logique import *
from graphique import *
from tkinter import *
from networkx import *
# "C:\Users\sofia\AppData\Local\Programs\Python\Python312\python.exe" ton_script.py


def main():
    # Création du jeu (graphe, joueur, etc.)
    jeu = Jeu()

    # Exemple : poser une barrière pour tester l'affichage
    # jeu.poserBarriere((2,2),(3,2),(2,3),(3,3), horizontal=True)

    # Lancer la fenêtre graphique
    FenetreJeu(jeu)

if __name__ == "__main__":
    main()


