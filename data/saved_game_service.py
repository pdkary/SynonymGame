import json
from typing import List
from data.Graph import Graph
from data.synonym_service import get_synonym_graph, add_tree_to_graph
from random import choice

GAME_FILE = 'data/premade_games.json'

def load_games():
    with open(GAME_FILE, 'r') as gf:
        return json.load(gf)

def save_games(games):
    with open(GAME_FILE, 'w') as gf:
        json.dump(games,gf)

def get_random_game(difficulty: int = 6):
    games = load_games()[difficulty]
    game = choice(games)
    print(game)
    return game

def get_all_n_length_paths(graph: Graph, n: int):
    all_paths = graph.get_all_shortest_paths()
    n_length_paths = {}
    for source in graph.nodes:
        for target in graph.nodes:
            source_paths = all_paths[source]
            if target not in source_paths:
                continue
            path = source_paths[target]
            if path is not None and len(path) == n:
                n_length_paths[source + "->" + target] = path
    return n_length_paths

def update_existing_paths():
    games = load_games()
    graph = get_synonym_graph()
    n_list = list(games.keys())
    for n in n_list:
        n_length_paths = get_all_n_length_paths(graph,n)
        if n in games:
            for k,v in  n_length_paths.items():
                games[n].append((k,v))
        else:
            games[n] = list(n_length_paths.items())
    save_games(games)

def update_all_n_length_paths(n_list: List):
    games = load_games()
    graph = get_synonym_graph()
    for n in n_list:
        n_length_paths = get_all_n_length_paths(graph,n)
        if n in games:
            for k,v in  n_length_paths.items():
                games[n].append((k,v))
        else:
            games[n] = list(n_length_paths.items())
    save_games(games)

def add_new_tree_and_update(word,depth=2):
    add_tree_to_graph(word,depth)
    update_existing_paths()

        
