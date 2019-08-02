from ...models import Req, Dep, DepType

import networkx as nx
import operator

def importReqsToGraph():
    g = nx.DiGraph()
    for d in Dep.objects.all():
        g.add_edge(d.source.text, d.destination.text)
    return g



#transofrms a directed cyclic graph to directed acyclic graph by compressing the components of the graph into one node
def transformToDAG(G):
    g2 = nx.DiGraph()
    components = list(nx.strongly_connected_components(G))
    for component in components:
        new_node = ','.join(str(e) for e in component)
        if not(new_node in g2.nodes):
            g2.add_node(new_node, size=len(component))
    
        suc_nodes = set()
        for e in component:
            for nei in G.neighbors(e):
                if not (nei in component):
                    suc_nodes.add(nei)
        for node in suc_nodes:
            for c in components:
                if node in c:
                    to_n = ','.join(str(e) for e in c)
                    break
            if not(to_n in g2.nodes):
                g2.add_node(to_n, size=len(component))
            if not((new_node, to_n) in g2.edges):
                g2.add_edge(new_node, to_n, weight=g2.node[to_n]['size'])
    return g2
    

#finds all the bridges based on importance --> based on their weight and returns a soreted list of couples of edge and weigth
def getBridges(G):
    bridges = {}
    for brg in nx.bridges(G.to_undirected()):
        if (brg[1], brg[0]) in G.edges:
            bridges[(brg[1], brg[0])] = G.get_edge_data(brg[1], brg[0], 'weight')['weight']
        else:
            bridges[brg] = G.get_edge_data(brg[0], brg[1], 'weight')['weight']
    sorted_brgs = sorted(bridges.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_brgs


def getLongestPath(G):
    return nx.dag_longest_path(G)


#find shortest (longest) paths between the root and all leaves --> as parallel paths
def calculatePathWeight(G, path):
    w = 0
    i = 0
    while i < (len(path) - 1):
        w = w + G[path[i]][path[i+1]]['weight']
        i = i + 1
    return w

def getParallelPaths(G):
    leaves = []
    roots = []
    for n in G.nodes:
        if G.out_degree(n) == 0:
            leaves.append(n)
        if G.in_degree(n) == 0:
             roots.append(n)
    paths = []
    for l in leaves:
        for r in roots:
            if not l in nx.descendants(G, r):
                continue
            p = nx.shortest_path(G, r, l, weight='weight')
            paths.append((p, calculatePathWeight(G, p)))
    paths.sort(key=operator.itemgetter(1), reverse=True)
    return paths