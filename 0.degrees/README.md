# degrees

Write a program that determines how many “degrees of separation” apart two actors are.


## STANDARD OUTPUT

      $ python degrees.py large
      Loading data...
      Data loaded.
      Name: Emma Watson
      Name: Jennifer Lawrence
      3 degrees of separation.
      1: Emma Watson and Brendan Gleeson starred in Harry Potter and the Order of the Phoenix
      2: Brendan Gleeson and Michael Fassbender starred in Trespass Against Us
      3: Michael Fassbender and Jennifer Lawrence starred in X-Men: First Class


## ASSIGNMENT

Complete the implementation of the shortest_path function such that it returns the shortest path from the person with id source to the person with the id target.

      - Assuming there is a path from the source to the target, your function should return a list, where each list item is the next (movie_id, person_id) pair in the path from the source to the target. Each pair should be a tuple of two strings.
        - For example, if the return value of shortest_path were [(1, 2), (3, 4)], that would mean that the source starred in movie 1 with person 2, person 2 starred in movie 3 with person 4, and person 4 is the target.
      - If there are multiple paths of minimum length from the source to the target, your function can return any of them.
      - If there is no possible path between two actors, your function should return None.
      - You may call the neighbors_for_person function, which accepts a person’s id as input, and returns a set of (movie_id, person_id) pairs for all people who starred in a movie with a given person.
