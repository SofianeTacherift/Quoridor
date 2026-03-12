import tkinter as tk
from logique import *

class FenetreJeu:

    def __init__(self, jeu):
        self.jeu = jeu

        

        self.root = tk.Tk()
        self.root.title("Quoridor")

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.on_click)
        self.root.bind("<Key>", self.on_key)
        self.canvas.bind("<Configure>", self.on_resize)

        self.bandeau = tk.Frame(self.root, bg="#222", height=60)
        self.bandeau.pack(fill="x")

        self.labelTouches = tk.Label(self.bandeau,text="ZQSD : déplacement - E : mode barrière - R : tourner barrière - A : placer barrière", 
                                     bg="#222", fg="white",
                                     font=("Arial",  18))
        self.labelTouches.pack(side="bottom")

        self.labelStatus = tk.Label(self.bandeau, text="", 
                                    font=("Arial", 18, "bold"), bg="#222", fg="white")
        self.labelStatus.pack(side="left", padx=20, pady=10)

        self.boutonRejouer = tk.Button(self.bandeau, text="Rejouer", 
                                        font=("Arial", 14), command=self.rejouer,
                                        bg="#444", fg="white", relief="flat", padx=10)
        self.boutonRejouer.pack(side="right", padx=20, pady=10)

        self.largeur = 1
        self.hauteur = 1
        self.barriereEnCours=None

        self.root.mainloop()

    def on_resize(self, event):
        self.largeur = event.width
        self.hauteur = event.height
        self.redessiner()

    def on_click(self,event):
        return

        
    def on_key(self, event):

        joueur = self.jeu.tour
   
        if self.jeu.gagnant:
            return

        if (joueur==self.jeu.j1): 

            if event.keysym.lower() == "e":
                joueur.modeBarriere = not joueur.modeBarriere
                if (joueur.modeBarriere):
                    self.barriereEnCours=Barriere((3,2),(3,3),(4,2),(4,3),"horizontal") if joueur.modeBarriere else None
                    self.redessiner()
                    return
                else:
                    
                    self.barriereEnCours=None
                    joueur.modeBarriere=False
                    self.redessiner()

            if joueur.modeBarriere and event.keysym.lower() == "a":
                if self.jeu.poserBarriere(self.barriereEnCours):
                    joueur.modeBarriere=False
                    self.barriereEnCours=None
                    self.jeu.changerJoueur()
                    self.redessiner()
                    self.tourBot()

                return
            
            if joueur.modeBarriere and event.keysym.lower() == "r":
                self.barriereEnCours.changerDirection()


            if not joueur.modeBarriere:

                x = joueur.caseX
                y = joueur.caseY

                deplacement=False


                if event.keysym.lower() == "z":
                    deplacement=self.jeu.deplacerJoueurY(-1)



                elif event.keysym.lower() == "s": 
                    deplacement=self.jeu.deplacerJoueurY(1)

                
                elif event.keysym.lower() == "q":
                    deplacement=self.jeu.deplacerJoueurX(-1)

                elif event.keysym.lower() == "d":
                    deplacement=self.jeu.deplacerJoueurX(1)


                if (deplacement):
                    if (self.jeu.gagnant):
                        self.redessiner()
                        return
                    self.jeu.changerJoueur()
                    self.redessiner()
                    self.tourBot()
            
            elif joueur.modeBarriere:
                match (event.keysym.lower()):

                    case "d":
                        self.barriereEnCours.deplacerX(1)

                    case "q":
                        self.barriereEnCours.deplacerX(-1)

                    case "s":
                        self.barriereEnCours.deplacerY(1)

                    case "z":
                        self.barriereEnCours.deplacerY(-1)
                    

                self.redessiner()

    def tourBot(self):
        self.jeu.jouerBot()
        self.redessiner()
            


    def redessiner(self):
        if self.jeu.gagnant:
            self.afficher_gagnant()
        self.canvas.delete("all")
        self.dessiner_grille()
        self.dessiner_barrieres()
        self.dessiner_joueurs()

    def dessiner_grille(self):
        cell_w = self.largeur / 9
        cell_h = self.hauteur / 9

        for i in range(10):
            # verticales
            x = i * cell_w
            self.canvas.create_line(x, 0, x, self.hauteur)

            # horizontales
            y = i * cell_h
            self.canvas.create_line(0, y, self.largeur, y)

    def dessiner_joueurs(self):
        cell_w = self.largeur / 9
        cell_h = self.hauteur / 9

        # Joueur 1
        x = self.jeu.j1.caseX * cell_w + cell_w/2
        y = self.jeu.j1.caseY * cell_h + cell_h/2
        self.canvas.create_oval(x-self.hauteur/18+5, y-self.hauteur/18+5, x+self.hauteur/18-5, y+self.hauteur/18-5, fill="blue")

        x = self.jeu.j2.caseX * cell_w + cell_w/2
        y = self.jeu.j2.caseY * cell_h + cell_h/2
        self.canvas.create_oval(x-self.hauteur/18+5, y-self.hauteur/18+5, x+self.hauteur/18-5, y+self.hauteur/18-5, fill="red")

    def dessiner_barrieres(self):
        cell_w = self.largeur / 9
        cell_h = self.hauteur / 9



        for b in self.jeu.listeBarrieres:
            if b.direction=="horizontal":
                x1 = b.NO[1] * cell_w
                y1 = b.NO[0] * cell_h + cell_h
                x2 = b.NE[1] * cell_w + cell_w
                self.canvas.create_rectangle(x1, y1-5, x2, y1+5, fill="brown")
            else:
                x1 = b.NO[1] * cell_w + cell_w
                y1 = b.NO[0] * cell_h
                y2 = b.SO[0] * cell_h + cell_h
                self.canvas.create_rectangle(x1-5, y1, x1+5, y2, fill="brown")

        if (self.barriereEnCours):
            if self.barriereEnCours.direction=="horizontal":
                x1 = self.barriereEnCours.NO[1] * cell_w
                y1 = self.barriereEnCours.NO[0] * cell_h + cell_h
                x2 = self.barriereEnCours.NE[1] * cell_w + cell_w
                self.canvas.create_rectangle(x1, y1-5, x2, y1+5, fill="blue")
            else:
                x1 = self.barriereEnCours.NO[1] * cell_w + cell_w
                y1 = self.barriereEnCours.NO[0] * cell_h
                y2 = self.barriereEnCours.SO[0] * cell_h + cell_h
                self.canvas.create_rectangle(x1-5, y1, x1+5, y2, fill="blue")
    

    def rejouer(self):
        self.jeu.__init__()
        self.barriereEnCours = None
        self.labelStatus.config(text="À toi de jouer !", fg="white")
        self.redessiner()

    def afficher_gagnant(self):
        nom = "Joueur 1" if self.jeu.gagnant == self.jeu.j1 else "Bot"
        couleur = "blue" if self.jeu.gagnant == self.jeu.j1 else "red"
        self.labelStatus.config(text=f"{nom} a gagné !", fg=couleur)