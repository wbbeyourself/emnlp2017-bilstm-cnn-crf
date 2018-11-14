# coding=utf-8

"""
@author: beyourself
@time: 2018/11/6 18:29
@file: evaluate.py
"""

import sys

sys.path.append('.')
sys.path.append('../')

CORRECT_TYPE = 'A'
PRONOUNCE_TYPE = 'B'
SHAPE_TYPE = 'C'
PUNCTUATION_TYPE = 'D'
TYPE_LIST = [CORRECT_TYPE, PRONOUNCE_TYPE, SHAPE_TYPE, PUNCTUATION_TYPE]


def confusion_matrix(label, predict):
    num_tags = len(TYPE_LIST)
    matrix = [[0 for i in range(num_tags)] for i in range(num_tags)]
    for i, types in enumerate(label):
        assert len(types) == len(predict[i])
        for j, t in enumerate(types):
            index_a = TYPE_LIST.index(t)
            index_predict = TYPE_LIST.index(predict[i][j])
            matrix[index_a][index_predict] += 1
    return matrix


def print_matrix(matrix):
    assert len(matrix[0]) == len(TYPE_LIST)
    length = len(TYPE_LIST)
    for i in range(length):
        total = sum(matrix[i])
        correct = matrix[i][i]
        accuracy = correct / total
        print('%-10s%-10s%-10s%-10s%-10s%-10s' % (
            TYPE_LIST[i], matrix[i][0], matrix[i][1], matrix[i][2], matrix[i][3], accuracy))


if __name__ == '__main__':
    filename1 = '../results/label.txt'
    filename2 = '../results/predict.txt'
    with open(filename1) as f:
        labels = [i.split() for i in f.readlines()]
    with open(filename2) as f:
        predicts = [i.split() for i in f.readlines()]
    matrix = confusion_matrix(labels, predicts)
    print_matrix(matrix)
    pass
