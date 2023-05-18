import requests
from bs4 import BeautifulSoup


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
            urls.append(f'https://astrorok.ru/2023/goroskop-na-{month}-2023-goda-{sign}.php')
            urls.append(f'https://astrorok.ru/2023/lyubovnyij-goroskop-na-{month}-2023-goda-{sign}.php')
    for month in months:
        urls.append(f'https://astrorok.ru/2023/goroskop-na-{month}-2023-goda.php')
        urls.append(f'https://astrorok.ru/goroskop/goroskop-na-{month}-2023-goda.php')
    return urls


def main():
    links = url_maker()
    text_saver('\n'.join(links), 'links')
    links = links_getter('links.txt')
    print(len(links))
    links = set(links)
    print(len(links))
    for link in links:
        text = text_getter(link)
        # print(text)
        text_saver(text, 'corpus')


if __name__ == '__main__':
    main()
