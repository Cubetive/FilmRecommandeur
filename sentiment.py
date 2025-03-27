"""CSC111 Project 2: FilmRecommandeur - Sentiment

This Python module is used to build and analyze the comments from the reviews, then
return a sentiment score based on keywords available. This will be used
in the advanced weighting system.

Copyright and Usage Information
===============================
This file (and other respective files associated with this project) is licensed
under the MIT License. Please consult LICENSE for further details.

Copyright (c) 2025 Minh Nguyen & Yifan Qiu
"""


def get_normalized_word_list(text: str) -> list[str]:
    """Return a list of words from a normalized text

    A normalized text is defined as the text where all nonalphanumeric elements
    are removed, and every letter is lowercase.

    >>> example = "I'm eating an ice cream."
    >>> get_normalized_word_list(example)
    ['im', 'eating', 'an', 'ice', 'cream']
    """
    word_list = text.lower().split()

    for i in range(len(word_list)):
        word = "".join([letter for letter in word_list[i] if letter.isalpha()])
        word_list[i] = word

    return word_list


def get_sentiment_review_score(review: str, sentiment_scores: dict[str, tuple[float, float]]) -> float:
    """Return the sentiment sscore for the provided review.
    """
    word_list = get_normalized_word_list(review)
    pos_score, neg_score, sen_keywords = 0, 0, 0

    for word in word_list:
        if word in sentiment_scores:
            sen_keywords += 1
            pos_score += sentiment_scores[word][0]
            neg_score += sentiment_scores[word][1]

    overall_score = (pos_score - neg_score) / sen_keywords
    return round(overall_score, 3)


def build_sentiment_score_dict(sentiment_file: str) -> dict[str, tuple[float, float]]:
    """Build a dictionary of sentiment scores based on the provided sentiment file
    """
    sentiments = {}

    with open(sentiment_file) as file:
        for line in file:
            if not line.startswith('#'):
                positive, negative, word = line.strip().split("\t")
                sentiments[word] = (float(positive), float(negative))

    return sentiments


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': ['build_sentiment_score_dict'],
        'max-line-length': 120
    })
