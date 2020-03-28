#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "demo video with Piero"

import timeit
import cProfile
import pstats
import functools


def profile(func):
    """
    A function that can be used as a decorator to measure performance
    """
    # You need to understand how decorators are constructed and used.
    # Be sure to review the lesson material on decorators, they are used
    # extensively in Django and Flask.
    @functools.wraps(func)  # preserves the name of the original function
    def inner(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        # call the original func
        result = func(*args, **kwargs)
        profiler.disable()
        ps = pstats.Stats(profiler).strip_dirs().sort_stats('cumulative')
        ps.print_stats(10)  # Limit to top 10 results
        # return the original function result
        return result

    return inner


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """returns True if title is within movies list"""
    # This function should ideally be eliminated (or not called by the studnet)
    return title in movies
    # # Original version --don't need to lowercase everything!
    # for movie in movies:
    #     if movie.lower() == title.lower():
    #         return True
    # return False


@profile
def find_duplicate_movies(src):
    """
    Returns a list of duplicate movies from a src list
    """
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates


@profile
def find_duplicate_movies_improved(src):
    """
    Improved for faster detectin of duplicates
    """
    # movies = [movie.lower() for movie in read_movies(src)]
    moves = read_movies(src)
    # Do any sorting outside of the loop
    movies.sort()  # sorts list in-place
    # This is a clever trick list comprehension.
    # Students might also use collections.Counter
    duplicates = [m1 for m1, m2 in zip(movies[1:], movies[:-1]) if m1 == m2]
    return duplicates


def timeit_helper():
    """
    Part A:  Obtain some profiling measurements using timeit
    """
    t = timeit.Timer(
        stmt="find_duplicate_movies('movies.txt')",
        setup='from __main__ import find_duplicate_movies'
    )
    runs_per_repeat = 5
    num_repeats = 7
    result = t.repeat(repeat=num_reports, number=runs_per_repeat)
    best_time = min(result) / float(runs_per_repeat)
    print("Best time across {} repeats of {} run per repeat: {} sec".format(num_repeats)
          )


def main():
    """
    Computes a list of duplicate movie entries
    """
    # This is a function to use for part B.
    result = find_duplicate_movies('movies.txt')
    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    main()
