from typing import List
import numpy as np

def nested_get(dic, keys):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    return dic[keys[-1]]

def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

class Node(object):
    def __init__(self,root, children: List[str] =[]):
        self.root = root
        self.children = children
    
    def add_children(self,children: list[str]):
        self.children += children
    
    def to_json(self):
        return dict(root=self.root,children=self.children)
    
    def __str__(self):
        return str(self.to_json())

class Graph(object):
    def __init__(self,nodes: List[Node] = []):
        self.nodes = {n.root:n for n in nodes}
    
    def add_node(self,node: Node):
        if node in self.nodes:
            self.nodes[node.root].add_children(node.children)
        else:
            self.nodes[node.root] = node
    
    ##builds tree using dfs
    def get_tree(self, root, depth):
        root_node = self.nodes[root]
        node_children = root_node.children
        if depth == 1:
            return node_children
        else:
            return {root:{c: self.get_tree(c,depth-1) for c in node_children}}
    
    def dijkstra(self,source:str):
        ## list of node names
        Q = []
        dist = {}
        prev = {}
        for v in self.nodes:
            dist[v] = np.inf
            prev[v] = None
            Q.append(v)

        dist[source] = 0

        while Q:
            u = min(Q, key=dist.get)
            Q.remove(u)
            neighbors_in_Q = [x for x in self.nodes[u].children if x in Q]
            for v in neighbors_in_Q:
                alt = dist[u] + 1
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
        return dist,prev
    
    def get_shortest_paths_from(self,source):
        paths = {}
        dist_source, prev_source = self.dijkstra(source)
        for target in self.nodes:
            if target is None or dist_source[target] == np.inf:
                continue
            path = [target]
            d = np.inf
            t = target
            while d > 1:
                d = dist_source[t]
                p = prev_source[t]
                path = [p] + path
                t = p
                if d == np.inf:
                    path = None
                    break
            paths[target] = path
        return paths
    
    def get_all_shortest_paths(self):
        paths = {}
        for source in self.nodes:
            paths[source] = self.get_shortest_paths_from(source)
        return paths
    
    def to_json(self):
        return {root:node.to_json() for root,node in self.nodes.items()}
    
    def __str__(self):
        return str(self.to_json())
