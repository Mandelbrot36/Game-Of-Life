![image](https://user-images.githubusercontent.com/107262375/190929856-eb3c5009-7ae3-42ef-a14e-ef3c0d705fe4.png)

John Conway's implementation of a cellular automaton - Game Of Life.
This implementation runs on a finite plane (of editable size), divided into cells. Each cell has 8 neighbours. Each cell must be either alive or dead.
The states of the cells change in discrete steps.
Conditions as to whether cells are alive or dead are editable by the user. 

The base class is the Cell class representing an individual cell.
The Space class represents our cell space, which are strong components of the Space class.
The GameMaster class deals with the 'physics' of the game. Its partial component is the Space class.
This class deals with checking the conditions as to the survival / formation of cells.
The graphical representation is handled by the GameOfLife class.
Its strong components are GameMaster and Space.
Its main task is to communicate between the graphical representation of the game board and its inner layer.
The game itself can be simulated without its graphical representation.
The Stats class deals with counting and storing simple statistics about our game. 
It is dependent on the GameOfLife class.
