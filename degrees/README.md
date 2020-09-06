# Degrees

**Description**: Write a program that determines how many "degrees of separation" there are between two actors. 

Video Demonstration
----------------------

 [![Project 0a: Degrees | CS50 AI 2020](http://img.youtube.com/vi/HITM0Ox-5xA/0.jpg)](https://youtu.be/HITM0Ox-5xA)


Background
----------
Using the concept of the game "Six Degrees of Kevin Bacon" and the concepts behind Breadth First Search, I used a Queue Frontier to find the shortest path to link two actors and solve this type of search problem. Begin by inputting the two actor(s)/actress(es) names and the ``` shortest_path ``` function that I implemented will find a list that relates them through the movies they starred in with other actors/actresses. The list contains pairs of tuples where each tuple corresponds to the next, [(movie1,person1),(movie2,person2)] the list is such that person 1 stars in movie 1 but has also starrred in movie 2 therefore linking them to person 2. Below is an example on how to run the code and what output you may get.

``` 
$ python degrees.py large
Loading data...
Data loaded.
Name: Emma Watson
Name: Jennifer Lawrence
3 degrees of separation.
1: Emma Watson and Brendan Gleeson starred in Harry Potter and the Order of the Phoenix
2: Brendan Gleeson and Michael Fassbender starred in Trespass Against Us
3: Michael Fassbender and Jennifer Lawrence starred in X-Men: First Class
``` 
Besides the ``` large```  excel data set there is a ``` small```  data set that you can also use. Keep in mind that between two runs of the same people you may get different results as there may be more than one way of linking those two individuals.

**NOTE**: For now, the ``` large```  excel data file is unavailable as I'm having trouble uploading these large files to github, however if you are interested you can visit: https://cs50.harvard.edu/ai/2020/projects/0/degrees/ and obtain it from there.
