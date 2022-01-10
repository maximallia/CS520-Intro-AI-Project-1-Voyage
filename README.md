# CS520-AI-Voyage
CS520 Intro AI. Assignment #1: Voyage into the Unknown


This project is intended as an exploration of a variant of the A* search algorithm covered in class, in the traditional application of Robotic Path Planning. In particular, we are going to look at a situation where the environment is not fully known in advance, and must be learned by the agent as it moves through it.

A gridworld is a discretization of terrain into square cells that are either unblocked (traversable) or blocked. Consider the following problem: an agent in a gridworld has to move from its current cell (S) to a goal cell, the location of a stationary target. The layout of the gridworld (what cells are blocked or unblocked) is unknown. These kinds of challenges arise frequently in robotics, where a mobile platform equipped with sensors builds a map of the world as it traverses an unknown environment.

Assume that the initial cell of the agent is unblocked. The agent can move from its current cell in the four main compass directions (east, south, west, north) to any adjacent cell, as long as that cell is unblocked and still part of the gridworld. All moves take one timestep for the agent, and thus have cost 1. (We can consider this in terms of energy consumption for the agent, for instance.) The agent always knows which (unblocked) cell it is currently in, and which (unblocked) cell the target is in. The agent knows that blocked cells remain blocked and unblocked cells remain unblocked but does not know initially which cells are blocked. However, it can observe or sense the status of some of its surrounding cells (corresponding to its field of view) and remember this information for future use. By exploring the maze, collecting information on blockages, and integrating that into the whole, the agent must reach the target as efficiently as possible.
We may structure a basic agent in the following way: the agent assumes that all cells are unblocked, until it observes them to be blocked, and all path planning is done with the current state of knowledge of the gridworld under this freespace assumption. In other words, it moves according to the following strategy:
• Based on its current knowledge of the environment, it plans a path from its current position to the goal.
• This path should be the shortest (presumed) unblocked path available.
• The agent attempts to follow this path plan, observing cells in its field of view as it moves.
• Observed blocked cells or unblocked cells are remembered, updating the agent’s knowledge of the environment. • If the agent discovers a block in its planned path, it re-plans, based on its current knowledge of the environment.

• The cycle repeats until the agent either a) reaches the target or b) determines that there is no unblocked path to the target.

Because this kind of strategy depends on being able to do a lot of searches, it is important these searches be as fast as possible. To that end, we are going to implement Repeated Forward A*, where each forward path planning step is done using the A* search algorithm. Recall from class that as A* runs, it maintains four values for each cell n that it encounters:
• g(n) - this represents the length of the shortest path discovered from the initial search point to cell n so far.
• h(n) - the heuristic value, estimating the distance from the cell n to the goal node.
• f (n) - f (n) is defined to be g(n) + h(n), which estimates the distance from the initial search node to the final goal node through cell n
• parent(n) - a pointer to the previous node along the shortest path to n.
A* maintains its fringe as a priority queue (initially containing the initial search point). The priority of the fringe is given by the value of f for every node in the fringe. Under some assumptions on h, the first time the goal node comes off the fringe represents the discovery of a shortest path from start to goal node. Until then, A* removes the cell n with the smallest value of f and expands it:
• Generate the children of n (neighbors believed or known to be unoccupied).
• The successors of n are the children n′ that are newly discovered, or g(n′) > g(n) + 1.
• For each successor n′, re-set g(n′) = g(n) + 1, representing the newly discovered shortest path from the start node to n′.
• For each successor n′, set parent(n′) = n.
• For each successor n′, insert n′ into the fringe at priority f(n′) = g(n′) + h(n′), or update its priority if it is
already in the queue.
The above is repeated until termination, representing either a) an exhaustion of all possible paths with no success, or b) successfully identifying a minimal path from start to finish. Afterwards, it follows the parents from the goal node to the initial node to identify a shortest path (in reverse).

Note: g may be taken to be infinite for any node that has not yet been discovered.
Repeated Forward A* moves the agent along the identified path, until it either successfully reaches the goal or it encounters an obstacle along its planned path. In the first case, the agent has reached the target; in the second case, A* is re-called using the agents current position and any updated information about the location of obstacles. This is repeated until one of the two termination conditions for this strategy is met.

In order to analyze algorithms for this problem, we need to generate consistent environments for comparison. Do the following: for a dim by dim array, let each cell independently be blocked with probability p, and empty with probability 1 − p. Exclude the upper left corner (chosen to be the start position) and the lower right corner (chosen to be the end position) from being blocked. Write a function to generate random gridworlds in this way for a given value of p (0 < p < 1).

