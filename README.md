# Gomoku AI Engine  

This project implements a simple AI engine for the game **Gomoku**, a strategy game played on an 8×8 board. The AI simulates a competitive gameplay environment, allowing players to experience Gomoku in its standard form.  

## About Gomoku  

Gomoku is a two-player game where one player uses black stones and the other uses white stones. The game proceeds as follows:  

1. The player with black stones always makes the first move.  
2. Players alternate turns, placing one stone per turn on any empty square.  
3. The objective is to place five stones in a row (horizontally, vertically, or diagonally) before the opponent does.  

For more details, refer to the [Wikipedia page on Gomoku](http://en.wikipedia.org/wiki/Gomoku).  

## Features  

- **Game Board**  
  - 8×8 grid representing the playing area.  
  - Visual representation of the board state after each move.  
- **AI Engine**  
  - Implements a basic decision-making algorithm to simulate competitive gameplay.  
  - AI evaluates the board to identify potential winning moves or block the opponent's strategies.  
- **Standard Rules**  
  - Enforces Gomoku's standard rules, including alternating turns and checking win conditions.  

 
## AI Strategy  

The AI engine uses a simple algorithm to:  
- Identify immediate winning moves.  
- Block the opponent's winning opportunities.  
- Place stones strategically to maximize the chance of forming a winning sequence.  


## Acknowledgments

- All credit goes to Professor Michael Guerzhoy
