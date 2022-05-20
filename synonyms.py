from copy import copy
from config import *
import requests
from typing import Dict, List
from pprint import pprint

# ganked from stackoverflow
from functools import lru_cache, reduce  # forward compatibility for Python 3
import operator


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def set_by_path(root, items, value):
    """Set a value in a nested object in root by item sequence."""
    get_by_path(root, items[:-1])[items[-1]] = value

# end gank

@lru_cache(maxsize=2048)
def get_synonyms(word):
    s1 = get_synonyms_1(word)
    if len(s1) > 0:
        return s1
    else:
        return get_synonyms_2(word)

def get_all_synonyms(words):
  return {word:get_synonyms(word) for word in words}

@lru_cache(maxsize=2048)
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


@lru_cache(maxsize=2048)
def get_synonyms_2(word):
    url = get_thesaurus_2_url(word)
    rj = requests.get(url).json()
    if 'error' in rj:
        return []
    r = rj['response']
    out = [x['list']['synonyms'].replace(' (generic term)', '').replace(
        ' ' + word, '').lower().split('|') for x in r]
    return list(set([item for sublist in out for item in sublist if ' ' not in item]))


def get_all_synonyms(words):
    return {word: get_synonyms(word) for word in words}


def get_synonym_tree(word, depth=2):
    output = {}
    queue = [([], word)]
    while queue:
        path, w = queue.pop(0)
        w_syns = [s for s in get_synonyms(w) if s not in path]
        
        new_path = path + [w]
        if len(path) >= depth-1:
            set_by_path(output, new_path, w_syns)
        else:
            set_by_path(output, new_path, {k: {} for k in w_syns})
            queue += [(new_path, s) for s in w_syns]
    return output


def get_tree_size(tree):
    sum = 0
    if isinstance(tree, Dict):
        sum += len(tree.keys())
        for k in tree.keys():
            sum += get_tree_size(tree[k])
    if isinstance(tree, List):
        sum += len(tree)
    return sum
