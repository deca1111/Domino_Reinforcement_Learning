import statistics
import time

from dominoObjectOrientedVersion.dominoGameAI import DominoGameAI
from dominoObjectOrientedVersion.playerDominoHumain import PlayerDominoHumain
from dominoObjectOrientedVersion.playerdomino import PlayerDomino
from agent_models.agent2Player import Agent2Player

if __name__ == "__main__":

    joueur1 = PlayerDominoHumain("Léo")
    # joueur2 = PlayerDomino("Nino")
    # joueur3 = PlayerDomino("Loan")
    # #
    # listJoueur1 = [joueur1, joueur2, joueur3]
    #
    # listJoueur2 = [joueur2, joueur3]
    #
    # partieDomino = DominoGame(listPlayer=listJoueur2, scoreMax=100, display=True)
    #
    # partieDomino.playGame()
    # # print(f"\nScores à la fin de la manche {partieDomino.indexManche} :")
    # for joueur in partieDomino.listPlayer:
    #     print(f"\t- Joueur {joueur.getName()} : {joueur.getScore()}/{partieDomino.scoreMax} points")
    # partieDomino.playGame()
    # print(f"\nScores à la fin de la manche {partieDomino.indexManche} :")
    # for joueur in partieDomino.listPlayer:
    #     print(f"\t- Joueur {joueur.getName()} : {joueur.getScore()}/{partieDomino.scoreMax} points")
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

    # joueurRandom1 = PlayerDomino("Bob")
    # joueurRandom2 = PlayerDomino("Robert")
    # joueurRandom3 = PlayerDomino("David")
    #
    # listOpponent2Joueurs = [joueurRandom1]
    # listOpponent3Joueurs = [joueurRandom1, joueurRandom2]
    # listOpponent4Joueurs = [joueurRandom1, joueurRandom2, joueurRandom3]
    #
    # gameTraining = DominoGameAI(listOpponent4Joueurs, display=True)
    # while True:
    #     reward, gameOver, classement = gameTraining.playStep(gameTraining.currentPossibleAction[0])
    #
    #     print(f"Reward : {reward}, GameOver : {gameOver}, Classement : {classement}")
    #     if gameOver:
    #         break

    agent = Agent2Player()

    agent.startTraining(25000, "dominoRL_V1-2_2P")
