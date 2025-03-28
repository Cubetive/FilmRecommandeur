"""CSC111 Project 2: FilmRecommandeur - Database Import

This Python module is used to import database from the database directory.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
import csv

from graph import Graph
from sentiment import get_sentiment_review_score, build_sentiment_score_dict


def load_review_graph(database_file: str, sentiment_file: str) -> Graph:
    """Return a review graph with the given dataset

    Preconditions:
        - database_file is the path to a CSV file corresponding to the following
        service formatting:
            index, movie title, reviewer, publisher, review, date, score
    """
    # The review graph to be returned
    review_graph = Graph()
    sentiment_dict = build_sentiment_score_dict(sentiment_file)

    with open(database_file, 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        next(reader)  # Skip header

        for row in reader:
            title, reviewer = row[1:3]
            review = row[4]
            score = row[6]

            # Import movie title
            review_graph.add_vertex(title, 'movie')
            # Import reviewer node
            review_graph.add_vertex(reviewer, 'user')
            # Import score (for now)
            sentiment_score = get_sentiment_review_score(review, sentiment_dict)
            review_graph.add_edge(title, reviewer, [float(score), sentiment_score])

    return review_graph


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['graph', 'csv', 'sentiment'],
        'allowed-io': ['load_review_graph'],
        'max-line-length': 120
    })
