import random
import time

# liste de mots pour le jeu
liste_mots = [""] #à remplir

# choisir un mot aléatoire de la liste des mots
mot = random.choice(liste_mots)

# initialiser les variables
lettres_trouvees = []
lettres_ratees = []
nb_erreurs_max = 7

# boucle principale du jeu
while True:
    # afficher les lettres trouvées et les lettres ratées
    print("Lettres trouvées : ", end="")
    for lettre in mot:
        if lettre in lettres_trouvees:
            print(lettre, end=" ")
        else:
            print("_", end=" ")
    print("\nLettres ratées : ", end="")
    for lettre in lettres_ratees:
        print(lettre, end=" ")
    print()

    # demander une lettre à l'utilisateur
    lettre = input("Entrez une lettre : ").lower()

    # vérifier si la lettre est dans le mot
    if lettre in mot:
        lettres_trouvees.append(lettre)
        if len(lettres_trouvees) == len(set(mot)):
            print("Bravo, vous avez trouvé le mot !")
            break
    else:
        lettres_ratees.append(lettre)
        if len(lettres_ratees) == nb_erreurs_max:
            print("Désolé, vous avez perdu. Le mot était", mot)
            break



####################################################################
#                                                                  #
#                          Jeux 2                                  #
#                                                                  #
####################################################################

# initialiser les variables
nombre_essais_max = 5
nombre_essais = 0
nombre_a_deviner = random.randint(1, 20)

# boucle principale du jeu
while nombre_essais < nombre_essais_max:
    # demander un nombre à l'utilisateur
    nombre = int(input("Devinez un nombre entre 1 et 20 : "))

    # comparer le nombre deviné avec le nombre à deviner
    if nombre == nombre_a_deviner:
        print("Bravo, vous avez deviné le nombre en", nombre_essais+1, "essais !")
        break
    elif nombre < nombre_a_deviner:
        print("Le nombre à deviner est plus grand.")
    else:
        print("Le nombre à deviner est plus petit.")

    nombre_essais += 1

# vérifier si le joueur a épuisé tous les essais
if nombre_essais == nombre_essais_max:
    print("Désolé, vous avez épuisé tous vos essais. Le nombre à deviner était", nombre_a_deviner)




####################################################################
#                                                                  #
#                          Jeux 3                                  #
#                                                                  #
####################################################################




# demander à l'utilisateur de saisir l'intervalle
borne_inf = int(input("Entrez la borne inférieure de l'intervalle : "))
borne_sup = int(input("Entrez la borne supérieure de l'intervalle : "))

# choisir un nombre aléatoire dans l'intervalle
nombre_a_deviner = random.randint(borne_inf, borne_sup)

# initialiser les variables
nombre_essais = 0
trouve = False

# chronométrer le temps écoulé
start_time = time.time()

# boucle principale du jeu
while not trouve:
    # demander au joueur de deviner un nombre
    nombre = int(input("Devinez un nombre entre " + str(borne_inf) + " et " + str(borne_sup) + " : "))
    nombre_essais += 1

    # comparer le nombre deviné avec le nombre à deviner
    if nombre == nombre_a_deviner:
        print("Bravo, vous avez deviné le nombre en", nombre_essais, "essais en", round(time.time() - start_time, 2), "secondes !")
        trouve = True
    elif nombre < nombre_a_deviner:
        print("Le nombre à deviner est plus grand.")
    else:
        print("Le nombre à deviner est plus petit.")
