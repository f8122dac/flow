# Flow
A solution program for "flow" in python

## How to use it?
Run test_maps.py to test it out. There are 6 example maps in test_maps.py. 

solver.py has the Game object. Initialize it with dimension of a board and tuples of two starting points for each color. 
When Game.solve method is invoked, it will return boolean value indicating success or failure.

Game.steps contains the state of the board. A solution is obtained by reading Game.steps after Game.solve method concluded.
