#!/usr/bin/python
# This scripts loads a pretrained model and a raw .txt files. It then performs sentence splitting and tokenization and passes
# the input sentences to the model for tagging. Prints the tokens and the tags in a CoNLL format to stdout
# Usage: python RunModel.py modelPath inputPath
# For pretrained models see docs/Pretrained_Models.md
from __future__ import print_function
import os
import nltk
from util.preprocessing import addCharInformation, createMatrices, addCasingInformation
from neuralnets.BiLSTM import BiLSTM
import sys

if len(sys.argv) < 2:
    print("Usage: python RunWordCheckModelOneByOne.py modelPath")
    exit()

modelPath = sys.argv[1]

inputPath = 'adas'

# 假设文件名都是txt的形式
if not os.path.isfile(modelPath):
    print('%s : file does not exist!!!' % modelPath)
    exit(-1)

# :: Load the model ::
lstmModel = BiLSTM.loadModel(modelPath)


def print_result(tokens, types):
    assert len(tokens) == len(types)
    s = ''
    for i, t in enumerate(types):
        if t == 'A':
            s += tokens[i]
        else:
            s += '[%s %s]' % (tokens[i], t)
    s += '\n'
    print(s)


while True:
    sentences = input('sentence: ')
    if len(sentences) < 1:
        print('请输入句子!\n')
        continue
    sentences = [{'tokens': [c for c in sentences.strip()]}]
    addCharInformation(sentences)
    addCasingInformation(sentences)
    dataMatrix = createMatrices(sentences, lstmModel.mappings, True)

    # :: Tag the input ::
    tags = lstmModel.tagSentences(dataMatrix)

    for sentenceIdx in range(len(sentences)):
        tokens = sentences[sentenceIdx]['tokens']
        types_of_sentence = []
        for tokenIdx in range(len(tokens)):
            for modelName in sorted(tags.keys()):
                tokenTag = tags[modelName][sentenceIdx][tokenIdx]
                types_of_sentence.append(tokenTag)
        print_result(tokens, types_of_sentence)
