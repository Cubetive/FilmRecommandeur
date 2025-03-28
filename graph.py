"""CSC111 Project 2: FilmRecommandeur - Graph

This Python module contains the Graph structure code for Project 2: FilmRecommandeur.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
from __future__ import annotations
from typing import Any, Union

import networkx as nx


MAX_VERTICES = 5000


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or movie.
        - kind: The type of this vertex: 'user' or 'movie'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - kind in ['user', 'movie']
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    kind: str
    neighbours: dict[_Vertex, list[float]]

    def __init__(self, item: Any, kind: str, neighbours: dict[_Vertex, list[float]]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.kind = kind
        self.neighbours = neighbours

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def weight(self, other: _Vertex) -> float:
        """Return the weight of the edge between self and other."""
        if other in self.neighbours:
            return self.neighbours[other][0]
        else:
            return 0

    def advanced_weight(self, other: _Vertex) -> float:
        """Return the advanced weight of the edge between self and other.
        Advanced weight is calculated by:
            advanced_weight = score + (score * sentiment_score)
        """
        if other in self.neighbours:
            score, sentiment_score = self.neighbours[other]
            return round(score + (score * sentiment_score), 1)
        else:
            return 0

    def similarity_score_unweighted(self, other: _Vertex) -> float:
        """Return the unweighted similarity score between this vertex and other."""
        if self.degree() == 0 or other.degree() == 0:
            return 0
        else:
            our_neighbours = set(self.neighbours.keys())
            their_neighbours = set(other.neighbours.keys())

            intersect = set.intersection(our_neighbours, their_neighbours)
            union = set.union(our_neighbours, their_neighbours)
            return len(intersect) / len(union)

    def similarity_score_weighted(self, other: _Vertex, restriction: int) -> float:
        """Return the weighted similarity score between this vertex and other,
        using only the scoring system.
        """
        if self.degree() == 0 or other.degree() == 0:
            return 0
        else:
            our_neighbours = set(self.neighbours.keys())
            their_neighbours = set(other.neighbours.keys())

            intersect = set.intersection(our_neighbours, their_neighbours)
            intersect_restrict = set([vertex for vertex in intersect
                                      if abs(self.weight(vertex) - other.weight(vertex)) <= restriction])
            union = set.union(our_neighbours, their_neighbours)
            return len(intersect_restrict) / len(union)

    def similarity_score_weighted_plus(self, other: _Vertex, restriction: int) -> float:
        """Return the weighted similarity score between this vertex and other,
        using both the scoring system and sentiment scores.
        """
        if self.degree() == 0 or other.degree() == 0:
            return 0
        else:
            our_neighbours = set(self.neighbours.keys())
            their_neighbours = set(other.neighbours.keys())

            intersect = set.intersection(our_neighbours, their_neighbours)
            intersect_restrict = set([vertex for vertex in intersect
                                      if abs(self.advanced_weight(vertex) - other.advanced_weight(vertex))
                                      <= restriction])
            union = set.union(our_neighbours, their_neighbours)
            return len(intersect_restrict) / len(union)


class Graph:
    """A (weighted) graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind, {})

    def add_edge(self, item1: Any, item2: Any, weight: list[float]) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_weight(self, item1: Any, item2: Any, advanced: bool = False) -> Union[int, float]:
        """Return the weight of the edge between the given items.

        Return 0 if item1 and item2 are not adjacent.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]

        if advanced:
            return v1.advanced_weight(v2)
        else:
            return v1.weight(v2)

    def average_weight(self, item: Any) -> float:
        """Return the average weight of the edges adjacent to the vertex corresponding to item.

        Raise ValueError if item does not corresponding to a vertex in the graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return sum(v.neighbours.values()) / len(v.neighbours)
        else:
            raise ValueError

    def to_networkx(self, max_vertices: int = MAX_VERTICES, advanced: bool = False) -> nx.Graph:
        """Convert this graph into a directional networkx graph

        max_vertices specifies the maximum number of vertices that can appear in the graph.

        Preconditions:
            - max_vertices > 0
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            if v.item not in graph_nx and graph_nx.number_of_nodes() < max_vertices:
                graph_nx.add_node(v.item, kind=v.kind)
            if v.item in graph_nx:
                for u in v.neighbours:
                    if u.item not in graph_nx:
                        if graph_nx.number_of_nodes() < max_vertices:
                            graph_nx.add_node(u.item, kind=u.kind)
                        else:
                            continue
                    score = v.neighbours[u][0]
                    sentiment = v.neighbours[u][1]
                    if advanced:
                        advanced_weight = v.advanced_weight(u)
                        graph_nx.add_edge(v.item, u.item,
                                          score=score,
                                          sentiment=sentiment,
                                          advanced_weight=advanced_weight)
                    else:
                        graph_nx.add_edge(v.item, u.item,
                                          score=score,
                                          sentiment=sentiment)
        return graph_nx

    def get_similarity_score(self, item1: Any, item2: Any,
                             score_type: str = 'unweighted', restriction: int = 5) -> float:
        """Return the similarity score between the two given items in this graph.

        The similarity score will be based on the score_type, which can be 'unweighted',
        'weighted', or 'advanced_weighted'. It will also be based on a restriction,
        which will determines how similar the scores should be (only applies to 'weighted'
        and 'advanced_weighted')

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - score_type in {'unweighted', 'weighted', 'advanced_weighted'}
            - restriction >= 0
        """
        if item1 in self._vertices and item2 in self._vertices:
            if score_type == 'unweighted':
                return self._vertices[item1].similarity_score_unweighted(self._vertices[item2])
            elif score_type == 'weighted':
                return self._vertices[item1].similarity_score_weighted(self._vertices[item2], restriction)
            else:
                return self._vertices[item1].similarity_score_weighted_plus(self._vertices[item2], restriction)
        else:
            raise ValueError

    def recommend_movie(self, movie: str, limit: int,
                        score_type: str = 'unweighted', restriction: int = 5) -> list[tuple[float, str, str]]:
        """Return a list of tuples of up to <limit> recommended movies based on similarity to the given movie.
        The tuple will contain the following information: movie title, similarity score, similar to

        Preconditions:
            - movie in self._vertices
            - self._vertices[movie].kind == 'movie'
            - limit >= 1
            - score_type in {'unweighted' , 'weighted', 'advanced_weighted'}
            - restriction >= 0
        """
        # A list of tuples between similarity score and book title
        ratings = []

        # Add other book items and their similarity score with *book*
        for movie_item in self.get_all_vertices('movie'):
            if movie_item != movie:
                similarity_score = self.get_similarity_score(movie, movie_item, score_type, restriction)
                if similarity_score > 0.0:
                    ratings.append((round(similarity_score * 1000, 2), movie_item, movie))

        # Sort ratings from highest to lowest
        ratings.sort(reverse=True)

        # Return min{limit. len(ratings)} recommended books
        return [ratings[i] for i in range(min(limit, len(ratings)))]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['networkx'],
        'disable': ['R1702'],
        'allowed-io': [],
        'max-line-length': 120
    })
