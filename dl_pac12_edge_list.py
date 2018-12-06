#!/usr/bin/env python3

import requests

from bs4 import BeautifulSoup

PAC12_SCHOOLS = set({
    'Washington',
    'USC',
    'California',
    'Washington State',
    'UCLA',
    'Arizona State',
    'Utah',
    'Stanford',
    'Oregon',
    'Oregon State',
    'Arizona',
    'Colorado'
})
#PAC12_URL = 'https://pac-12.com/football/schedule'
RECORD_IFNAME = 'game_record.html'
PAC12_EDGE_LIST_OFNAME = 'pac12_edge_list.csv'

'''
return list of edges where each edge is of format [winner_name, winner_score, loser_name, loser_score]
'''
def get_edge_list(record_str):
    edge_list = []
    soup = BeautifulSoup(record_str, 'html.parser')

    rows = soup.find_all('div', class_='team-detail')

    for row in rows:
        school_tags = row.find_all('img')
        schools = [school_tag.get('title') for school_tag in school_tags]
        #.find(lambda tag: tag.name == 'span' and tag['class'] == ['detail', 'tl', ''])
        score0_soup = row.find('span', {"class": ['tl']})
        score1_soup = row.find('span', {"class": ['tr']})
        if score0_soup is None or score1_soup is None:
            continue # skip the games that don't have scores yet

        score0 = int(score0_soup.decode_contents())
        score1 = int(score1_soup.decode_contents())

        #swap if schools[0] lost
        if score0 < score1:
            edge_list.append((schools[1],str(score1),schools[0],str(score0)))
        else:
            edge_list.append((schools[0],str(score0),schools[1],str(score1)))
    return edge_list

def get_pac12(edge_list):
    pac12 = []
    for edge in edge_list:
        school0, _, school1, _ = edge
        if school0 in PAC12_SCHOOLS and school1 in PAC12_SCHOOLS:
            pac12.append(edge)
    return pac12

def create_edge_list():
    with open(RECORD_IFNAME, 'r') as f:
        record_str = f.read()
    edge_list = get_edge_list(record_str)
    pac12_edge_list = get_pac12(edge_list)
    print("writing {} edge(s) to '{}' ...".format(len(pac12_edge_list), RECORD_IFNAME))
    with open(PAC12_EDGE_LIST_OFNAME, 'w+') as f:
        for edge in pac12_edge_list:
            f.write(','.join(edge)+'\n')

if __name__ == "__main__":
    create_edge_list()
