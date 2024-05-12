import numpy as np
import Levenshtein as lev

def calculate_similarity(spoken_phrase, command_list):
    similarities = [lev.ratio(spoken_phrase, command)
                        for command in command_list]
    return similarities
