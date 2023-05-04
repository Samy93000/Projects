from tkinter import *

expression = "0"

def appuyer(touche):
    global expression
    if expression == "0":
        expression = ""
    if touche == "=":
        calculer()
        return
    expression += str(touche)
    equation.set(expression)


def calculer():
    try:
        global expression
        total = str(eval(expression))

        equation.set(total)
        expression = total
    except:
        equation.set("erreur")
        expression = ""


def effacer():
    global expression
    expression = "0"
    equation.set(expression)

def effacer_expression():
    global expression
    if expression == "0":
        return
    expression = expression[:-1]
    if not expression:
        expression = "0"
    equation.set(expression)


if __name__ == "__main__":
    gui = Tk()

    # Couleur de fond
    gui.configure(background="#101419")

    # Titre de l'application
    gui.title("Calculatrice")

    # Tailler de la fenetre
    gui.geometry("300x500")

    # Variable pour stocker le contenu actual
    equation = StringVar()

    # Boite de resultats
    resultat = Label(gui, bg="#101419", fg="#FFF", textvariable=equation, height=2, font=("Calculator", 24), anchor="e")
    resultat.grid(columnspan=4, padx=20, pady=10, sticky="nsew")

    # Boutons
    boutons = [7, 8, 9, "*", 4, 5, 6, "-", 1, 2, 3, "+", 0, ".", "/", "="]
    ligne = 1
    colonne = 0

    for bouton in boutons:
        b = Label(gui, text=str(bouton), bg="#476C9B", fg="#FFF", height=4, width=6, font=("Calculator", 16), bd=2, relief="raised")
        # Rendre le texte cliquable
        b.bind("<Button-1>", lambda e, bouton=bouton: appuyer(bouton))

        b.grid(row=ligne, column=colonne, padx=5, pady=5, sticky="nsew")

        colonne += 1
        if colonne == 4:
            colonne = 0
            ligne += 1

    # Boutons Effacer

    b1 = Label(gui, text="<-",
               bg="#984447",
               fg="#FFF",
               height=2, width=13,
               font=("Calculator", 12), bd=2,
               relief="raised"
               )
    b1.bind("<Button-1>", lambda e: effacer_expression())
    b1.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    b2 = Label(gui, text="Effacer tout",
               bg="#984447",
               fg="#FFF",
               height=2,
               width=13,
               font=("Calculator", 12),
               bd=2, relief="raised")

    b2.bind("<Button-1>", lambda e: effacer())
    b2.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Configuration de la grille pour la rendre responsive
    for i in range(4):
        gui.grid_columnconfigure(i, weight=1)
    for i in range(6):
        gui.grid_rowconfigure(i,weight=1)

    # Lancement de l'interface
    gui.mainloop()
