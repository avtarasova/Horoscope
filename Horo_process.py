import requests
from bs4 import BeautifulSoup
from nltk.tokenize import regexp_tokenize
from collections import Counter
import random


def text_saver(text, name, sep='\n'):
    with open(f'{name}.txt', 'a+', encoding='utf-8') as myf:
        myf.write(text + sep)
    return


def links_getter(name):
    with open(name, 'r') as myf:
        links_list = myf.read().split(sep='\n')
    return links_list

def url_getter(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, features='lxml')
    a_list = soup.find_all('a')
    a_list.pop()
    links = []
    for a in a_list:
        link = a['href']
        if link[0] == '/':
            link = 'https://astrorok.ru' + link
        if link[0:4] != 'http':
            link = 'https://astrorok.ru/' + link
        links.append(link)
    return links

def text_getter(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, features='lxml')
    p_list = soup.find_all('p')
    text_list = []
    for p in p_list[:-1]:
        # print(p.text)
        if p.text not in ['\n', '', ' ']:
            text_list.append(p.text)
    return ' '.join(text_list)


def url_maker():
    urls = []
    domen = 'https://astrorok.ru/'
    hand_list = ['nedelay/', 'den/']
    postfix = ['-zavtra.php', '.php']
    signs = ['oven', 'telecz', 'blizneczyi', 'lev', 'rak', 'deva', 'vesyi',
             'scorpion', 'strelecz', 'kozerog', 'vodolej', 'ryibyi']
    signs_orig = ['oven', 'taurus', 'twins', 'lion', 'cancer', 'virgo', 'libra',
                  'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'fish']
    months = ['noyabr', 'oktyabr', 'sentyabr', 'avgust', 'iyul', 'iyun', 'aprel', 'mart']
    for sign in signs_orig:
        urls.append(domen + hand_list[1] + sign + postfix[0])
        urls.append(domen + hand_list[1] + sign + postfix[1])
        urls.append(domen + hand_list[0] + sign + postfix[1])
    for sign in signs:
        for month in months:
            urls.append(f'https://astrorok.ru/2022/goroskop-na-{month}-2022-goda-{sign}.php')
            urls.append(f'https://astrorok.ru/2022/lyubovnyij-goroskop-na-{month}-2022-goda-{sign}.php')
    for month in months:
        urls.append(f'https://astrorok.ru/2022/goroskop-na-{month}-2022-goda.php')
        urls.append(f'https://astrorok.ru/goroskop/goroskop-na-{month}-2021-goda.php')
    return urls

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
