import statistics
import time

from dominoGame import DominoGame
from dominoGameAI import DominoGameAI
from playerDominoHumain import PlayerDominoHumain
from playerdomino import PlayerDomino
from pieceDomino import PieceDomino
from actionDomino import ActionDomino

if __name__ == "__main__":

    # joueur1 = PlayerDominoHumain("Léo")
    # joueur2 = PlayerDomino("Nino")
    # joueur3 = PlayerDomino("Loan")
    #
    # listJoueur1 = [joueur1, joueur2, joueur3]
    #
    # listJoueur2 = [joueur2, joueur3]
    #
    # partieDomino = DominoGame(listPlayer=listJoueur2, scoreMax=100, display=False)
    #
    # # partieDomino.playGame()
    # # print(f"\nScores à la fin de la manche {partieDomino.indexManche} :")
    # # for joueur in partieDomino.listPlayer:
    # #     print(f"\t- Joueur {joueur.getName()} : {joueur.getScore()}/{partieDomino.scoreMax} points")
    # # partieDomino.playGame()
    # # print(f"\nScores à la fin de la manche {partieDomino.indexManche} :")
    # # for joueur in partieDomino.listPlayer:
    # #     print(f"\t- Joueur {joueur.getName()} : {joueur.getScore()}/{partieDomino.scoreMax} points")
    # temps = []
    # startGlob = time.time()
    #
    # nbParties = 1000
    # for _ in range(1000):
    #     startGame = time.time()
    #     partieDomino.playGame()
    #     temps.append(time.time()-startGame)
    # print(f"Fin des {nbParties} parties !")
    # print(f"Temps total : {round(time.time()-startGlob, 5)} secondes")
    # print(f"Temps moyen par partie : {round(statistics.mean(temps), 5)} secondes")
    # print(f"Nombre moyen de parties par minutes : {int(60/statistics.mean(temps))}")

    joueurRandom1 = PlayerDomino("Bob")

    gameTraining = DominoGameAI([joueurRandom1], display=True)