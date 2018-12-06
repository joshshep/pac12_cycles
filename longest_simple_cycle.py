#!/usr/bin/env python3

from pprint import pprint

import networkx as nx

EDGE_LIST_IFNAME = 'pac12_edge_list.csv'

# Finding all the elementary circuits of a directed graph
# https://epubs.siam.org/doi/pdf/10.1137/0204007

# 
def get_game_dict():
    games = {}
    with open(EDGE_LIST_IFNAME, 'r') as f:
        for line in f:
            school0, score0, school1, score1 = line[:-1].split(',')
            ordered_players = (school0, school1)
            if ordered_players in games:
                games[ordered_players].append((score0,score1))
            else:
                games[ordered_players] = [(score0,score1)]
    return games

# get the longest simple cycle from the given edge list
def get_longest_cycle(edge_list):
    G = nx.DiGraph(edge_list)
    simple_cycles = nx.simple_cycles(G)
    longest_cycle = []
    num_simple_cycles = 0 # count num ties (excluding parallel wins)
    num_same_len = 0
    for cycle in simple_cycles:
        num_simple_cycles += 1
        if len(cycle) > len(longest_cycle):
            longest_cycle = cycle
            num_same_len = 1
        elif len(cycle) == len(longest_cycle):
            num_same_len += 1
    print("found {} simple cycle(s) (excluding dup wins)".format(num_simple_cycles))
    if len(longest_cycle) == 0:
        return []
    print("found {} simple cycle(s) with max len={}".format(num_same_len, len(longest_cycle)))
    return longest_cycle

def print_edges(game_dict, cycle):
    school0 = cycle[-1]
    for school1 in cycle:
        ordered_players = (school0, school1)
        score0, score1 = game_dict[ordered_players][0]
        print("{:<16} defeats {:<16}: {}-{}".format(school0, school1, score0, score1))
        school0 = school1
    return cycle

if __name__ == "__main__":
    game_dict = get_game_dict()
    edge_list = list(game_dict.keys())
    longest_cycle = get_longest_cycle(edge_list)
    print_edges(game_dict, longest_cycle)
    print("pac12's largest circle of suck (len={}): {}".format(len(longest_cycle), longest_cycle))
