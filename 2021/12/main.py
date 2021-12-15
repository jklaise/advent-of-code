from copy import deepcopy
from itertools import chain
from typing import List, NamedTuple, Tuple


class Edge(NamedTuple):
    node1: str
    node2: str


test_data = ["start-A",
             "start-b",
             "A-c",
             "A-b",
             "b-d",
             "A-end",
             "b-end"]


def parse_data(data: List[str]) -> Tuple[List[Edge], List[Edge], List[Edge]]:
    def parse_line(line: str) -> List[Edge]:
        line = line.split('-')
        return [Edge(*line), Edge(*reversed(line))]

    # the following is a bit nasty
    all_edges = list(chain(*map(parse_line, data)))
    start_edges = list(filter(lambda x: x.node1 == 'start' or x.node2 == 'start', all_edges))
    end_edges = list(filter(lambda x: x.node1 == 'end' or x.node2 == 'end', all_edges))
    mid_edges = list(filter(lambda x: x not in start_edges and x not in end_edges, all_edges))
    start_edges = list(filter(lambda x: x.node1 == 'start', start_edges))
    end_edges = list(filter(lambda x: x.node2 == 'end', end_edges))
    return start_edges, mid_edges, end_edges


def filter_start_edges(edges: List[Edge]) -> List[Edge]:
    start_edges = list(filter(lambda x: x.node1 == 'start', edges))
    return start_edges


def filter_end_edges(edges: List[Edge]) -> List[Edge]:
    end_edges = list(filter(lambda x: x.node2 == 'end', edges))
    return end_edges


def prune_lower_case(edges: List[Edge], node: str) -> List[Edge]:
    return list(filter(lambda x: x.node1 != node and x.node2 != node, edges))


def get_candidates(path: List[Edge], edges: List[Edge]) -> List[Edge]:
    lower_case_exclude = set([e.node1 for e in path if str.islower(e.node1)])
    filter_lower_case = lambda x: x.node1 not in lower_case_exclude and x.node2 not in lower_case_exclude
    filter_matching = lambda x: x.node1 == path[-1].node2
    return list(filter(lambda x: filter_lower_case(x) and filter_matching(x), edges))


def get_new_paths(path: List[Edge], candidates: List[Edge]) -> List[List[Edge]]:
    if not candidates:
        return [path]
    new_paths = []
    for candidate in candidates:
        new_paths.append(deepcopy(path) + [candidate])
    return new_paths


def find_paths(paths: List[List[Edge]],
               candidates: List[List[Edge]],
               edges: List[Edge]) -> List[List[Edge]]:
    # handle starting with paths=[] and find starting edges
    if not paths:
        start_edges = filter_start_edges(edges)
        paths = [[edge] for edge in start_edges]
        candidates = [get_candidates(path, edges) for path in paths]
    else:
        paths = list(chain(*[get_new_paths(path, candidate) for path, candidate in zip(paths, candidates)]))
        candidates = [get_candidates(path, edges) for path in paths]

    # once we run out of candidates for all paths, return
    if not any(candidates):
        return paths
    else:
        return find_paths(paths, candidates, edges)


if __name__ == "__main__":
    with open('input.txt') as f:
        data = f.read().splitlines()

    start_edges, mid_edges, end_edges = parse_data(data)
    edges = start_edges + mid_edges + end_edges

    # Part 1
    paths = find_paths([], [], edges)
    ending_paths = list(filter(lambda path: path[-1].node2 == 'end', paths))
    print(f'Answer to Part 1 is {len(ending_paths)}')
