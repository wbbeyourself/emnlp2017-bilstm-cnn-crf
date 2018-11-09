# coding = utf-8
from __future__ import print_function
import re
import logging


def maxIndexValue(sentences, featureName):
    maxItem = 0
    for sentence in sentences:
        for entry in sentence[featureName]:
            maxItem = max(maxItem, entry)

    return maxItem

# 一些预处理，替换日期、时间、数字、标点符号等
def wordNormalize(word):
    word = word.lower()
    word = word.replace("--", "-")
    word = re.sub("\"+", '"', word)
    word = re.sub("[0-9]{4}-[0-9]{2}-[0-9]{2}", 'DATE_TOKEN', word)
    word = re.sub("[0-9]{2}:[0-9]{2}:[0-9]{2}", 'TIME_TOKEN', word)
    word = re.sub("[0-9]{2}:[0-9]{2}", 'TIME_TOKEN', word)
    word = re.sub("[0-9.,]+", 'NUMBER_TOKEN', word)
    return word


def mapTokens2Idx(sentences, word2Idx):
    numTokens = 0
    numUnknownTokens = 0
    for sentence in sentences:
        for idx in range(len(sentence['raw_tokens'])):
            token = sentence['raw_tokens'][idx]
            wordIdx = word2Idx['UNKNOWN_TOKEN']
            numTokens += 1
            if token in word2Idx:
                wordIdx = word2Idx[token]
            elif token.lower() in word2Idx:
                wordIdx = word2Idx[token.lower()]
            elif wordNormalize(token) in word2Idx:
                wordIdx = word2Idx[wordNormalize(token)]
            else:
                numUnknownTokens += 1

            sentence['tokens'][idx] = wordIdx

    if numTokens > 0:
        logging.info("Unknown-Tokens: %.2f%%" % (numUnknownTokens / float(numTokens) * 100))


if __name__ == '__main__':
    s = '你好  ... ------ 2018-11-19  2018:11:78 16:01 2432 3543 45 645 654 6 5"""""""afsd JHGHUGUGUYV11312 12323"'
    print(s)
    print(wordNormalize(s))
    pass
