#!/usr/bin/env python3
"""tarjan_scc - Tarjan's strongly connected components algorithm.

Usage: python tarjan_scc.py [--random N E]
"""
import sys, random

def tarjan_scc(graph):
    index_counter = [0]
    stack = []
    on_stack = set()
    index = {}
    lowlink = {}
    sccs = []

    def strongconnect(v):
        index[v] = lowlink[v] = index_counter[0]
        index_counter[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])
        if lowlink[v] == index[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in graph:
        if v not in index:
            strongconnect(v)
    return sccs

def condensation(graph, sccs):
    """Build DAG of SCCs."""
    node_to_scc = {}
    for i, scc in enumerate(sccs):
        for v in scc:
            node_to_scc[v] = i
    dag = {i: set() for i in range(len(sccs))}
    for v in graph:
        for w in graph.get(v, []):
            si, sj = node_to_scc[v], node_to_scc[w]
            if si != sj:
                dag[si].add(sj)
    return {k: list(v) for k, v in dag.items()}

def main():
    n, e = 8, 12
    args = sys.argv[1:]
    if "--random" in args:
        i = args.index("--random")
        if i+2 < len(args): n, e = int(args[i+1]), int(args[i+2])
    nodes = list(range(n))
    graph = {v: [] for v in nodes}
    for _ in range(e):
        u, v = random.choice(nodes), random.choice(nodes)
        if u != v and v not in graph[u]:
            graph[u].append(v)
    print(f"Graph ({n} nodes, {sum(len(v) for v in graph.values())} edges):")
    for v in sorted(graph):
        if graph[v]:
            print(f"  {v} -> {graph[v]}")
    sccs = tarjan_scc(graph)
    print(f"\nStrongly Connected Components ({len(sccs)}):")
    for i, scc in enumerate(sccs):
        print(f"  SCC {i}: {sorted(scc)}")
    dag = condensation(graph, sccs)
    print(f"\nCondensation DAG:")
    for v in sorted(dag):
        if dag[v]:
            print(f"  SCC{v} -> {['SCC'+str(w) for w in dag[v]]}")

if __name__ == "__main__":
    main()
