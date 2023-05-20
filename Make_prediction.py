import requests
from bs4 import BeautifulSoup
from nltk.tokenize import regexp_tokenize
from collections import Counter
import random

def token_division(file_name, rex=r'[\S]+'):
    with open(file_name, 'r', encoding='utf-8') as file:
        list_of_tokens = regexp_tokenize(file.read(), rex)
        # Сейчас он должен разбивать на токены по одному слову
    return list_of_tokens

def bigram_division(list_of_tokens):
    list_of_bigrams = []
    for i in range(0, len(list_of_tokens) - 1):
        list_of_bigrams.append(list_of_tokens[i] + ' ' + list_of_tokens[i + 1])
    # Сейчас он должен разбивать на токены по два слова
    return list_of_bigrams

def trigram_division(list_of_tokens):
    list_of_trigrams = []
    for i in range(0, len(list_of_tokens) - 2):
        list_of_trigrams.append(list_of_tokens[i] + ' ' + list_of_tokens[i + 1] + ' ' +
                                list_of_tokens[i+2])
        # Сейчас он должен разбивать на токены по три слова
    return list_of_trigrams

def only_capital_head(list_of_trigrams, n=3):
    list_of_head = []
    for trigram in list_of_trigrams:
        temp = trigram.split()
        if temp[0][0].isupper() and temp[0][-1] not in ['!', '?', '.']:
            if n == 3:
                list_of_head.append(temp[0] + ' ' + temp[1])
            if n == 2:
                list_of_head.append(temp[0])
    return list_of_head

def creation_of_prob_tail_list_2(head, list_of_bigrams):
    list_of_tails = [bigram.split()[1] for bigram in list_of_bigrams
                     if bigram.split()[0] == head]
    prob_list_of_tails = Counter(list_of_tails).most_common()
    return prob_list_of_tails

def creation_of_prob_tail_list_3(head, list_of_trigrams):
    list_of_tails = []
    for trigram in list_of_trigrams:
        temp = trigram.split()
        if temp[0] + ' ' + temp[1] == head:
            list_of_tails.append(temp[2])
    prob_list_of_tails = Counter(list_of_tails).most_common()
    return prob_list_of_tails

def creation_of_tail_or_prob_list(prob_list_of_tails, n=0):  # by default list of tails (if n=1: probs) will be created
    out_list = []
    for pair in prob_list_of_tails:
        # print(pair)
        out_list.append(pair[n])
    return out_list


def tail_selection(head, trigram_list):
    temp = creation_of_prob_tail_list_3(head, trigram_list)
    # print(temp)
    tail_list = creation_of_tail_or_prob_list(temp, 0)
    prob_list = creation_of_tail_or_prob_list(temp, 1)
    tail = random.choices(tail_list, weights=prob_list)
    return tail[0]


def text_generator(token_list, number_of_lines=10, mode=3):
    all_head_list = bigram_division(token_list)
    trigram_list = trigram_division(token_list)
    capital_head_list = only_capital_head(all_head_list)
    head = random.choice(capital_head_list)
    output_list = head.split()
    for i in range(number_of_lines):
        while True:
            reserved_head = head
            tail = tail_selection(head, trigram_list)
            if not output_list: # or len(output_list) >= 12:
                while True:
                    if tail[-1] in ['.', '?', '!']:
                        tail = tail_selection(reserved_head, trigram_list)
                    else:
                        break
            output_list.append(tail)
            head = head.split()[1] + ' ' + tail
            last_char = head[-1]
            if len(output_list) >= 5 and last_char in ['.', '?', '!']:
                text_saver(' '.join(output_list), 'test_horoscope', sep='\n\n')
                output_list = []
                break


def main():
    token_list = token_division('corpus.txt')
    token_list.extend(token_division('aneki.txt', r'[^\d\s]+'))
    text_generator(token_list)
    text_saver('\n', 'test_horoscope')
    pass


if __name__ == '__main__':
    main()
