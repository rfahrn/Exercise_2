import sklearn
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_recall_fscore_support

# example labeler
#labeler1 = [2, 0, 2, 2, 0, 1]
#labeler2 = [0, 0, 2, 2, 0, 2]

# us
Rebecka_labeling = []
Jesica_labeling = []



def get_TP_FP_FN_(file):
    TP = []
    FP = []
    FN = []
    """opens the csv-file of the annotations and returns 3 lists => TP: list, FP:list, FN:list"""
    return TP,FP,FN

def get_IAA_KAPPA(labeler1,labeler2):
    return cohen_kappa_score(labeler1, labeler2)


def precision_recall_fmeasure(tp,fp,fn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fMeasure = (2 * precision * recall) / (precision + recall)
    return precision, recall, fMeasure

def main():
    #TP, FP, FN = get_TP_FP_FN_('RebeckaANN.csv')
    #TP, FP, FN = get_TP_FP_FN_('JessicaANN.csv')



    pass




if __name__ == '__main__':
    main()