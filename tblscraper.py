import httplib2
import bs4
import parser


class Player:

    def __init__(self):
        self.stats = []  # creates a new empty list for each dog

    def add_stat(self, stat):
        self.stats.append(stat)


class HTMLNotFoundError(Exception): pass


class TableNotFoundError(Exception): pass


class HeadersNotFoundError(Exception): pass


def scrape_by_html(html, headers=None, links=False, prefix=''):
    return table_to_dicts(html_to_table(html=html), headers=headers, links=links, prefix=prefix)


def scrape_by_url(url, headers=None, links=False, prefix=''):
    return table_to_dicts(html_to_table(url=url), headers=headers, links=links, prefix=prefix)


def scrape_by_file(filename, headers=None, links=False, prefix=''):
    return table_to_dicts(html_to_table(filename=filename), headers=headers, links=links, prefix=prefix)


def html_to_table(html=None, url=None, filename=None):
    if html:
        pass
    elif url:
        h = httplib2.Http('.cache')
        response, content = h.request(url, headers={'cache-control': 'max-age=315360, public'})
        html = content.decode('utf-8')
    elif filename:
        html = open(filename, mode='r', encoding='utf-8').read()
    else:
        raise HTMLNotFoundError('No HTML found, please pass in HTML as either a string, a url, or a file')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    return table


def table_to_dicts(table, headers, links=False, prefix=''):
    rows = table.find_all("tr")
    heading = table.find_all("th")
    if rows[0].find("th"):
        heading = rows.pop(0)

    if headers:
        headers = [header.lower() for header in headers]
    elif heading:
        headers = [header.get_text().strip('\u200b\t\n\r').lower() for header in heading.find_all("th") if
                   isinstance(header, bs4.element.Tag)]
    else:
        raise HeadersNotFoundError('No headers found in table, please pass in a valid list of headers')

    data = [[column.get_text().translate({ord(c): None for c in '\u200b\t\n\r'}) for column in row if
             isinstance(column, bs4.element.Tag)] for row in rows]

    data = [dict(zip(headers, row)) for row in data]

    if "date & time" in data[0]:
        for dictionary in data:
            dictionary["date & time"] = parser.parse(dictionary["date & time"], fuzzy=True)

    # add links to each dictionary if asked for
    if links:
        for i in range(len(data)):
            link = rows[i].find("a")

            if link:
                href = prefix + link["href"]
            else:
                href = None

            data[i].update({'url': href})

    return data


def delete_by_header(data, header):
    for dictionary in data:
        del dictionary[header]

    return data


def print_players(data):
    for player in data:
        print(player)


def print_players_stat(data, stat):
    for player in data:
        print(player[''].replace('*+', '') + "'s " + stat + " for 2017 was : " + player[stat])


def generate_players(data):
    print(data[0])
    players = []
    playerList = []
    for player in data:
        x = Player()

        x.add_stat(player[''].replace('*', '').replace('+', ''))
        x.add_stat(player['tm'])
        x.add_stat(player['age'])
        x.add_stat(player['pos'])
        x.add_stat(player['g'])
        x.add_stat(player['gs'])
        x.add_stat(str(player['qbrec']))
        x.add_stat(player['cmp'])
        x.add_stat(player['att'])
        x.add_stat(player['cmp%'])
        x.add_stat(player['yds'])
        x.add_stat(player['td'])
        x.add_stat(player['int'])
        x.add_stat(player['lng'])
        x.add_stat(player['y/a'])
        x.add_stat(player['y/c'])
        x.add_stat(player['y/g'])
        x.add_stat(player['rate'])
        x.add_stat(player['qbr'])
        x.add_stat(player['sk'])
        x.add_stat(player['4qc'])
        x.add_stat(player['gwd'])

        playerStats = dict(zip(['name','team', 'age', 'pos', 'games', 'gs', 'record', 'comp', 'att', 'comperc', 'yards', 'td', 'int', 'long', 'ypa', 'ypc', 'ypg', 'rating', 'qbr','sacks','4qc','gwd'], x.stats))
        playerList.append(playerStats)

    return playerList



results = scrape_by_url('https://www.pro-football-reference.com/years/2017/passing.htm')
players = generate_players(results)

for player in players:
    print(player['name'] + "'s Completion Percentage Was : " + player['comperc'])