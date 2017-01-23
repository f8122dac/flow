# Flow
A solution program for "flow" written in plain old python
![screenshot](https://raw.githubusercontent.com/chn0905/flow/master/screenshot.png)


## Dependency
- tkinter: gui
- pickle: saving and loading games

## How to use it?
To test it out, run gui.py and draw points on the board by clicking on cells. When two points are selected, they become a `pair`. 
Press `d` key to delete a point(the order of deletion is FILO). Solve button solves the current configuration, clear button clears the board, and load and save does what it says.

A game is stored as 'a board of given dimension with multiple pairs of points within it that does not overlap with other points'.

`solver.py` has the `Game` object. Initialize it with dimension of a board and tuples of two starting points for each color. 
When `Game.solve()` method is invoked, it will return a boolean value indicating success or failure.

`Game.steps` contains the state of the board. A solution is obtained by examining `Game.steps` after `Game.solve()` method is successfully concluded.
