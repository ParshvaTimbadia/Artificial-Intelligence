# Map Coloring:

Constraint Satisfaction Problem:
A constraint satisfaction problem is a problem composed of variables that have possible values (domains) and constraints on what those values can be. A solver finds a potential solution to that problem by selecting values from the domains of each variable that fit the constraints. For more information you should check out Chapter 6 of Artificial Intelligence: A Modern Approach (Third Edition) by Norvig and Russell.

We are going to look at the Map Coloring problem here.  The Map coloring problem is where you are provided with a map and no two adjacent states have the same color. Refer Section 6.1.1 in the book.
You are provided with the starter code and need to fill in the solveCSP method according to the instructions provided in the code itself. You only need to submit the map_color.py file for this part.

# Forward Planning:
 
 Planning is an important topic in AI because intelligent agents are expected to automatically plan their own actions in uncertain domains. Planning and scheduling systems are commonly used in automation and logistics operations, robotics and self-driving cars, and for aerospace applications like the Hubble telescope and NASA Mars rovers.

This project is split between implementation and analysis. First you will combine symbolic logic and classical search to implement an agent that performs progression search to solve planning problems. Then you will experiment with different search algorithms and heuristics and use the results to answer questions about designing planning systems.

Read all of the instructions below carefully before starting the project so that you understand the requirements for successfully completing the project. Understanding the project requirements will help you avoid repeating parts of the experiment, some of which can have long runtimes.
NOTE: You should read "Artificial Intelligence: A Modern Approach" 3rd edition chapter 10 or 2nd edition Chapter 11 on Planning, available on the AIMA book site before starting this project.
Getting Started (Local Environment)
If you prefer to complete the exercise in your own local environment, then follow the steps below:

NOTE: You are strongly encouraged to install pypy 3.5 (download here) for this project. Pypy is an alternative to the standard cPython runtime that tries to optimize and selectively compile your code for improved speed, and it can run 2-10x faster for this project. There are binaries available for Linux, Windows, and OS X. Simply download and run the appropriate pypy binary installer (make sure you get version 3.5) or use the package manager for your OS. When properly installed, any python commands can be run with pypy instead. (You may need to specify pypy3 on some OSes.)

●Activate the aind environment (OS X or Unix/Linux users use the command shown; Windows users only run activate aind)
$ source activate aind
Completing the Project
1.Make sure that everything is working by running the example problem (based on the cake problem from Fig 10.7 in Chapter 10.3 of AIMA ed3). The script will print information about the problem domain and solve it with several different search algorithms.
$ python example_have_cake.py
2.Complete all TODO sections in my_planning_graph.py. You should refer to the pseudocode\heuristics.md file provided, chapter 10 of AIMA 3rd edition or chapter 11 of AIMA 2nd edition (available on the AIMA book site) and the detailed instructions inline with each TODO statement. Test your code for this module by running:
$ python -m unittest -v
3.Experiment with different search algorithms using the run_search.py script. (See example usage below.) The goal of your experiment is to understand the tradeoffs in speed, optimality, and complexity of progression search as problem size increases. 
●Run the search experiment manually (you will be prompted to select problems & search algorithms)
$ python run_search.py -m
●You can also run specific problems & search algorithms - e.g., to run breadth first search and UCS on problems 1 and 2:
$ python run_search.py -p 1 2 -s 1 2
The run_search.py script allows you to choose any combination of eleven search algorithms (three uninformed and eight with heuristics) on four air cargo problems. The cargo problem instances have different numbers of airplanes, cargo items, and airports that increase the complexity of the domains.

Use your results to answer the following questions. Make a pdf for the answers to these questions.

●Which algorithm or algorithms would be most appropriate for planning in a very restricted domain (i.e., one that has only a few actions) and needs to operate in real time?
●Which algorithm or algorithms would be most appropriate for planning in very large domains (e.g., planning delivery routes for all UPS drivers in the U.S. on a given day)
●Which algorithm or algorithms would be most appropriate for planning problems where it is important to find only optimal plans?
