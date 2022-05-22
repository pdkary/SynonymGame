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
        json.dump(games, gf)

def get_random_game(difficulty: int = 3):
    games = load_games()[str(difficulty)]
    game = choice(list(games.keys()))
    return game, games[game]

def get_all_n_length_paths(graph: Graph, n_list: List[int]):
    all_paths = graph.get_all_shortest_paths()
    n_length_paths = {n:{} for n in n_list}
    for source in graph.nodes:
        for target in graph.nodes:
            source_paths = all_paths[source]
            if target in source_paths:
                path = source_paths[target]
                if str(len(path)) in n_list:
                    key = source + "->" + target
                    n_length_paths[str(len(path))][key] = path

    return n_length_paths

def update_existing_paths():
    games = load_games()
    graph = get_synonym_graph()
    n_list = list(games.keys())
    n_length_paths = get_all_n_length_paths(graph,n_list)
    for n in n_list:
        if n in games:
            for k,v in  n_length_paths[n].items():
                games[n][k] = v
        else:
            games[n] = n_length_paths[n]
    save_games(games)

def update_all_n_length_paths(n_list: List):
    games = load_games()
    graph = get_synonym_graph()
    n_length_paths = get_all_n_length_paths(graph,n_list)
    for n in n_list:
        if n in games:
            for k,v in  n_length_paths[n].items():
                games[n][k] = v
        else:
            games[n] = n_length_paths[n]
    save_games(games)

def add_new_tree_and_update(word,depth=2):
    add_tree_to_graph(word,depth)
    update_existing_paths()

        
