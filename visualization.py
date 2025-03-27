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

MAX_VERTICES = 5000

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'


def setup_graph(transport_graph: graph.Graph,
                layout: str = 'spring_layout',
                max_vertices: int = 5000) -> list:
    """Use plotly and networkx to setup the visuals for the given graph.
    """

    graph_nx = transport_graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    x_edges = []
    y_edges = []

    for edge in graph_nx.edges:
        x1, x2 = pos[edge[0]][0], pos[edge[1]][0]
        x_edges += [x1, x2, None]
        y1, y2 = pos[edge[0]][1], pos[edge[1]][1]
        y_edges += [y1, y2, None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines+text',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=1),
                     )

    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data = [trace3, trace4]

    return data


def visualize_graph(transport_graph: graph.Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 5000,
                    output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """
    draw_graph(setup_graph(transport_graph, layout, max_vertices), output_file)


def draw_graph(data: list, output_file: str = '', weight_positions=None) -> None:
    """
    Draw graph based on given data.

    Optional arguments:
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
        - weight_positions: weights to draw on edges for a weighted graph
    """

    fig = Figure(data=data)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if weight_positions:
        for w in weight_positions:
            fig.add_annotation(
                x=w[0], y=w[1],  # Text annotation position
                xref="x", yref="y",  # Coordinate reference system
                text=w[2],  # Text content
                showarrow=True  # Show arrow
            )

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['networkx', 'graph', 'plotly.graph_objs'],
        'allowed-io': [],
        'max-line-length': 120
    })
