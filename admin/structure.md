# Project Structure

## Project Aim
- The aim of this project is to simulate a traffic controller that controls vehicles arriving into and leaving out of an intersection

## Key ideas and concepts
# Concept of Intersection for this project
- For this project, I am going to assume that an intersection simply a meeting of 2 or more roads. We can treat each 
road to have 2 directions each (assume roads are not one way). Here I use the word 'direction' as a substitute for traffic
input
- For simplicity, I haven't distinguished between the actual directions that cars arriving into a direction want to go. For example,
in a 4 way intersection-- left, right and straight turning traffic.

# Concept of direction
- I have treated a direction in this project as particular inflow of traffic into an intersection.
- An intersection has 4 directions, north, east, south and west
- The inflow of traffic for a particular direction follows a normal distribution around a mean > 0

# Implementation 

## Classes

### Direction
- Class to represent traffic flow for one direction
- Contains attribute for the wait times for each vehicle in this direction, stored as a list
- Attribute for the average flow of traffic for this direction, arbitary number
- Method to find the total wait time of all vehicles for a particular direction

### Intersection
- Class to represent a collection of Directions forming a complete intersection
- Methods to add new vehicles to each direction after a cycle
- Represents the state of an actual intersection
- Attribute for a cyclic linked list of Direction objects. This makes it easy for a Controller object to cycle through
each direction. The idea is to start at North, then go counter clockwise to west. When the west direction is reached, it's 
next pointer points to north, and then the whole thing starts off again. In practice this can allow for virtually any
number of directions
- Method to add a new direction to the intersection
- Method that adds new vehicles to the intersection, not sure if this should be in Controller or Intersection
- Method to add waiting time to each of the vehicles in an intersection after letting one direction through the intersection

### Controller
- Controls an intersection's traffic, acts as a puppet of sorts
- Starts control of the traffic with a method start()
- 