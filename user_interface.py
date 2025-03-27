"""CSC111 Project 2: FilmRecommandeur - User Interface

This Python module is used to build the user interface for the application.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
from PyQt5.QtWidgets import QWidget


class UserInterface(QWidget):
    """The main User Interface for the movie recommender.
    """
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['QWidget'],
        'allowed-io': [],
        'max-line-length': 120
    })
