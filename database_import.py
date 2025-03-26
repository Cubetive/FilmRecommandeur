"""CSC111 Project 2: OptiTransport - Database Import

This Python module is used to import database from the database directory.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
from graph import Graph


def load_service_graph(database_file: str) -> Graph:
    """Return a service graph with the given dataset

    Preconditions:
        - database_file is the path to a CSV file corresponding to the following
        service formatting:
            name, service type, departure, arrival, price, accessibility, user preference, average delay
    """
    # TODO Implement the method and get a database which corresponds to this
