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

if len(sys.argv) < 3:
    print("Usage: python RunModel.py modelPath inputPath")
    exit()

modelPath = sys.argv[1]
inputPath = sys.argv[2]

# 假设文件名都是txt的形式
if not os.path.isfile(inputPath):
    print('%s : file does not exist!!!')
    exit(-1)
dir_path = os.path.dirname(os.path.abspath(inputPath))
prefix = os.path.basename(inputPath).split('.')[0]
predict_type_path = os.path.join(dir_path, prefix + '_predict.txt')
predict_sentence_type_path = os.path.join(dir_path, prefix + '_predict_with_sentence.txt')

predicted_sentences = []
predicted_types = []

# :: Read input ::
with open(inputPath, encoding='utf-8') as f:
    # :: Prepare the input ::
    sentences = [{'tokens': [c for c in sent.strip()]} for sent in f if len(sent) > 1]

# :: Load the model ::
lstmModel = BiLSTM.loadModel(modelPath)

addCharInformation(sentences)
addCasingInformation(sentences)
dataMatrix = createMatrices(sentences, lstmModel.mappings, True)

# :: Tag the input ::
tags = lstmModel.tagSentences(dataMatrix)

# :: Output to stdout ::
for sentenceIdx in range(len(sentences)):
    tokens = sentences[sentenceIdx]['tokens']
    types_of_sentence = []
    for tokenIdx in range(len(tokens)):
        for modelName in sorted(tags.keys()):
            tokenTag = tags[modelName][sentenceIdx][tokenIdx]
            types_of_sentence.append(tokenTag)
    predicted_sentences.append(' '.join(tokens))
    predicted_types.append(' '.join(types_of_sentence))

print('writing predict_type_path file ...')
with open(predict_type_path, 'w', encoding='utf-8') as f:
    for line in predicted_types:
        f.write(line + '\n')

print('writing predict_sentence_type_path file ...')
with open(predict_sentence_type_path, 'w', encoding='utf-8') as f:
    for i, types in enumerate(predicted_types):
        f.write(predicted_sentences[i] + '\n')
        f.write(types + '\n')

print('Compelte!!!')
