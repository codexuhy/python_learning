import numpy as np

"""
// Given a list of words and two words word1 and word2, find the shortest word distance between word1 and word2 in the list.

// ["the", "quick", "brown", "fox", "jumps", "very", "quick"]

// quick, brown: 1
// quick, fox: 2

// your method will be called repeatedly many times with different parameters.
"""
cache = ["the", "quick", "brown", "fox", "jumps", "very", "quick"]
cache = np.array(cache)

def find_shortest_distance(word1,word2):
    distances = []
    indices1 = np.where(cache == word1)[0]
    indices2 = np.where(cache == word2)[0]
    for indice1 in indices1:
        for indice2 in indices2:
            dist = np.abs(indice2 - indice1)
            distances.append(dist)
    return np.min(distances)

# distance1 = find_shortest_distance("quick","fox")
distance2 = find_shortest_distance("brown","very")
print(distance2)