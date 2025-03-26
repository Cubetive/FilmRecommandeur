"""CSC111 Project 2: OptiTransport - Graph

This Python module contains the Graph structure code for Project 2: OptiTransport.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
from __future__ import annotations
from typing import Any, Optional


class Service:
    """A service class to store information about a specific service.
    This can be either train services (such as GO Train) or airlines (like Air Canada)

    Instance Attributes:
        - name: The name of the service
        - service_type: The type of the service
        - departure: The name of the location which the service departs from
        - arrival: The name of the location which the service arrives at
        - price: The associated price to use this service (for one adult)
        - ratings: A dictionary of ratings which will have the following ratings:
            - accessibility: A weighting from 0 to 1, determining how good the accessbility service is. If
            there is no information on this, then it'll always be 0.
            - user_pref: Online ratings of the service (if applicable)
            - average_delay: The average delay time of the service (if applicable)
            - overall_rating: A computed overall rating of the service. This metric will be used
            if no preference is selected.

    Representaion Invariants:
        - price >= 0.0
        - service_type in ['train', 'plane', 'bus']
        - 0 <= ratings['accessibility'] <= 1
        - 0 <= ratings['overall_rating'] <= 5
    """
    name: str
    service_type: str
    departure: str
    arrival: str
    price: float
    ratings: dict[str, Optional[float]]

    def __init__(self, name: str, service_type: str, depature: str,
                 arrival: str, price: float, ratings: dict[str, Optional[float]]):
        self.name = name
        self.service_type = service_type
        self.departure = depature
        self.arrival = arrival
        self.price = price
        self.ratings = ratings

    def compute_overall_rating(self, other_services: set[Service]) -> None:
        """Compute the overall rating of this particular instance of service, by
        using the data from other services which shares the same edge as this service.

        Preconditions:
            - self not in other_services
        """
        # TODO: Implement the individual weighting system


class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: dict[_Vertex, set[Service]]

    def __init__(self, item: Any, neighbours: dict[_Vertex, set[Service]]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

    def compute_all_services_overall_weighting(self, services: set[Service]) -> None:
        """Compute the weighting of every service in the edge"""
        for service in services:
            service.compute_overall_rating(services ^ {service})


class Graph:
    """A graph.

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

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, dict())

    def add_edge_service(self, item1: Any, item2: Any, serv: Service) -> None:
        """Add an edge from item1 to item2 if it doesn't exist yet, then add the serv
        to the edge.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge and service (if it doesn't exist, else, only add the service)
            if v2 not in v1.neighbours:
                v1.neighbours[v2] = set()

            v1.neighbours[v2].add(serv)
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def find_optimal_route(self, item1: Any, item2: Any, filter_type='') -> list[Service]:
        """Return a list of services such that the first item has its depature location that is
        item1 and the last item of the list has its arrival location as item2.

        It will be optimized based on the filter_type, which can either be:
        overall, price, accessibility, user preference, average delay, and specific services only.

        Raise a ValueEror if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        # TODO Implement this method (when we have a plan on how to implement it)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': [],
        'max-line-length': 120
    })
