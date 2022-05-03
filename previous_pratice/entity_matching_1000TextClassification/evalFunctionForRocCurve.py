"""
This file is to create the eval function to obtain the roc curve
for the ground truth labels obtained from combineData.py.

The goal here is to find the best weight percentage for the eval function.

"""
import combineData
import numpy as np
# from sklearn import metrics
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt
import matplotlib as mpl
import argparse

mpl.rcParams['figure.figsize'] = (12, 10)
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']


def evalFunction(artistScore, trackScore, percentageForArtistScore=0.5):
    artistScoreRatio = artistScore / 100
    trackScoreRatio = trackScore / 100
    score = percentageForArtistScore * artistScoreRatio + (1 - percentageForArtistScore) * trackScoreRatio
    return score


# plot the roc:
def plot_roc(name, fp, tp, **kwargs):
    # fp, tp, _ = sklearn.metrics.roc_curve(labels, prediction)

    font = {'weight': 'bold',
            'size': 22}
    plt.plot(100 * fp, 100 * tp, label=name, linewidth=2, **kwargs)
    plt.xlabel('False positives [%]', **font)
    plt.ylabel('True positives [%]', **font)
    plt.xlim([-0.5, 100.5])
    plt.ylim([-0.5, 100.5])
    plt.grid(True)
    ax = plt.gca()
    ax.set_aspect('equal')
    # plt.figtext(0.05, 0.95, "auc score is " + "{0:.2f}".format(auc), **font)
    mpl.rc('font', **font)


def plot_prc(name, precision, recall, **kwargs):
    # precision, recall, _ = sklearn.metrics.precision_recall_curve(labels, prediction)

    plt.plot(precision, recall, label=name, linewidth=2, **kwargs)
    font = {'weight': 'bold',
            'size': 22}
    plt.xlabel('Recall', **font)
    plt.ylabel('Precision', **font)
    plt.xlim([0, 1])
    # plt.ylim([0, 1])
    plt.grid(True)
    ax = plt.gca()
    ax.set_aspect('equal')
    # plt.figtext(0.05, 0.95, "prc score is " + "{0:.2f}".format(pr_auc), **font)
    mpl.rc('font', **font)



def rocAndPrcCurve(manualStartIndex, manualEndIndex,
                   fuzzyScoreFile="fuzzyScores.txt", manualAnnotateFile="1000annotate.csv",
                   percentEval=None, isCombined=True):

    groundTruthLabels = combineData.combineData(manualStartIndex, manualEndIndex,
                                                fuzzyScoreFile, manualAnnotateFile, isCombined)

    index = [truth[0] for truth in groundTruthLabels]
    true = [truth[1] for truth in groundTruthLabels]
    true = np.array(true)

    allScores = combineData.importScore(fuzzyScoreFile)

    allRoc = []

    for k in range(len(percentEval)):
        score = []
        for i in index:
            row = allScores[i].replace("\n", "").split(",")
            artistScore, trackScore = float(row[1]), float(row[2])
            predictValue = evalFunction(artistScore, trackScore, float(percentEval[k]))
            score.append(predictValue)

        score = np.array(score)

        # roc curve:
        fpr, tpr, thresholds1 = roc_curve(true, score)
        roc_auc = roc_auc_score(true, score)
        allRoc.append(roc_auc)
        plot_roc("Weight={}".format(percentEval[k]), fpr, tpr, color=colors[k])
        plt.legend(loc='lower right')

    file_save = "roc_curve.png"
    plt.savefig("./temp/{}".format(file_save), format='png')
    plt.show()


    # prc curve
    allPrc = []
    for k in range(len(percentEval)):
        score = []
        for i in index:
            row = allScores[i].replace("\n", "").split(",")
            artistScore, trackScore = float(row[1]), float(row[2])
            predictValue = evalFunction(artistScore, trackScore, float(percentEval[k]))
            score.append(predictValue)

        score = np.array(score)

        # prc curve:
        precision, recall, thresholds2 = precision_recall_curve(true, score)
        pr_auc = average_precision_score(true, score)
        allPrc.append(pr_auc)
        plot_prc("Weight={}".format(percentEval[k]), precision, recall, color=colors[k])
        plt.legend(loc='lower left')

    file_save1 = "prc_curve.png"
    plt.savefig("./temp/{}".format(file_save1), format='png')
    plt.show()

    print("The selected weight percentages are: {}.".format(percentEval))
    print("All rocAUC are {}.\nAll prcAUC are {}.".format(allRoc, allPrc))
    return allRoc, allPrc

#
# fuzzyScoreFilename = "fuzzyScores.txt"
# labelScoreFilename = "1000annotate.csv"
# manualLabelStartIndex = 0
# manualLabelEndIndex = 1000
#
# rocAuc, prcAuc = rocCurve(manualLabelStartIndex, manualLabelEndIndex, fuzzyScoreFilename, labelScoreFilename, 0.5)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameters for evalFunctionForRocCurve. ')

    parser.add_argument('--startIndex', type=int, required=True,
                        help='start index for the manually labeled data')
    parser.add_argument('--endIndex', type=int, required=True,
                        help='end index for the manually labeled data')
    parser.add_argument('--fuzzyScoreFile', type=str, required=True,
                        help='path to the fuzzy score file (the default is "fuzzyScores.txt"')
    parser.add_argument('--manualLabelFile', type=str, required=True,
                        help='path to the manually labeled file (the default is "1000annotate.csv")')
    parser.add_argument('-p', '--percentForArtistScore', nargs='+', required=True,
                        help='set a list of weight percentage for eval function')
    parser.add_argument('--combined', action=argparse.BooleanOptionalAction, required=True,
                        help='select whether to combine manual label '
                             'and fuzzywuzzy label with both as 0 and 100 scores'
                             'need to use "--combined" or "--no-combined" in the arg')
    args = parser.parse_args()
    rocAndPrcCurve(args.startIndex, args.endIndex, args.fuzzyScoreFile, args.manualLabelFile,
                   args.percentForArtistScore, args.combined)

# current calling command line:
    # python .\evalFunctionAndAUC.py --startIndex=0 --endIndex=1000 --fuzzyScoreFile="fuzzyScores.txt"
    # --manualLabelFile="1000annotate.csv" -p 0.2 0.4 0.5 0.6 0.8 --combined/--no-combined
