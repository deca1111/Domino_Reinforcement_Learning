import copy
import random
import statistics
import time
from itertools import chain, product
import utils

nbParties = 1000

tempsParties = []

display = False

for i in range(nbParties):

    start = time.time()

    # seedPartie = 100
    nbJoueurs = 3
    scoreMax = 150

    # Initialisation de l'aléatoire
    # random.seed(seedPartie)

    # L'index de la liste représente le nombre de joueurs et la valeur le nombre de pièce à distribuer à chaque joueur
    nbPieces = [0, 0, 7, 6, 6, 4, 4]

    scoresJoueurs = [0] * nbJoueurs

    isGameOver = False
    mancheActuelle = 1

    while not isGameOver:

        # ============================================= Début d'une manche =============================================
        if display:
            print(f"\n============================= Début de la manche {mancheActuelle} =============================")

        isMancheOver = False

        # Distribution des dominos
        pioche = copy.deepcopy(utils.listPiece)
        random.shuffle(pioche)
        mainsJoueurs = [[] for _ in range(nbJoueurs)]
        for _, indexJoueur in product(range(nbPieces[nbJoueurs]), range(nbJoueurs)):
            piecePioche = pioche.pop(0)
            mainsJoueurs[indexJoueur].append(piecePioche)

        if display:
            for joueur, main in enumerate(mainsJoueurs):
                print(f"Main du joueur {joueur} : {main}")

            print(f"Pioche : {pioche}")

        # Vérification qu'il n'y a pas de série (1|0 à 1|6 par exemple)
        if nbJoueurs == 2:

            isSerie = False
            for joueur in range(nbJoueurs):
                for seriePossible in set(mainsJoueurs[joueur][0]):
                    for paire in mainsJoueurs[joueur][1:]:
                        if seriePossible not in paire:
                            break
                    else:
                        isSerie = True
                        if display:
                            print(f"Il y a une serie pour le joueur {joueur} : {mainsJoueurs[joueur]}")
                        break
                if isSerie:
                    break

            isMancheOver = True

        # Détermination de la première pièce
        # On commence par chercher le plus grand double dans les mains des joueurs
        try:
            snake = max(
                (x, y) for x, y in list(chain.from_iterable(mainsJoueurs)) if x == y
                )
        except Exception:
            snake = max(((x, y) for x, y in list(chain.from_iterable(mainsJoueurs))), key=lambda x: sum(x))

        premierJoueur = 0

        # On l'enlève de la main de son propriétaire
        for i in range(nbJoueurs):
            if snake in mainsJoueurs[i]:
                mainsJoueurs[i].remove(snake)
                premierJoueur = i
                break

        if display:
            print(f"Premier joueur : {premierJoueur}")
            print(f"Snake : {snake}")

        # Initialisation du plateau
        plateau = [snake]
        tourActuel = 1

        while not isMancheOver and not isGameOver:

            # ============================================ Début d'un tour ============================================
            if display:
                print(f"\n__________________ Début du tour {tourActuel} __________________")

            nbJoueurTour = 1
            isTourOver = False

            # On sauvegarde les mains au début du tour
            mainDebutTour = copy.deepcopy(mainsJoueurs)

            # Un tour de jeu
            while not isTourOver and not isMancheOver and not isGameOver:

                joueurActuel = (nbJoueurTour + premierJoueur) % nbJoueurs

                if display:
                    print(f"\nC'est au joueur {joueurActuel} de jouer")
                    print(f"Main du joueur : {mainsJoueurs[joueurActuel]}")
                    print(f"État du plateau : {plateau}")

                if actionPossible := utils.generatePossibleAction(
                        plateau, mainsJoueurs[joueurActuel]
                        ):

                    actionJoue = utils.pickRandomAction(actionPossible)

                    if display:
                        # Affichage des actions possibles
                        print("Actions possible :")
                        for action in actionPossible:
                            print(f"\t- {action} : {utils.getPieceFromIndexAction(action)}")

                        print(f"Le joueur {joueurActuel} a choisi l'action {utils.getPieceFromIndexAction(actionJoue)}")

                    plateau, mainsJoueurs[joueurActuel] = utils.computeAction(plateau, mainsJoueurs[joueurActuel],
                                                                              actionJoue)

                    # Si le joueur qui a joué a la main vide, il a gagné la manche
                    if len(mainsJoueurs[joueurActuel]) == 0:
                        isMancheOver = True

                        if display:
                            print(f"Le joueur {joueurActuel} a posé toutes ses pièces !")

                # Si il n'y a pas d'action possible, on pioche (si possible) et on passe son tour
                else:
                    if display:
                        print("Pas d'actions possible")

                    if len(pioche) > 0:
                        piecePioche = pioche.pop(0)
                        mainsJoueurs[joueurActuel].append(piecePioche)

                        if display:
                            print(f"\tLe joueur {joueurActuel} à pioché la pièce {piecePioche}")
                    else:
                        if display:
                            print(f"La pioche est vide, le joueur {joueurActuel} passe son tour")

                if display:
                    print(f"\nPlateau après le tour du joueur {joueurActuel} : {plateau}")

                nbJoueurTour += 1
                if nbJoueurTour > nbJoueurs:
                    isTourOver = True

            # ============================================= Fin d'un tour =============================================
            if display:
                print(f"\n__________________ Fin du tour {tourActuel} __________________")

            tourActuel += 1

            # Si les mains des joueurs sont les mêmes au début et à la fin de la manche, c'est qu'on ne peut plus jouer
            # et que la pioche est vide, on arrête donc la manche.
            if mainDebutTour == mainsJoueurs:
                isMancheOver = True

                if display:
                    print("Partie bloqué, fin de la manche et comptage des points")

        # ============================================== Fin d'une manche ==============================================

        # On update les scores
        scoresJoueurs = utils.computeScores(mainsJoueurs, scoresJoueurs)

        for joueur in range(nbJoueurs):
            if scoresJoueurs[joueur] >= scoreMax:
                isGameOver = True

        if display:
            print(f"\nScores à la fin de la manche {mancheActuelle} :")
            for joueur in range(nbJoueurs):
                print(f"\t- Joueur {joueur} : {scoresJoueurs[joueur]}/{scoreMax} points")

            print(f"\n============================= Fin de la manche {mancheActuelle} =============================")

        mancheActuelle += 1

    classement = [*range(nbJoueurs)]
    classement.sort(key=lambda x: scoresJoueurs[x])

    if display:
        print("\nFin de la partie !")

        print(f"Le joueur {classement[0]} a gagné avec {scoresJoueurs[classement[0]]}")

        print("\nClassement complet :")
        for joueur in classement:
            print(f"\t- Joueur {joueur} : {scoresJoueurs[joueur]} points")

    tempsParties.append(time.time() - start)

print(f"Fin des {nbParties} parties !")
print(f"Temps moyen : {round(statistics.mean(tempsParties), 5)} secondes par parties")
print(f"Nombre moyen de parties pas minutes : {int(60/statistics.mean(tempsParties))}")
