import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plotMetrics(x, y, xMean, yMean):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    # Clear
    plt.clf()

    plt.title("Entrainement...")
    plt.xlabel("Nb parties")
    plt.ylabel("% victoire")

    plt.plot(x, y, label="Globale")
    plt.plot(xMean, yMean, label="100 dernière games")
    plt.ylim(0, 1)

    plt.legend()
    plt.show(block=False)
    plt.pause(.1)


def savePlot(x, y, xMean, yMean, filename):
    plt.title("Fin de l'entrainement")
    plt.xlabel("Nb parties")
    plt.ylabel("% victoire")
    plt.ylim(0, 1)

    plt.plot(x, y, label="Globale")
    plt.plot(xMean, yMean, label="100 dernière games")

    plt.legend()
    plt.savefig(filename)

# plotClassement = [1, 2, 2, 1]
# plotMeanClassement = [1, 1.5, 5 / 3, 6 / 4]
# plotProportionVictoire = [1, 0.5, 1 / 3, 0.5]
# totalClassement = 6
# totalVictoire = 2
#
# plotMetrics(plotClassement, plotMeanClassement, plotProportionVictoire)
