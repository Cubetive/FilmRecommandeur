"""CSC111 Project 2: FilmRecommandeur - User Interface

This Python module is used to build the user interface for the application.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QButtonGroup, QComboBox, QGridLayout, QMainWindow, QPushButton,
    QRadioButton, QScrollArea, QSlider, QWidget, QLabel, QGroupBox,
    QHBoxLayout, QVBoxLayout
)

from graph import Graph

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480

MINIMUM = 5
MAXIMUM = 25
LIMIT = 50


class UserInterface(QMainWindow):
    """The main User Interface for the movie recommender.

    Instance Attributes:
        - graph: The graph used by the UI.
        - is_running: whether or not the command is currently running.
    """
    # Private Instance Attributes:
    #     - _widgets:
    #         A collection of widgets contained in the User Interface.
    #         This is use for the purpose of methods accessing necessary widgets.
    #     - _output_widgets:
    #         A collection which stores the outputwidgets
    _widgets: QWidget = {}
    _output_widgets: set[QGroupBox] = set()
    graph: Graph
    is_running: bool

    def __init__(self, graph: Graph) -> None:
        """Initializing QWidget / User Interface"""
        super().__init__()
        # Setup
        self.graph = graph
        self.is_running = False

        # App settings
        self.setWindowTitle('Movie Recommender')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Layout
        layout = QHBoxLayout()

        # Movie selection and other settings
        settings_box = self.build_settings_widget()
        # Output box
        output_box = self.build_output_widget()

        # Build container
        layout.addWidget(settings_box)
        layout.addWidget(output_box)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def build_settings_widget(self) -> QGroupBox:
        """Submethod to build the selection and settings widget
        """
        # New box and layout
        settings_box = QGroupBox()
        settings_box_layout = QVBoxLayout()

        # Selection box
        selection_box = QGroupBox()
        selection_layout = QGridLayout()
        selection_box.setLayout(selection_layout)
        settings_box_layout.addWidget(selection_box)

        # Selection box (lable)
        selection_label = QLabel('Movie selection')
        selection_layout.addWidget(selection_label, 0, 0, Qt.AlignTop)

        # Selection box (movie selection)
        for i in range(1, 5):
            normalized_name = 'movie_selection_option_' + str(i)
            self._widgets[normalized_name] = QComboBox()
            self._widgets[normalized_name].setPlaceholderText('Choose a watched/favourite movie')
            # Insert dummy
            self._widgets[normalized_name].insertItem(0, 'Unselected')
            # Import movie names
            for title in self.graph.get_all_vertices('movie'):
                self._widgets[normalized_name].insertItem(0, title)

            selection_layout.addWidget(self._widgets[normalized_name], i, 0, Qt.AlignCenter)

        # Options box
        options_box = self.build_option_box()
        settings_box_layout.addWidget(options_box)

        # Restriction Slider
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(MINIMUM)
        slider.setMaximum(MAXIMUM)
        settings_box_layout.addWidget(slider)
        self._widgets['restriction_slider'] = slider

        # Recommend button
        recommend_button = QPushButton('Recommend me movies!')
        self._widgets['recommend_button'] = recommend_button
        recommend_button.clicked.connect(self.run_recommendation_command)

        settings_box_layout.addWidget(recommend_button)

        # Set layout and return
        settings_box.setLayout(settings_box_layout)
        return settings_box

    def build_option_box(self) -> QGroupBox:
        """Submethod to build the option widget
        """
        # Options box
        options_box = QGroupBox()
        options_layout = QGridLayout()
        options_box.setLayout(options_layout)

        # Weighting options
        weighting_label = QLabel('Choose weighting')
        options_layout.addWidget(weighting_label, 0, 0, Qt.AlignLeft)

        weighting_buttom_group = QButtonGroup()
        weighting_options = ['Unweighted', 'Weighted', 'Advanced Weighted']

        for i in range(len(weighting_options)):
            normalized_name = weighting_options[i].lower().replace(' ', '_') + '_btn'
            self._widgets[normalized_name] = QRadioButton(weighting_options[i])
            weighting_buttom_group.addButton(self._widgets[normalized_name])
            options_layout.addWidget(self._widgets[normalized_name], 1, i, Qt.AlignTop)

            if i == 0:
                self._widgets[normalized_name].setChecked(True)

        # Restriction Slider
        restriction_label = QLabel('Choose Leniency Level')
        options_layout.addWidget(restriction_label, 2, 0, Qt.AlignLeft)
        minimum_label = QLabel('Strict')
        options_layout.addWidget(minimum_label, 3, 0, Qt.AlignLeft)
        maximum_label = QLabel('Lenient')
        options_layout.addWidget(maximum_label, 3, 2, Qt.AlignRight)

        return options_box

    def build_output_widget(self) -> QGroupBox:
        """Submethod to build the output widget
        """
        # Setup output
        output_box = QGroupBox()
        output_box_layout = QVBoxLayout()
        scroll_area = QScrollArea()

        # Scroll area properties
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)

        # Setup output content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        self._widgets['content_layout'] = content_layout

        scroll_area.setWidget(content_widget)
        output_box_layout.addWidget(scroll_area)

        # Set layout and return
        output_box.setLayout(output_box_layout)
        return output_box

    def build_result(self, ranking: int, movie_title: str,
                     similarity_index: float, similar_to: str) -> QGroupBox:
        """Build a box which contains the returned result
        """
        result_box = QGroupBox()
        result_layout = QGridLayout()

        title_text = QLabel(str(ranking) + ". " + movie_title)
        result_layout.addWidget(title_text, 0, 0, Qt.AlignCenter)

        index_text = QLabel("Similarity Index: " + str(similarity_index))
        result_layout.addWidget(index_text, 1, 0, Qt.AlignCenter)

        similar_to_text = QLabel("Similar to: " + similar_to)
        result_layout.addWidget(similar_to_text, 2, 0, Qt.AlignCenter)

        result_box.setLayout(result_layout)
        return result_box

    def build_recommendations(self) -> None:
        """The main method to build and display the results
        """
        # Setup
        content_layout = self._widgets['content_layout']
        user_movies = []
        temp_recommendations = []
        recommendations = []

        # Get movies
        for i in range(1, 5):
            normalized_name = 'movie_selection_option_' + str(i)
            item = self._widgets[normalized_name].currentText()

            if item not in {'', 'Unselected'}:
                user_movies.append(item)

        # Get options
        weight_mode = 'unweighted'
        if self._widgets['weighted_btn'].isChecked():
            weight_mode = 'weighted'
        elif self._widgets['advanced_weighted_btn'].isChecked():
            weight_mode = 'advanced_weighted'

        restriction = self._widgets['restriction_slider'].value()

        # Get recommendations
        for movie in user_movies:
            lst = self.graph.recommend_movie(movie, LIMIT, weight_mode, restriction)
            temp_recommendations += lst

        # Filter unnecessaries
        temp_recommendations.sort(reverse=True)

        for recommend in temp_recommendations:
            if recommend[1] in user_movies or recommend[1] in [rec[1] for rec in recommendations]:
                continue

            if len(recommendations) >= LIMIT:
                break

            recommendations.append(recommend)

        # Remove previous elements
        for widget in self._output_widgets:
            content_layout.removeWidget(widget)

        self._output_widgets = set()

        # Build widget
        for i in range(1, min(LIMIT, len(recommendations))):
            element = self.build_result(i, recommendations[i][1],
                                        recommendations[i][0], recommendations[i][2])
            self._output_widgets.add(element)
            content_layout.addWidget(element)

        # End command
        self.is_running = False
        self._widgets['recommend_button'].setText('Recommend me movies!')

    def run_recommendation_command(self) -> None:
        """Method which detects the signal upon the recommend button get pressed.
        """
        if not self.is_running:
            self.is_running = True
            self._widgets['recommend_button'].setText('Running...')
            self.build_recommendations()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Disabling E0611 because it (wrongfully) detects that there exists no pyqt5 classes.
    # for whatever reason.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui', 'graph'],
        'disable': ['E0611'],
        'allowed-io': [],
        'max-line-length': 120
    })
