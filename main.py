"""CSC111 Project 2: FilmRecommandeur - Main

This Python module contains the main code for Project 2: FilmRecommandeur.
Please consult Minh Nguyen at huynhtuanminh.nguyen@mail.utoronto.ca
for more information.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
from PyQt5.QtWidgets import QApplication

import database_import
from graph import Graph
from user_interface import UserInterface
from visualization import visualize_graph

DATABASE_FILE = 'data/rottentomatoes-400k.csv'
SENTIMENT_FILE = 'data/sentiment_scores.txt'

if __name__ == "__main__":
    # Build review graph
    review_graph = database_import.load_review_graph(DATABASE_FILE, SENTIMENT_FILE)
    visualize_graph(review_graph)

    # Build application
    app = QApplication([])
    window = UserInterface(review_graph)
    window.show()
    app.exec_()
