# Sea Battle

A classic naval combat game (also known as Battleship) implemented in Python using Tkinter for the graphical user interface.

## Overview

Sea Battle is a turn-based strategy game where players attempt to sink their opponent's fleet of ships by guessing the coordinates of their positions on a grid. This implementation allows you to play against a computer opponent.

## Features

- Graphical user interface built with Tkinter
- Player vs Computer gameplay
- Random ship placement option
- Manual ship placement
- Visual feedback for hits and misses
- Game state tracking

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

## How to Play

1. Run the game by executing the main.py file:
   ```bash
   python main.py
   ```

2. Place your ships on the grid:
   - Use the "Random" button to place ships automatically
   - Or place ships manually by clicking on the grid
   - Once satisfied with placement, click "Ready"

3. Game rules:
   - Take turns attacking the computer's grid by clicking on cells
   - Hit ships are marked in red
   - Missed shots are marked in blue
   - Sunk ships are fully revealed
   - The first player to sink all opponent ships wins

## Project Structure

- **main.py**: Entry point of the application
- **app.py**: Main application logic and UI handling
- **board.py**: Implementation of the game board
- **cell.py**: Cell representation for the game grid
- **ship.py**: Ship class definition
- **ships.py**: Fleet management and ship placement logic

## Controls

- Left-click: Place ships/Attack opponent's grid
- "Random" button: Randomly place your ships
- "Ready" button: Confirm ship placement and start the game

## Development

This project is structured in an object-oriented manner with separate classes for different components of the game. The main game logic is handled by the App class, which manages the game state and user interactions.