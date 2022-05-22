import json
import time
from typing import List
import requests
from data.api_config import *
from data.Graph import Node, Graph

SYNONYM_FILE = 'data/saved_synonyms.json'

def load_synonyms():
    with open(SYNONYM_FILE, 'r') as sf:
        return json.load(sf)

def save_synonyms(syns):
    with open(SYNONYM_FILE, 'w') as sf:
        json.dump(syns,sf)

def get_syns_and_update(word):
    existing_syns = load_synonyms()
    if word in existing_syns and len(existing_syns[word]) > 0:
        existing_syns[word].sort()
        return existing_syns[word]
    else:
        out = get_oxford_syns(word)
        if len(out) == 0:
            out = get_synonyms_1(word)
        if len(out) == 0:
            out = get_synonyms_2(word)
        out.sort()
        existing_syns[word] = out
        save_synonyms(existing_syns)
        return out

def get_oxford_syns(word):
    url = oxford_url + word
    r = requests.get(url, headers=oxford_headers)
    try:
        rj = r.json()
    except Exception:
        return []
    syns = []
    if 'error' in rj:
        return []
    for res in rj["results"]:
        for lexical_entry in res['lexicalEntries']:
            for entry in lexical_entry['entries']:
                for sense in entry['senses']:
                    if 'synonyms' in sense:
                        for syn in sense['synonyms']:
                            if ' ' not in syn['text']:
                                syns.append(syn['text'].lower())
    time.sleep(10)
    return syns

def get_synonyms_1(word):
    url = get_thesaurus_1_url(word)
    r = requests.get(url)
    if len(r.content) == 0:
        return []

    rj = r.json()
    if isinstance(rj, List):
        return rj

    typ = list(rj.keys())[0]
    try:
        if 'sin' in rj:
            return list(set([s for s in [*rj[typ]['syn'], *rj[typ]['sim']] if ' ' not in s]))
        else:
            return list(set([s for s in rj[typ]['syn'] if ' ' not in s]))
    except:
        return []

def get_synonyms_2(word):
    url = get_thesaurus_2_url(word)
    rj = requests.get(url).json()
    if 'error' in rj:
        return []
    r = rj['response']
    out = [x['list']['synonyms'].replace(' (generic term)', '').replace(
        ' ' + word, '').lower().split('|') for x in r]
    return list(set([item for sublist in out for item in sublist if ' ' not in item]))

def get_synonym_graph() -> Graph:
    syns = load_synonyms()
    syn_graph = Graph()
    for k,v in syns.items():
        syn_graph.add_node(Node(k,v))
    return syn_graph

##bfs
def add_tree_to_graph(word, depth=2):
    graph = get_synonym_graph()
    queue = [([], word)]
    current_path_size = 0
    current_depth_time_start = time.time()

    while queue:
        path, w = queue.pop(0)
        ##update and save to file
        w_syns = [s for s in get_syns_and_update(w)]
        graph.add_node(Node(w,w_syns))

        if len(path) != current_path_size:
            current_path_size = len(path)
            current_depth_time_end = time.time()
            current_depth_time = current_depth_time_end - current_depth_time_start
            print('depth: ' +str(current_path_size) + '| first entry: ' + w + '| time: ' + str(current_depth_time))
            current_depth_time_start = time.time()

        new_path = path + [w]
        if len(path) < depth -1:
            queue += [(new_path, s) for s in w_syns]
    return graph.get_tree(word,depth)

