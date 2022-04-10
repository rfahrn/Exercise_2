#!/usr/local/bin/python3
# *-* coding: UTF-8 *-*
# Authors: Jessica Roady & Rebecka Fahrni

from sklearn.metrics import cohen_kappa_score
import pandas as pd


def get_IAA_KAPPA(labeler1,labeler2):
    """ Returns Kappa-score """
    return cohen_kappa_score(labeler1, labeler2)


def precision_recall_fmeasure(tp, fp, fn):
    """ Calculates precision, recall, and F-measure """
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fMeasure = (2 * precision * recall) / (precision + recall)
    return precision, recall, fMeasure


def file_to_dataframe(file1, file2):
    """ Opens two .csv files, creates pandas-dataframe, and returns for each file TP/FP/FN """
    last3_df1 = pd.read_csv(file1).iloc[:,-3:].fillna(0)
    last3_df2 = pd.read_csv(file2).iloc[:,-3:].fillna(0)

    TP1 = last3_df1['TP'].to_numpy()
    FP1 = last3_df1['FP'].to_numpy()
    FN1 = last3_df1['FN'].to_numpy()
    TP2 = last3_df2['TP'].to_numpy()
    FP2 = last3_df2['FP'].to_numpy()
    FN2 = last3_df2['FN'].to_numpy()

    TP1sum = last3_df1['TP'].sum()
    FP1sum = last3_df1['FP'].sum()
    FN1sum = last3_df1['FN'].sum()
    TP2sum = last3_df2['TP'].sum()
    FP2sum = last3_df2['FP'].sum()
    FN2sum = last3_df2['FN'].sum()

    return (TP1sum, FP1sum, FN1sum), (TP2sum, FP2sum, FN2sum), (TP1, FP1, FN1), (TP2, FP2, FN2)


def main():
    A1, A2, A1arr, A2arr = file_to_dataframe('jessica.csv', 'rebecka.csv')

    precision1, recall1, fMeasure1 = precision_recall_fmeasure(A1[0], A1[1], A1[2])
    precision2, recall2, fMeasure2 = precision_recall_fmeasure(A2[0], A2[1], A2[2])

    print(f'Annotator 1:\n'
          f'\tPrecision: {round(precision1,2)}\tRecall: {round(recall1,2)}\tF-measure: {round(fMeasure1,2)}\n')
    print(f'Annotator 2:\n'
          f'\tPrecision: {round(precision2,2)}\tRecall: {round(recall2,2)}\tF-measure: {round(fMeasure2,2)}\n')

    # Our labels:
    labeler1TP = A1arr[0]
    labeler2TP = A2arr[0]
    labeler1FP = A1arr[1]
    labeler2FP = A2arr[1]
    labeler1FN = A1arr[2]
    labeler2FN = A2arr[2]

    TP_kappa = round(get_IAA_KAPPA(labeler1TP, labeler2TP), 4)
    FP_kappa = round(get_IAA_KAPPA(labeler1FP, labeler2FP), 4)
    FN_kappa = round(get_IAA_KAPPA(labeler1FN, labeler2FN), 4)

    print(f'TP Kappa: {TP_kappa}\nFP Kappa: {FP_kappa}\nFN Kappa: {FN_kappa}')


if __name__ == '__main__':
    main()
