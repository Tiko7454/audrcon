import numpy as np
import Levenshtein as lev

def calculate_similarity(spoken_phrase, command_list):
    similarities = []
    for command in command_list:
        similarities.append(lev.ratio(spoken_phrase, command))
    return similarities
