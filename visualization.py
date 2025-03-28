"""CSC111 Project 2: FilmRecommandeur - Database Import

This Python module is used to visualize the graphs.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
from plotly.graph_objs import Scatter, Figure
import networkx as nx

import graph

MAX_VERTICES = 250

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'


def setup_graph(transport_graph: graph.Graph,
                layout: str = 'spring_layout',
                max_vertices: int = MAX_VERTICES) -> tuple:
    """
    Use Plotly and NetworkX to setup the visuals for the given graph.
    Assumes that the Graph.to_networkx method adds a 'kind' attribute
    to each node indicating 'user' (film reviewer) or 'movie'.
    """
    graph_nx = transport_graph.to_networkx(max_vertices)
    pos = getattr(nx, layout)(graph_nx)

    x_edges, y_edges = [], []
    for edge in graph_nx.edges:
        x1, y1 = pos[edge[0]]
        x2, y2 = pos[edge[1]]
        x_edges += [x1, x2, None]
        y_edges += [y1, y2, None]

    edge_trace = Scatter(
        x=x_edges,
        y=y_edges,
        mode='lines',
        name='Reviews',
        line={"color": LINE_COLOUR, "width": 1},
        hoverinfo='none'  # No hover info for the line segments themselves.
    )

    x_users, y_users, labels_users = [], [], []
    x_movies, y_movies, labels_movies = [], [], []

    for node, data in graph_nx.nodes(data=True):
        node_x, node_y = pos[node]
        kind = data.get('kind', 'movie')
        if kind == 'user':
            x_users.append(node_x)
            y_users.append(node_y)
            labels_users.append(str(node))
        else:
            x_movies.append(node_x)
            y_movies.append(node_y)
            labels_movies.append(str(node))

    user_trace = Scatter(
        x=x_users,
        y=y_users,
        mode='markers',
        name='Film Reviewers',
        marker={"symbol": 'circle', "size": 7,
                "color": 'blue',
                "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}},
        text=labels_users,
        hovertemplate='%{text}'
    )

    movie_trace = Scatter(
        x=x_movies,
        y=y_movies,
        mode='markers',
        name='Films',
        marker={"symbol": 'square', "size": 7,
                "color": 'red',
                "line": {"color": VERTEX_BORDER_COLOUR, "width": 0.5}},
        text=labels_movies,
        hovertemplate='%{text}'
    )

    edge_mid_x = []
    edge_mid_y = []
    edge_hover_text = []

    for edge in graph_nx.edges(data=True):
        node1, node2, edge_data = edge
        x1, y1 = pos[node1]
        x2, y2 = pos[node2]
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        edge_mid_x.append(mid_x)
        edge_mid_y.append(mid_y)

        node1_kind = graph_nx.nodes[node1].get('kind', 'movie')
        node2_kind = graph_nx.nodes[node2].get('kind', 'movie')
        if node1_kind == 'movie' and node2_kind == 'user':
            film = node1
            reviewer = node2
        elif node2_kind == 'movie' and node1_kind == 'user':
            film = node2
            reviewer = node1
        else:
            film = node1
            reviewer = node2

        score = edge_data.get('score', 0)
        sentiment = edge_data.get('sentiment', 0)
        hover_text = (f"Film: {film}<br>"
                      f"Reviewer: {reviewer}<br>"
                      f"Score: {score}<br>"
                      f"Sentiment: {sentiment}")
        edge_hover_text.append(hover_text)

    edge_hover_trace = Scatter(
        x=edge_mid_x,
        y=edge_mid_y,
        mode='markers',
        name='Edge Info',
        marker={"size": 0.1, "color": 'rgba(0,0,0,0)'},
        hoverinfo='text',
        hovertext=edge_hover_text,
        showlegend=False
    )

    data = [edge_trace, user_trace, movie_trace, edge_hover_trace]
    return data, None


def visualize_graph(transport_graph: graph.Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = MAX_VERTICES,
                    output_file: str = '') -> None:
    """
    Use Plotly and NetworkX to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the Plotly image to (rather than displaying
            in your web browser)
    """
    data, _ = setup_graph(transport_graph, layout, max_vertices)
    draw_graph(data, output_file)


def draw_graph(data: list, output_file: str = '') -> None:
    """
    Draw graph based on given data.

    Optional arguments:
        - output_file: a filename to save the Plotly image to (rather than displaying
            in your web browser)
        - weight_positions: weights to draw on edges for a weighted graph
    """
    fig = Figure(data=data)
    fig.update_layout({'showlegend': True})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if output_file:
        fig.write_image(output_file)
    else:
        fig.show()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['networkx', 'plotly.graph_objs', 'graph'],
        'disable': ['R0914'],
        'allowed-io': [],
        'max-line-length': 120
    })
