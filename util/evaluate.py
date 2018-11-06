# coding=utf-8

"""
@author: beyourself
@time: 2018/11/6 18:29
@file: evaluate.py
"""


def confusion_matrix(label, predict, tags=['A', 'B', 'C']):
    num_tags = len(tags)
    matrix = [[0 for i in range(num_tags)] for i in range(num_tags)]
    for i, types in enumerate(label):
        assert len(types) == len(predict[i])
        for j, t in enumerate(types):
            index_a = tags.index(t)
            index_predict = tags.index(predict[i][j])
            matrix[index_a][index_predict] += 1
    return matrix


def print_matrix(matrix, tags=['A', 'B', 'C']):
    assert len(matrix[0]) == len(tags)
    length = len(tags)
    for i in range(length):
        format_string = '%-10s' * (length + 1)
        print(format_string % (tags[i], matrix[i][0], matrix[i][1], matrix[i][2]))


filename1 = '../results/label.txt'
filename2 = '../results/predict.txt'
with open(filename1) as f:
    labels = [i.split() for i in f.readlines()]
with open(filename2) as f:
    predicts = [i.split() for i in f.readlines()]
matrix = confusion_matrix(labels, predicts)
print_matrix(matrix)
