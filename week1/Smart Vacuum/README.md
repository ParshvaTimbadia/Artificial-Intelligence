Three different types of agents are present in a continuum world (where the value of dirt ranges from 0 to 1). The world is a grid of size m*n. The agents can move around the grid to clean dirt. If an agent is present on a tile, it will suck all the dirt from that tile, using one move. An agent can only move to any of the four neighboring tiles, using one move in doing so. The agent decides which tile to go to next based on the type of agent it is. Performance measure is the amount of dirt cleaned

A. Simple Reflex Agent
Has no memory and no state. Can sense dirt only in current tile. Chooses next move randomly. Can detect boandary of the grid.

B. Greedy Agent
Has no memory and no state. Can sense dirt in current tile and four neighboring tiles. Will choose neighboring tile with maximum dirt for next move. Can detect boandary of the grid.

C. State Agent
Has memory and state. Can sense dirt in current tile and four neighboring tiles. Will choose neighboring tile with maximum dirt for next move. Keeps a track of visited tiles and tries to avoid them. If it is surrounded by visited states on all sides, it will choose randomly. Can detect boandary of the grid.

Files included
vacuum_agent.py - Python code for the three agents and the world
environ.txt - Contains the initial state of the world (grid size and dirt present on each tile) and the agent (initial position and maximum moves allowed)
Text files 'output_partA.txt', 'output_partB.txt', and 'output_partC.txt' - The output for the program for each of the three agents. With every move and performance measure at that point is shown. The grid with current position of agents is printed at every 5 steps
comparison_table.pdf - compares the performance measure of all three agents from two different initial points
